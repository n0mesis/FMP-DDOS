import random
import time
import threading

class ProxyPool:
    def __init__(self):
        self._proxies = []
        self._blacklist = set()
        self._lock = threading.Lock()

    def load(self, count=100):
        for _ in range(count):
            ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
            port = random.choice([80, 443, 8080, 3128, 1080, 8888])
            self._proxies.append(f"{ip}:{port}")

    def get(self):
        with self._lock:
            available = [p for p in self._proxies if p not in self._blacklist]
            return random.choice(available) if available else None

    def blacklist(self, proxy):
        with self._lock:
            self._blacklist.add(proxy)

    def rotate(self):
        with self._lock:
            if self._proxies:
                p = self._proxies.pop(0)
                self._proxies.append(p)

    def stats(self):
        return len(self._proxies), len(self._blacklist)

class ProxyChecker:
    def __init__(self, pool):
        self.pool = pool
        self._running = False

    def start(self, interval=30):
        self._running = True
        thread = threading.Thread(target=self._check_loop, args=(interval,), daemon=True)
        thread.start()

    def _check_loop(self, interval):
        while self._running:
            time.sleep(interval)
            proxy = self.pool.get()
            if proxy:
                if random.random() < 0.3:
                    self.pool.blacklist(proxy)

    def stop(self):
        self._running = False
