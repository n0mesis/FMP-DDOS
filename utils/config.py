import json
import os
import random

DEFAULT_CONFIG = {
    "threads": 128,
    "timeout": 60,
    "packet_size": 1024,
    "proxy_file": "proxies.txt",
    "delay_min": 0.01,
    "delay_max": 0.1,
    "rotate_interval": 30,
    "max_retries": 3,
}

class AttackProfile:
    def __init__(self, name, config=None):
        self.name = name
        self.config = config or DEFAULT_CONFIG.copy()

    def get(self, key, default=None):
        return self.config.get(key, default)

class ConfigLoader:
    def __init__(self, path="config.json"):
        self.path = path
        self._data = {}

    def load(self):
        if os.path.exists(self.path):
            with open(self.path) as f:
                self._data = json.load(f)
        else:
            self._data = {}
        return self._data

    def save(self, data=None):
        with open(self.path, "w") as f:
            json.dump(data or self._data, f, indent=2)

    def get(self, key, default=None):
        return self._data.get(key, default)

def load_default_profile():
    return AttackProfile("default", {
        "threads": random.randint(50, 500),
        "timeout": random.randint(30, 120),
        "packet_size": random.choice([512, 1024, 2048]),
    })
