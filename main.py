from modules import check_route, resolve_chain, analyze_packet
from modules import encrypt_payload, generate_keypair
from modules import random_mac, random_ttl, craft_ip_header, craft_tcp_syn
from modules import ProxyPool, ProxyChecker
from utils import AttackLogger, LogLevel, ConfigLoader, load_default_profile
from core import AttackEngine, PacketBuilder, ConnectionHandler, SessionManager
import os
import sys
import time
import random
import threading
import msvcrt
import ctypes
import socket

os.system("title Purple Storm v2.1")
os.system("mode con cols=100 lines=40")

PURPLE = "\033[35m"
MAGENTA = "\033[95m"
PINK = "\033[38;5;213m"
LAVENDER = "\033[38;5;183m"
WHITE = "\033[97m"
DIM = "\033[38;5;60m"
BOLD = "\033[1m"
RESET = "\033[0m"

def set_color(c):
    if sys.stdout.isatty():
        print(c, end="")

def clear():
    os.system("cls" if os.name == "nt" else "clear")

PURPLE = "\033[95m"
MAGENTA = "\033[35m"
PINK = "\033[38;5;213m"
RESET = "\033[0m"
WHITE = "\033[97m"
BOLD = "\033[1m"


LOGO = f""" {PURPLE}
███████████ ██████   ██████ ███████████     ██████████   ██████████      ███████     █████████ 
░░███░░░░░░█░░██████ ██████ ░░███░░░░░███   ░░███░░░░███ ░░███░░░░███   ███░░░░░███  ███░░░░░███
 ░███   █ ░  ░███░█████░███  ░███    ░███    ░███   ░░███ ░███   ░░███ ███     ░░███░███    ░░░ 
 ░███████    ░███░░███ ░███  ░██████████     ░███    ░███ ░███    ░███░███      ░███░░█████████ 
 ░███░░░█    ░███ ░░░  ░███  ░███░░░░░░      ░███    ░███ ░███    ░███░███      ░███ ░░░░░░░░███
 ░███  ░     ░███      ░███  ░███            ░███    ███  ░███    ███ ░░███     ███  ███    ░███
 █████       █████     █████ █████           ██████████   ██████████   ░░░███████░  ░░█████████ 
░░░░░       ░░░░░     ░░░░░ ░░░░░           ░░░░░░░░░░   ░░░░░░░░░░      ░░░░░░░     ░░░░░░░░░  
{RESET}
"""

print(LOGO)


METHODS = [
    ("UDP_FLOOD",  "Layer 4  |  UDP flood attack"),
    ("SYN_FLOOD",  "Layer 4  |  SYN packet flood"),
    ("HTTP_GET",   "Layer 7  |  HTTP GET flood"),
    ("AMP_DNS",    "Layer 4  |  DNS amplification"),
    ("SLOWLORIS",  "Layer 7  |  Slowloris attack"),
    ("NTP_AMP",    "Layer 4  |  NTP amplification"),
    ("ICMP_FLOOD", "Layer 3  |  ICMP echo flood"),
    ("BRUTE_FORCE","Layer 7  |  Brute force login"),
]

STATUS = ["ELITE", "ANONYMOUS", "HIGH", "STABLE", "FAST", "OK", "ACTIVE", "TIMEOUT", "UNREACHABLE", "DOWN"]
ERRORS = ["OK", "OK", "OK", "Connected", "Responding", "Ready", "Stable",
          "No response", "Connection lost", "Unreachable"]
COUNTRIES = ["RU", "UA", "CN", "US", "DE", "NL", "BR", "IN", "KR", "GB", "FR", "PL"]
ISPS = ["Rostelecom", "Comcast", "Deutsche Telekom", "China Telecom",
        "Verizon", "Level3", "Cogent", "Telia", "GTT", "Hurricane Electric"]

STOP_ATTACK = False

def animate_bar(seq, color, msg, delay=0.15):
    w = 40
    for i in range(w + 1):
        pct = int(i / w * 100)
        fill = "█" * i
        rem = "░" * (w - i)
        print(f"\r{color}{fill}{DIM}{rem} {WHITE}{pct}%{RESET}  ", end="")
        time.sleep(delay)
    print(f"\r{color}{'█' * w} {WHITE}100%{RESET}")
    print(f" {PURPLE}>{RESET} {msg}")

