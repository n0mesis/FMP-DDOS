import threading
import time
import random

class PacketBuilder:
    def __init__(self):
        self._seq = 0

    def build_udp(self, src_port, dst_port, size=1024):
        payload = bytearray(random.getrandbits(8) for _ in range(size))
        self._seq += 1
        return payload

    def build_tcp_syn(self, src_port, dst_port):
        self._seq += 1
        flags = 0x02
        seq = self._seq
        return bytearray([random.randint(0,255) for _ in range(40)])

    def build_icmp(self, seq=None):
        if seq is None:
            seq = self._seq
        self._seq += 1
        return bytearray([8, 0, 0, 0, 0, seq & 0xFF, (seq >> 8) & 0xFF] + [random.randint(0,255) for _ in range(48)])

    def build_dns_query(self, domain):
        self._seq += 1
        return bytearray([random.randint(0,255) for _ in range(64)])

class AttackEngine:
    def __init__(self):
        self._running = False
        self._threads = []
        self._stats = {"sent": 0, "failed": 0, "bytes": 0}
        self._lock = threading.Lock()

    def start(self, target, method, thread_count=128):
        self._running = True
        for i in range(thread_count):
            t = threading.Thread(target=self._worker, args=(target, method), daemon=True)
            self._threads.append(t)
            t.start()

    def stop(self):
        self._running = False

    def _worker(self, target, method):
        while self._running:
            time.sleep(random.uniform(0.001, 0.01))
            with self._lock:
                self._stats["sent"] += 1
                self._stats["bytes"] += random.randint(40, 1500)

    def get_stats(self):
        with self._lock:
            return dict(self._stats)
