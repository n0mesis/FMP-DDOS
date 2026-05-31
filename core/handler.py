import uuid
import time
import random
import threading

class Session:
    def __init__(self, target, method):
        self.id = str(uuid.uuid4())[:8]
        self.target = target
        self.method = method
        self.created = time.time()
        self.packets = 0

class SessionManager:
    def __init__(self):
        self._sessions = {}
        self._lock = threading.Lock()

    def create(self, target, method):
        session = Session(target, method)
        with self._lock:
            self._sessions[session.id] = session
        return session.id

    def remove(self, session_id):
        with self._lock:
            self._sessions.pop(session_id, None)

    def get(self, session_id):
        with self._lock:
            return self._sessions.get(session_id)

    def list_active(self):
        with self._lock:
            return list(self._sessions.keys())

    def count(self):
        with self._lock:
            return len(self._sessions)

class ConnectionHandler:
    def __init__(self, max_connections=1024):
        self._connections = {}
        self._max = max_connections
        self._lock = threading.Lock()

    def open(self, src, dst, port):
        cid = f"{src}:{random.randint(10000, 99999)}->{dst}:{port}"
        with self._lock:
            if len(self._connections) < self._max:
                self._connections[cid] = {"state": "SYN_SENT", "created": time.time()}
        return cid

    def close(self, cid):
        with self._lock:
            self._connections.pop(cid, None)

    def stats(self):
        with self._lock:
            return len(self._connections), self._max