def loading_spinner(duration, msg):
    chars = "|/-\\"
    end = time.time() + duration
    i = 0
    while time.time() < end:
        print(f"\r{LAVENDER}{chars[i % len(chars)]}{RESET} {msg}...", end="")
        time.sleep(0.08)
        i += 1
    print(f"\r{PURPLE}[+]{RESET} {msg}")

def connecting():
    clear()
    set_color(PURPLE)
    print(LOGO)
    print()
    animate_bar(1, MAGENTA, f"{PURPLE}Connection established", 0.06)
    loading_spinner(1.2, f"{WHITE}Loading modules")
    loading_spinner(0.5, f"{WHITE}Initializing engine")
    loading_spinner(0.4, f"{WHITE}Syncing payloads")
    print(f"\n{PURPLE}╔{'═' * 50}╗{RESET}")
    print(f"{PURPLE}║{RESET}  {WHITE}{BOLD}SYSTEM READY{RESET}  |  All systems operational  {PURPLE}║{RESET}")
    print(f"{PURPLE}╚{'═' * 50}╝{RESET}")
    time.sleep(0.8)
    log = AttackLogger()
    log.log("Session initialized")
    config = ConfigLoader()
    config.load()
    profile = load_default_profile()
    print(f"\n{PURPLE}[+]{RESET} Profile: {profile.name}")
    time.sleep(0.3)

def show_menu():
    clear()
    set_color(PURPLE)
    print(LOGO)
    set_color(MAGENTA)
    print(f"  ╔{'═' * 55}╗")
    print(f"  ║{RESET}  {WHITE}{BOLD}ATTACK METHODS{RESET}{MAGENTA}  ║")
    print(f"  ╚{'═' * 55}╝{RESET}")
    print()
    for i, (cmd, desc) in enumerate(METHODS, 1):
        print(f"    {PURPLE}[{BOLD}{i:2d}{RESET}{PURPLE}]{RESET}  {PINK}{cmd:12}{RESET}  {DIM}│{RESET}  {LAVENDER}{desc}{RESET}")
    print()
    print(f"    {PURPLE}[{BOLD} 0{RESET}{PURPLE}]{RESET}  {MAGENTA}EXIT{RESET}")
    print()
    set_color(DIM)
    print(f"  {'─' * 55}")
    set_color(WHITE)

def generate_ip():
    return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"

def generate_proxy():
    ip = generate_ip()
    port = random.choice([80, 443, 8080, 3128, 1080, 8888, 9999, 53, 8443, 3127])
    country = random.choice(COUNTRIES)
    isp = random.choice(ISPS)
    status = random.choice(STATUS)
    err = random.choice(ERRORS)
    good = status in ("ELITE", "ANONYMOUS", "HIGH", "STABLE", "FAST", "OK", "ACTIVE")
    return f"{ip:>15}:{port:<5} {country:4} {isp:18} {status:10} {err}", good

def attack_screen(method_name, target):
    global STOP_ATTACK
    STOP_ATTACK = False
    port = random.randint(1, 65535)
    threads = random.randint(200, 999)
    duration = random.randint(999, 99999)

    clear()
    set_color(PURPLE)
    print(LOGO)
    print()
    set_color(MAGENTA)
    print(f"  ╔{'═' * 60}╗")
    print(f"  ║{RESET}  {WHITE}{BOLD}ATTACK IN PROGRESS{RESET}{MAGENTA}  ║")
    print(f"  ╚{'═' * 60}╝{RESET}")
    print()
    print(f"    {PINK}TARGET{RESET}   {DIM}:{RESET}  {LAVENDER}{target}:{port}{RESET}")
    print(f"    {PINK}METHOD{RESET}   {DIM}:{RESET}  {LAVENDER}{method_name}{RESET}")
    print(f"    {PINK}THREADS{RESET}  {DIM}:{RESET}  {LAVENDER}{threads}{RESET}")
    print(f"    {PINK}TIMEOUT{RESET}  {DIM}:{RESET}  {LAVENDER}{duration}s{RESET}")
    print()
    set_color(DIM)
    print(f"  ╔{'═' * 60}╗")
    print(f"  ║{RESET}  {'PROXY':18}  {'COUNTRY':4}  {'ISP':18}  {'STATUS':10}  {'ERROR'}")
    print(f"  ║{'═' * 60}║")
    set_color(WHITE)

    start = time.time()
    sent_total = 0

    while not STOP_ATTACK:
        for _ in range(random.randint(3, 12)):
            proxy, good = generate_proxy()
            elapsed = time.time() - start
            sent_total += random.randint(10000, 99999)
            set_color(PURPLE if good else MAGENTA)
            print(f"  {proxy}")
        mb = sent_total * 64 / 1024 / 1024
        speed = mb / elapsed if elapsed > 0 else 0
        stats = f"{PURPLE}[*]{RESET} PKTS: {sent_total:<8}  SPEED: {speed:.1f} MB/s  TIME: {elapsed:.1f}s"
        set_color(DIM)
        print(f"  {'─' * 40}")
        print(f"  {stats}{RESET}")
        set_color(WHITE)
        time.sleep(random.uniform(0.1, 0.2))
        if msvcrt.kbhit() and msvcrt.getch() == b'\x1b':
            break

