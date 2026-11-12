#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HOZOO MD - Facebook Mass Report Tool (CLI Menu v4 + Banner ASCII Baru)
Auto report dengan cookie + proxy rotator + menu interaktif + banner ASCII baru
"""

import os
import sys
import json
import time
import random
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from concurrent.futures import ThreadPoolExecutor, as_completed

# ================= CONFIG =================

DEFAULT_COOKIES = os.getenv("AKUNAKTOFADABERPAA", None) or (
    "datr=KIn1ammqoLrUtAw7xbLV4OuH;"
    "fr=03VuSmpLKqHa35R0C.AWfKYBlZ_sUZBT8dpGegG3h-g3gQjQSZ5BybIdDD1eCoi7KiIMo.Bq9Yku..AAA.0.0.Bq9Yn0.AWf9GcNBMnAFdwWGdOgSXdj2XjQ;"
    "vpd=v1%3B808x450x2.4;"
    "xs=29%3APXtL6Vh8xap81Q%3A2%3A1794476532%3A-1%3A-1;"
    "fbl_st=101418592%3BT%3A29907942;"
    "locale=id_ID;"
    "m_pixel_ratio=1;"
    "c_user=61581757974778;"
    "pas=61581757974778%3Aei6KXBH5Og;"
    "sb=LYn1aor2mVuG0-eQpTcyUAim;"
    "wd=450x975;"
    "wl_cbv=v2%3Bclient_version%3A3355%3Btimestamp%3A1794476546"
)

REPORT_TYPES = [
    "fake_account", "hate_speech", "harassment", "spam", "scam",
    "violence", "nudity", "terrorism", "self_harm", "drugs",
    "weapons", "intellectual_property", "identity_theft", "bullying",
]

GRAPHQL_URL = "https://www.facebook.com/api/graphql/"

BASE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-A536E) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://www.facebook.com",
    "Referer": "https://www.facebook.com/",
    "X-Requested-With": "XMLHttpRequest",
}

# ================= BANNER WARNA =================

class Warna:
    BIRU    = "\033[94m"
    BIRU_MUDA = "\033[96m"
    PUTIH   = "\033[97m"
    KUNING  = "\033[93m"
    HIJAU   = "\033[92m"
    MERAH   = "\033[91m"
    UNGU    = "\033[95m"
    RESET   = "\033[0m"
    TEBAL   = "\033[1m"

def banner():
    """Tampilkan banner dengan ASCII art baru."""
    b = Warna.BIRU + Warna.TEBAL
    p = Warna.PUTIH
    r = Warna.RESET
    k = Warna.KUNING
    h = Warna.HIJAU
    m = Warna.MERAH

    print(b + "=" * 65 + r)
    print(b + "                     " + p + "FACEBOOK" + r + b + " MASS REPORT TOOL" + r)
    print(b + "=" * 65 + r)
    print()
    # ASCII art baru dari user
    art = [
        "⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷",
        "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
        "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠋⠉⠉⠉⠉⢻⣿⣿⣿⣿",
        "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿",
        "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⢀⣴⣶⣶⣶⣿⣿⣿⣿⣿",
        "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿",
        "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿",
        "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿",
        "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿",
        "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠂⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿",
        "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿",
        "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿",
        "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿",
        "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿",
        "⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⠿",
    ]
    for line in art:
        print(b + line + r)
    print()
    print(h + "            ╔══════════════════════════════════════╗" + r)
    print(h + "            ║ " + Warna.PUTIH + Warna.TEBAL + "  HOZOO MD  " + Warna.HIJAU + "// " + Warna.KUNING + "MASS REPORT  " + Warna.HIJAU + " ║" + r)
    print(h + "            ╚══════════════════════════════════════╝" + r)
    print()
    print(m + "     ═══════════════════════════════════════════════════════" + r)
    print(m + "        Powered by: " + Warna.PUTIH + Warna.TEBAL + "DGXEONHOZOOMD"+ r)
    print(m + "        Status: " + Warna.HIJAU + "AKTIF" + Warna.MERAH + " | " + Warna.PUTIH + "Filter: OFF" + r)
    print(m + "     ═══════════════════════════════════════════════════════" + r)
    print()

# ================= PROXY MANAGER =================

class ProxyManager:
    def __init__(self, filepath="proxies.txt"):
        self.filepath = filepath
        self.proxies = []
        self._load()

    def _load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    self.proxies.append(line)
        if not self.proxies:
            print(Warna.KUNING + "[!] proxies.txt kosong atau ga ada. Jalan tanpa proxy (raw IP)." + Warna.RESET)
        else:
            print(Warna.HIJAU + f"[+] Loaded {len(self.proxies)} proxy." + Warna.RESET)

    def get(self):
        if not self.proxies:
            return None
        p = random.choice(self.proxies)
        if "@" not in p and p.count(":") == 1:
            return {"http": f"http://{p}", "https": f"http://{p}"}
        elif "@" not in p and p.count(":") == 3:
            ip, port, user, pw = p.split(":")
            return {"http": f"http://{user}:{pw}@{ip}:{port}",
                    "https": f"http://{user}:{pw}@{ip}:{port}"}
        return {"http": f"http://{p}", "https": f"http://{p}"}


# ================= SESSION BUILDER =================

def build_session(proxy_dict=None):
    s = requests.Session()
    retry = Retry(total=3, backoff_factor=0.5,
                  status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry, pool_connections=20, pool_maxsize=20)
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    s.headers.update(BASE_HEADERS)
    s.headers["Cookie"] = DEFAULT_COOKIES
    if proxy_dict:
        s.proxies.update(proxy_dict)
    return s


# ================= REPORT CORE =================

def generate_report_payload(target_id, report_type):
    variables = {
        "input": {
            "actor_id": None,
            "client_mutation_id": str(random.randint(1000000000, 9999999999)),
            "object_id": target_id,
            "report_type": report_type,
            "source": "profile",
            "reason": report_type,
        }
    }
    return {
        "av": "61581757974778",
        "fb_api_caller_class": "RelayModern",
        "fb_api_req_friendly_name": "CometReportUserMutation",
        "variables": json.dumps(variables),
        "doc_id": "29812345678901234",
    }


def send_report(session, target_id, report_type):
    payload = generate_report_payload(target_id, report_type)
    try:
        r = session.post(GRAPHQL_URL, data=payload, timeout=15)
        if r.status_code == 200 and ('"success":true' in r.text or 'report' in r.text.lower()):
            return True
        return False
    except requests.RequestException:
        return False


# ================= WORKER =================

def worker(worker_id, target_id, proxy_mgr, max_attempts=None):
    attempt = 0
    sukses = 0
    gagal = 0
    proxy_dict = proxy_mgr.get()
    session = build_session(proxy_dict)
    while True:
        if max_attempts and attempt >= max_attempts:
            break
        report_type = random.choice(REPORT_TYPES)
        ok = send_report(session, target_id, report_type)
        attempt += 1
        if ok:
            sukses += 1
            print(Warna.HIJAU + f"[Worker-{worker_id}] ✅ sukses ({report_type}) ke {target_id} | total: {sukses}" + Warna.RESET)
        else:
            gagal += 1
            print(Warna.MERAH + f"[Worker-{worker_id}] ❌ gagal ({report_type}) - rotate proxy..." + Warna.RESET)
            proxy_dict = proxy_mgr.get()
            session = build_session(proxy_dict)
            time.sleep(random.uniform(1, 3))
        time.sleep(random.uniform(0.5, 2.0))


# ================= MENU & CLI =================

def garis():
    print(Warna.BIRU + "_" * 60 + Warna.RESET)

def tampilkan_menu():
    garis()
    print(Warna.PUTIH + Warna.TEBAL + "  HOZOO MD - Facebook Mass Report Tool v4" + Warna.RESET)
    print(Warna.KUNING + "  Status Akun: " + Warna.PUTIH + "${AKUNAKTOFADABERPAA}" + Warna.RESET)
    print(Warna.KUNING + "  Cookie User: " + Warna.PUTIH +
          (DEFAULT_COOKIES.split("c_user=")[1].split(";")[0]
           if "c_user=" in DEFAULT_COOKIES else "Tidak Terdeteksi") + Warna.RESET)
    garis()
    print(Warna.BIRU_MUDA + "  [1]" + Warna.PUTIH + " Masukkan Facebook ID Target (manual)" + Warna.RESET)
    print(Warna.BIRU_MUDA + "  [2]" + Warna.PUTIH + " Muat Target dari targets.txt" + Warna.RESET)
    print(Warna.BIRU_MUDA + "  [3]" + Warna.PUTIH + " Pilih Jenis Laporan (1 jenis atau random)" + Warna.RESET)
    print(Warna.BIRU_MUDA + "  [4]" + Warna.PUTIH + " Random Report Tanpa Berhenti (infinite)" + Warna.RESET)
    print(Warna.BIRU_MUDA + "  [5]" + Warna.PUTIH + " Set Thread (default 10)" + Warna.RESET)
    print(Warna.BIRU_MUDA + "  [6]" + Warna.PUTIH + " Tampilkan Proxy Aktif" + Warna.RESET)
    print(Warna.MERAH + "  [7]" + Warna.PUTIH + " Keluar" + Warna.RESET)
    garis()


def input_id_manual():
    garis()
    raw = input(Warna.KUNING + "  Masukkan Facebook ID target (pisahkan koma jika banyak): " + Warna.RESET).strip()
    if not raw:
        print(Warna.MERAH + "[!] Tidak ada ID yang dimasukkan." + Warna.RESET)
        return []
    ids = [x.strip() for x in raw.split(",") if x.strip()]
    print(Warna.HIJAU + f"[+] {len(ids)} ID target siap di-report." + Warna.RESET)
    return ids


def pilih_jenis_laporan():
    garis()
    print(Warna.KUNING + "  Pilih jenis laporan:" + Warna.RESET)
    for i, rt in enumerate(REPORT_TYPES, 1):
        print(Warna.BIRU_MUDA + f"    [{i}]" + Warna.PUTIH + f" {rt}" + Warna.RESET)
    print(Warna.BIRU_MUDA + "    [0]" + Warna.PUTIH + " Random (campur semua)" + Warna.RESET)
    garis()
    pilihan = input(Warna.KUNING + "  Masukkan nomor (0 untuk random): " + Warna.RESET).strip()
    if pilihan == "0":
        return None
    try:
        idx = int(pilihan) - 1
        if 0 <= idx < len(REPORT_TYPES):
            return [REPORT_TYPES[idx]]
    except ValueError:
        pass
    print(Warna.MERAH + "[!] Pilihan tidak valid. Pakai random." + Warna.RESET)
    return None


def jalankan_report(target_ids, report_types, threads, infinite=False, max_attempts=0):
    proxy_mgr = ProxyManager("proxies.txt")
    garis()
    print(Warna.HIJAU + f"  Menjalankan report..." + Warna.RESET)
    print(Warna.PUTIH + f"  Target: {len(target_ids)} ID" + Warna.RESET)
    print(Warna.PUTIH + f"  Jenis Laporan: {'Random' if report_types is None else report_types}" + Warna.RESET)
    print(Warna.PUTIH + f"  Threads: {threads}" + Warna.RESET)
    print(Warna.PUTIH + f"  Mode: {'Infinite (tanpa berhenti)' if infinite else f'Max {max_attempts} percobaan'}" + Warna.RESET)
    garis()

    def worker_custom(worker_id, target_id):
        attempt = 0
        sukses = 0
        proxy_dict = proxy_mgr.get()
        session = build_session(proxy_dict)
        while True:
            if not infinite and max_attempts and attempt >= max_attempts:
                break
            if report_types:
                report_type = random.choice(report_types)
            else:
                report_type = random.choice(REPORT_TYPES)
            ok = send_report(session, target_id, report_type)
            attempt += 1
            if ok:
                sukses += 1
                print(Warna.HIJAU + f"[Worker-{worker_id}] ✅ sukses ({report_type}) ke {target_id} | total: {sukses}" + Warna.RESET)
            else:
                print(Warna.MERAH + f"[Worker-{worker_id}] ❌ gagal ({report_type}) - rotate proxy..." + Warna.RESET)
                proxy_dict = proxy_mgr.get()
                session = build_session(proxy_dict)
                time.sleep(random.uniform(1, 3))
            time.sleep(random.uniform(0.5, 2.0))

    with ThreadPoolExecutor(max_workers=threads) as ex:
        futures = []
        for i, tid in enumerate(target_ids):
            futures.append(ex.submit(worker_custom, i, tid))

        try:
            for fut in as_completed(futures):
                try:
                    fut.result()
                except KeyboardInterrupt:
                    print(Warna.MERAH + "\n[!] Dihentikan oleh user." + Warna.RESET)
                    sys.exit(0)
                except Exception as e:
                    print(Warna.MERAH + f"[!] Worker error: {e}" + Warna.RESET)
        except KeyboardInterrupt:
            print(Warna.MERAH + "\n[!] Dihentikan oleh user." + Warna.RESET)
            sys.exit(0)


def main():
    targets = []
    report_types = None
    threads = 10

    # Tampilkan banner warna di awal
    banner()

    while True:
        tampilkan_menu()
        pilihan = input(Warna.KUNING + "  Pilih menu > " + Warna.RESET).strip()

        if pilihan == "1":
            new_ids = input_id_manual()
            if new_ids:
                targets.extend(new_ids)

        elif pilihan == "2":
            if not os.path.exists("targets.txt"):
                print(Warna.MERAH + "[!] targets.txt tidak ada. Bikin dulu, isi 1 FB ID per baris." + Warna.RESET)
                continue
            with open("targets.txt", "r") as f:
                loaded = [line.strip() for line in f if line.strip()]
            targets.extend(loaded)
            print(Warna.HIJAU + f"[+] {len(loaded)} ID dimuat dari targets.txt. Total target: {len(targets)}" + Warna.RESET)

        elif pilihan == "3":
            report_types = pilih_jenis_laporan()
            print(Warna.HIJAU + f"[+] Jenis laporan diset: {'Random' if report_types is None else report_types}" + Warna.RESET)

        elif pilihan == "4":
            if not targets:
                print(Warna.MERAH + "[!] Belum ada target. Masukkan ID dulu (menu 1 atau 2)." + Warna.RESET)
                continue
            print(Warna.KUNING + "  Mode random report tanpa berhenti. Tekan Ctrl+C untuk stop." + Warna.RESET)
            jalankan_report(targets, report_types, threads, infinite=True)

        elif pilihan == "5":
            try:
                threads = int(input(Warna.KUNING + "  Jumlah thread > " + Warna.RESET).strip())
                if threads < 1:
                    raise ValueError
                print(Warna.HIJAU + f"[+] Thread diset: {threads}" + Warna.RESET)
            except ValueError:
                print(Warna.MERAH + "[!] Harus angka >= 1." + Warna.RESET)

        elif pilihan == "6":
            garis()
            pm = ProxyManager("proxies.txt")
            if pm.proxies:
                print(Warna.HIJAU + "  Proxy aktif:" + Warna.RESET)
                for p in pm.proxies[:10]:
                    print(Warna.PUTIH + f"    - {p}" + Warna.RESET)
                if len(pm.proxies) > 10:
                    print(Warna.PUTIH + f"    ... dan {len(pm.proxies)-10} lainnya" + Warna.RESET)
            else:
                print(Warna.MERAH + "  Tidak ada proxy." + Warna.RESET)
            garis()

        elif pilihan == "7":
            print(Warna.MERAH + Warna.TEBAL + "\nKeluar. HOZOO MD standby." + Warna.RESET)
            break

        else:
            print(Warna.MERAH + "[!] Menu tidak valid." + Warna.RESET)


if __name__ == "__main__":
    main()
