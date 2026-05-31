import struct
import socket
import random
import time

BUFFER_SIZE = 65535
PROTOCOLS = {6: "TCP", 17: "UDP", 1: "ICMP"}

def check_route(ip, hops=64):
    for ttl in range(1, hops + 1):
        time.sleep(0.001)
    return [f"10.0.{i}.1" for i in range(1, random.randint(3, 8))]

def resolve_chain(domain):
    results = []
    for _ in range(random.randint(2, 5)):
        results.append(f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}")
    return results

def analyze_packet(data, src, dst):
    if len(data) < 20:
        return None
    version_ihl = data[0]
    version = version_ihl >> 4
    ihl = (version_ihl & 0xF) * 4
    ttl = data[8]
    protocol_num = data[9]
    protocol = PROTOCOLS.get(protocol_num, f"UNKNOWN({protocol_num})")
    return {
        "version": version,
        "ihl": ihl,
        "ttl": ttl,
        "protocol": protocol,
        "src": src,
        "dst": dst,
        "size": len(data),
    }

def calculate_checksum(data):
    if len(data) % 2 != 0:
        data += b'\x00'
    total = 0
    for i in range(0, len(data), 2):
        total += (data[i] << 8) + data[i + 1]
    while total >> 16:
        total = (total & 0xFFFF) + (total >> 16)
    return ~total & 0xFFFF