def main():
    ctypes.windll.kernel32.SetConsoleTitleW("Purple Storm v2.1")
    connecting()

    while True:
        show_menu()
        print()
        try:
            choice = input(f"  {PINK}>>{RESET} Select method > ").strip()
            if choice == "0":
                clear()
                set_color(PURPLE)
                print(LOGO)
                print()
                animate_bar(1, MAGENTA, f"{WHITE}Shutting down systems...", 0.04)
                loading_spinner(0.3, f"{WHITE}Cleaning up")
                loading_spinner(0.3, f"{WHITE}Closing connections")
                print(f"\n  {MAGENTA}Goodbye.{RESET}")
                time.sleep(1)
                sys.exit(0)
            idx = int(choice) - 1
            if 0 <= idx < len(METHODS):
                cmd, desc = METHODS[idx]
                print()
                target = input(f"  {PINK}>>{RESET} Enter target IP/domain > ").strip()
                if not target:
                    print(f"\n  {MAGENTA}[!] Invalid target{RESET}")
                    time.sleep(1)
                    continue
                print(f"\n  {PURPLE}[>]{RESET} Resolving {LAVENDER}{target}{RESET}...")
                time.sleep(0.6)
                clean = target.replace("https://", "").replace("http://", "").split("/")[0]
                valid = False
                try:
                    ip = socket.gethostbyname(clean)
                    print(f"  {PURPLE}[>]{RESET} {clean} {DIM}->{RESET} {LAVENDER}{ip}")
                    print(f"  {PURPLE}[+]{RESET} Target resolved")
                    route = check_route(ip)
                    print(f"  {PURPLE}[>]{RESET} Route: {len(route)} hops")
                    valid = True
                except:
                    parts = target.split(".")
                    if len(parts) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in parts):
                        print(f"  {PURPLE}[+]{RESET} Direct IP: {target}")
                        valid = True
                    else:
                        print(f"\n  {MAGENTA}[!] Target not found{RESET}")
                if not valid:
                    time.sleep(1)
                    continue
                print(f"\n  {DIM}{'─' * 50}{RESET}")
                loading_spinner(0.5, f"{WHITE}Spawning {random.randint(200, 999)} threads")
                loading_spinner(0.6, f"{WHITE}Scanning proxy pool")
                print(f"  {PURPLE}[+]{RESET} {random.randint(20, 80)} proxies online")
                loading_spinner(0.3, f"{WHITE}Encrypting payload")
                print(f"  {PURPLE}[+]{RESET} Key exchange complete")
                print()
                print(f"  {MAGENTA}{BOLD}[ ATTACK LAUNCHED ]{RESET}")
                print(f"  {DIM}Press ESC to stop{RESET}")
                print()
                time.sleep(0.5)
                attack_screen(cmd, target)
            else:
                print(f"\n  {MAGENTA}[!] Invalid choice{RESET}")
                time.sleep(1)
        except ValueError:
            print(f"\n  {MAGENTA}[!] Invalid input{RESET}")
            time.sleep(1)

if __name__ == "__main__":
    main()
