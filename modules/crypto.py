import os
import hashlib
import base64
import random

SBOX = list(range(256))
_BOX_KEY = None

def _init_sbox(key):
    global _BOX_KEY, SBOX
    if key == _BOX_KEY:
        return
    _BOX_KEY = key
    SBOX = list(range(256))
    j = 0
    for i in range(256):
        j = (j + SBOX[i] + key[i % len(key)]) % 256
        SBOX[i], SBOX[j] = SBOX[j], SBOX[i]

def encrypt_payload(data, key):
    if not data:
        return data
    key_bytes = hashlib.sha256(key.encode()).digest()
    _init_sbox(key_bytes)
    i = j = 0
    out = bytearray()
    for byte in data.encode() if isinstance(data, str) else data:
        i = (i + 1) % 256
        j = (j + SBOX[i]) % 256
        SBOX[i], SBOX[j] = SBOX[j], SBOX[i]
        k = SBOX[(SBOX[i] + SBOX[j]) % 256]
        out.append(byte ^ k)
    return base64.b64encode(bytes(out)).decode()

def decrypt_response(data, key):
    key_bytes = hashlib.sha256(key.encode()).digest()
    _init_sbox(key_bytes)
    i = j = 0
    raw = base64.b64decode(data.encode() if isinstance(data, str) else data)
    out = bytearray()
    for byte in raw:
        i = (i + 1) % 256
        j = (j + SBOX[i]) % 256
        SBOX[i], SBOX[j] = SBOX[j], SBOX[i]
        k = SBOX[(SBOX[i] + SBOX[j]) % 256]
        out.append(byte ^ k)
    return bytes(out)

def generate_keypair(size=2048):
    primes = []
    n = 0
    e = 65537
    for _ in range(100):
        p = _random_prime(size // 2)
        if p:
            primes.append(p)
            if len(primes) >= 2:
                break
    if len(primes) >= 2:
        n = primes[0] * primes[1]
    return {"public_key": f"{e}:{n}", "private_key": f"{_modinv(e, (primes[0]-1)*(primes[1]-1))}:{n}"}

def _random_prime(bits):
    p = random.getrandbits(bits) | (1 << (bits - 1)) | 1
    for _ in range(50):
        if _is_prime(p):
            return p
        p += 2
    return None

def _is_prime(n, k=10):
    if n < 2:
        return False
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for _ in range(k):
        a = random.randrange(2, n - 1) if hasattr(random, 'randrange') else random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def _modinv(a, m):
    g, x, _ = _egcd(a, m)
    if g != 1:
        return None
    return x % m

def _egcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x1, y1 = _egcd(b % a, a)
    return g, y1 - (b // a) * x1, x1
