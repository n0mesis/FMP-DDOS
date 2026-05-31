import random
import struct

OUI_DB = [
    "00:11:22", "00:1A:2B", "00:50:56", "00:0C:29",
    "08:00:27", "52:54:00", "00:15:5D", "00:1D:60",
    "00:E0:4C", "00:90:F5", "00:1B:21", "00:25:90",
]

def random_mac():
    oui = random.choice(OUI_DB)
    nic = ":".join(f"{random.randint(0,255):02X}" for _ in range(3))
    return f"{oui}:{nic}"

def random_ttl():
    return random.choice([32, 64, 128, 255])

def random_window():
    return random.choice([8192, 16384, 32768, 65535])

def random_seq():
    return random.randint(0, 4294967295)

def random_ack():
    return random.randint(0, 4294967295)

def craft_ip_header(src, dst, proto=6, ttl=None):
    if ttl is None:
        ttl = random_ttl()
    ver_ihl = 0x45
    total_length = 40
    ident = random.randint(0, 65535)
    flags_offset = 0
    checksum = 0
    src_parts = [int(x) for x in src.split(".")]
    dst_parts = [int(x) for x in dst.split(".")]
    header = struct.pack("!BBHHHBBH4s4s",
        ver_ihl, 0, total_length, ident, flags_offset,
        ttl, proto, checksum,
        bytes(src_parts), bytes(dst_parts))
    return header

def craft_tcp_syn(src_port, dst_port, seq=None, window=None):
    if seq is None:
        seq = random_seq()
    if window is None:
        window = random_window()
    data_offset = 0x50
    flags = 0x02
    checksum = 0
    urgent = 0
    return struct.pack("!HHIIBBHHH",
        src_port, dst_port, seq, 0,
        data_offset, flags, window, checksum, urgent)
