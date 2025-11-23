#!/usr/bin/env python3
"""
WAHO automation tool
- DATA token login -> extracts AUTH token and saves both
- Auto-validate / auto-refresh auth token
- Show accounts
- Claim eligible accounts (online >= 24h)
- Lucky draw status
- Lucky draw auto-spin
- Menu + colored output
Requires: requests, colorama
Install: pip install requests colorama
"""

import os
import json
import time
import random
import re
import shutil
import requests
from colorama import Fore, Style, init

# Config
TOKEN_FILE = "token.json"
init(autoreset=True)

C_ACC   = Fore.MAGENTA
C_QR    = Fore.CYAN
C_MONEY = Fore.GREEN
C_TIME  = Fore.YELLOW
C_OK    = Fore.GREEN
C_BAD   = Fore.RED
C_INFO  = Fore.CYAN
RESET   = Style.RESET_ALL

# Helpers / banner
def banner():
    os.system("clear")
    print(Fore.RED + " █████╗ ███╗   ███╗ █████╗ ███╗   ██╗")
    print(Fore.RED + "██╔══██╗████╗ ████║██╔══██╗████╗  ██║")
    print(Fore.RED + "███████║██╔████╔██║███████║██╔██╗ ██║")
    print(Fore.RED + "██╔══██║██║╚██╔╝██║██╔══██║██║╚██╗██║")
    print(Fore.RED + "██║  ██║██║ ╚═╝ ██║██║  ██║██║ ╚████║")
    print(Fore.LIGHTBLACK_EX + "╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝")
    print(C_INFO + "[!] This script is created for auto-claiming WAHO" + RESET)
    print()

def human_sleep(seconds):
    # simple human-like wait with dot animation
    for _ in range(seconds):
        print(".", end="", flush=True)
        time.sleep(1)
    print()

# Network / IP
def get_ip():
    try:
        r = requests.get("https://api.ipify.org/?format=json", timeout=6)
        j = r.json()
        return j.get("ip")
    except:
        return "0.0.0.0"

IP = get_ip()

# Request headers
DEFAULT_HEADERS = {
    "Host": "api.waho.pro",
    "accept": "application/json, text/plain, */*",
    "user-agent": "Mozilla/5.0 (Linux; Android 7.1.2; Pixel Build/NHG47O)",
    "content-type": "text/plain",
    "origin": "https://waho.pro",
    "x-requested-with": "mark.via",
    "sec-fetch-site": "same-site",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://waho.pro/wechatListTemp",
    "accept-encoding": "gzip, deflate",
    "accept-language": "en,en-US;q=0.9"
}

# Token file handling
def save_tokens(auth_token=None, data_token=None):
    data = {}
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, "r") as f:
                data = json.load(f)
        except:
            data = {}
    if auth_token:
        data["auth_token"] = auth_token
    if data_token:
        data["data_token"] = data_token
    with open(TOKEN_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_tokens():
    if not os.path.exists(TOKEN_FILE):
        return None, None
    try:
        with open(TOKEN_FILE, "r") as f:
            data = json.load(f)
            return data.get("auth_token"), data.get("data_token")
    except:
        return None, None

# Login / validation
def login_with_data_token(data_token):
    """
    Login using DATA token (long string). Save auth and data tokens.
    """
    url = f"https://api.waho.pro/login/login?ip={IP}"
    headers = DEFAULT_HEADERS.copy()
    headers.update({"referer": "https://waho.pro/login"})
    payload = json.dumps({"data": data_token})
    try:
        r = requests.post(url, headers=headers, data=payload, timeout=10)
        j = r.json()
    except Exception as e:
        print(C_BAD + f"[!] Login request failed: {e}" + RESET)
        return None
    if j.get("code") != 0:
        print(C_BAD + f"[!] Login failed: {j.get('msg', 'unknown')}" + RESET)
        return None
    auth_token = j["data"].get("token")
    uid = j["data"].get("uid")
    if auth_token:
        save_tokens(auth_token=auth_token, data_token=data_token)
        print(C_OK + f"[+] Login OK — uid: {uid}. Auth token saved." + RESET)
        return auth_token
    else:
        print(C_BAD + "[!] Login responded but no token found." + RESET)
        return None

def load_or_obtain_tokens():
    auth, data = load_tokens()
    if auth:
        return auth
    print(C_INFO + "No saved auth token found. Paste your WAHO DATA token (the long string):" + RESET)
    data_token = input("> ").strip()
    return login_with_data_token(data_token)

def get_info(auth_token):
    url = f"https://api.waho.pro/member/index?token={auth_token}&ip={IP}"
    try:
        r = requests.post(url, headers=DEFAULT_HEADERS, data='{"httpRequestIndex":0,"httpRequestCount":0}', timeout=10)
        j = r.json()
    except Exception as e:
        raise RuntimeError(f"Request failed: {e}")
    if j.get("code") != 0:
        raise RuntimeError(f"Invalid token or error: {j.get('msg')}")
    data = j.get("data", {})
    user_key = data.get("user_key", "")
    today_commission = data.get("today_commission", 0)
    total_balance = data.get("money", 0)
    return user_key, today_commission, total_balance

def validate_auth_token(auth_token):
    """
    Validate auth token; if invalid, attempt auto re-login with saved DATA token,
    otherwise ask user to paste DATA token and login.
    """
    try:
        get_info(auth_token)
        return auth_token
    except Exception as e:
        print(C_BAD + "[!] Saved AUTH token invalid or expired: " + str(e) + RESET)
    # try auto re-login with saved data token
    _, saved_data = load_tokens()
    if saved_data:
        print(C_INFO + "[*] Attempting auto re-login with saved DATA token..." + RESET)
        new_auth = login_with_data_token(saved_data)
        if new_auth:
            return new_auth
        print(C_BAD + "[!] Auto re-login failed." + RESET)
    # ask user for DATA token
    print(C_INFO + "Please paste your DATA token to re-login (the long encoded string):" + RESET)
    data_token = input("> ").strip()
    return login_with_data_token(data_token)

# Accounts / claim
def parse_online_time_to_hours(online_time_str):
    if not online_time_str:
        return 0
    s = str(online_time_str)
    days = 0
    hours = 0
    m = re.search(r"(\d+)\s*天", s)
    if m:
        days = int(m.group(1))
    m2 = re.search(r"(\d+)\s*小时", s)
    if m2:
        hours = int(m2.group(1))
    if days == 0 and hours == 0:
        m3 = re.search(r"(\d+)\s*h", s, re.I)
        if m3:
            hours = int(m3.group(1))
    total_hours = days * 24 + hours
    return total_hours

def get_account_list(auth_token):
    url = f"https://api.waho.pro//newlogin/getwxlist?token={auth_token}&ip={IP}"
    data = '{"page":1,"limit":1000,"httpRequestIndex":0,"httpRequestCount":0}'
    try:
        r = requests.post(url, headers=DEFAULT_HEADERS, data=data, timeout=12)
        j = r.json()
    except Exception as e:
        print(C_BAD + f"[!] Failed to fetch accounts: {e}" + RESET)
        return []
    if j.get("code") != 0:
        print(C_BAD + f"[!] Error fetching accounts: {j.get('msg')}" + RESET)
        return []
    items = j.get("data", {}).get("list", [])
    return items

def show_accounts(auth_token):
    items = get_account_list(auth_token)
    if not items:
        print(C_BAD + "[!] No accounts found or failed to fetch." + RESET)
        return
    width = shutil.get_terminal_size().columns
    line = "-" * width
    for idx, it in enumerate(items, start=1):
        print(f"[{idx}]")
        print(f"{C_ACC}ACCOUNT:      {it.get('account','')}{RESET}")
        print(f"{C_QR}QR ID:        {it.get('qr_id','')}{RESET}")
        print(f"{C_MONEY}MONEY:        {it.get('money','')}{RESET}")
        print(f"{C_TIME}ONLINE TIME:  {it.get('online_time','')}{RESET}")
        print(line)

def claim_eligible_accounts(auth_token):
    items = get_account_list(auth_token)
    if not items:
        print(C_BAD + "[!] No accounts to claim." + RESET)
        return
    for it in items:
        account_name = it.get("account", "UNKNOWN")
        qr_id = it.get("qr_id")
        online_time = it.get("online_time", "")
        hours = online_time
        if hours < 24:
            print(f"{C_BAD}[SKIP] {account_name} — Online {hours}h (<24h){RESET}")
            continue
        claim_url = f"https://api.waho.pro/Activity/ClaimOnlineRewards?token={auth_token}&ip={IP}"
        payload = json.dumps({"qr_id": qr_id, "httpRequestIndex": 0, "httpRequestCount": 0})
        try:
            r = requests.post(claim_url, headers=DEFAULT_HEADERS, data=payload, timeout=12)
            j = r.json()
        except Exception as e:
            print(C_BAD + f"[FAILED] {account_name} — request error: {e}" + RESET)
            continue
        if j.get("code") == 0:
            amount = j.get("data", {}).get("Amount")
            print(C_OK + f"[CLAIMED] {account_name} → +{amount} 💵" + RESET)
        else:
            print(C_BAD + f"[FAILED] {account_name} → {j.get('msg', 'Unknown')}" + RESET)
        wait = random.randint(3, 6)
        human_sleep(wait)
    print(C_OK + "\nAll done.\n" + RESET)

# Lucky draw status
def lucky_draw_status(auth_token):
    url = f"https://api.waho.pro/Activity/LuckyDrawNum?token={auth_token}&ip={IP}"
    payload = json.dumps({"httpRequestIndex": 0, "httpRequestCount": 0})
    headers = DEFAULT_HEADERS.copy()
    headers.update({"referer": "https://waho.pro/spin"})
    try:
        r = requests.post(url, headers=headers, data=payload, timeout=10)
        j = r.json()
    except Exception as e:
        print(C_BAD + f"[!] Lucky Draw request failed: {e}" + RESET)
        return
    if j.get("code") != 0:
        print(C_BAD + f"[!] Lucky Draw error: {j.get('msg')}" + RESET)
        return
    data = j.get("data", {})
    spins_left = data.get("lucky_draw_num", 0)
    earned_money = data.get("lucky_draw_money", 0)
    print()
    print(" LUCKY DRAW STATUS ".center(40, "="))
    print(f"{C_INFO}Spins Left: {spins_left}{RESET}")
    print(f"{C_MONEY}Total Lucky Money Earned: {earned_money}{RESET}")
    print("=" * 40)
    print()

# Lucky draw auto-spin
def lucky_draw_auto(auth_token):
    print()
    print(" AUTO LUCKY DRAW ".center(40, "="))
    url_info = f"https://api.waho.pro/Activity/LuckyDrawNum?token={auth_token}&ip={IP}"
    payload = json.dumps({"httpRequestIndex": 0, "httpRequestCount": 0})
    headers = DEFAULT_HEADERS.copy()
    headers.update({"referer": "https://waho.pro/spin"})
    try:
        r = requests.post(url_info, headers=headers, data=payload, timeout=10)
        j = r.json()
    except Exception as e:
        print(C_BAD + f"[!] Failed to fetch lucky draw count: {e}" + RESET)
        return
    if j.get("code") != 0:
        print(C_BAD + f"[!] Error: {j.get('msg')}" + RESET)
        return
    spins_left = j.get("data", {}).get("lucky_draw_num", 0)
    total_money = 0.0
    print(C_INFO + f"Spins Available: {spins_left}" + RESET)
    print("=" * 40)
    if spins_left <= 0:
        print(C_BAD + "[!] No spins available." + RESET)
        return
    spin_url = f"https://api.waho.pro/Activity/LuckyDraw?token={auth_token}&ip={IP}"
    for i in range(spins_left):
        print(C_INFO + f"🎰 Spin {i+1}/{spins_left} ..." + RESET)
        try:
            r2 = requests.post(spin_url, headers=headers, data=payload, timeout=12)
            j2 = r2.json()
#            print(j2)
        except Exception as e:
            print(C_BAD + f"[!] Spin error: {e}" + RESET)
            break
        if j2.get("code") != 0:
            print(C_BAD + f"[FAILED] {j2.get('msg', 'Unknown error')}" + RESET)
            break
        amount = j2.get("data", {}).get("lucky_draw_money", 0)
        cur_num = j2.get("data", {}).get("cur_num", 0)
        total_money += amount
        print(C_OK + f"→ Reward: +{amount} 💵 | Remaining Spins: {int(spins_left)-int(i)}" + RESET)
        human_sleep(random.randint(5, 6))
    print()
    print("=" * 40)
    print(C_OK + f"TOTAL SPIN REWARD: +{total_money} 💵" + RESET)
    print("=" * 40)
    print()

# Menu
def update_data_token_interactive():
    print(C_INFO + "Paste your WAHO DATA token (long string) to login and save:" + RESET)
    dt = input("> ").strip()
    if not dt:
        print(C_BAD + "No input. Aborting." + RESET)
        return None
    auth = login_with_data_token(dt)
    if auth:
        print(C_OK + "Saved new DATA & AUTH tokens." + RESET)
    return auth

def menu_loop():
    while True:
        banner()
        saved_auth, saved_data = load_tokens()
        if not saved_auth:
            auth = load_or_obtain_tokens()
        else:
            auth = validate_auth_token(saved_auth)
        if not auth:
            print(C_BAD + "[!] Unable to obtain a valid auth token. Use option 5 to provide DATA token." + RESET)
        if auth:
            try:
                user_key, today_commission, total_balance = get_info(auth)
                width = shutil.get_terminal_size().columns
                print(" USER INFO ".center(width, "="))
                print(f"{C_ACC}USER IP: {IP}{RESET}")
                print(f"{C_ACC}LOGIN ACCOUNT: {user_key}{RESET}")
                print(f"{C_ACC}Today Commission: {today_commission}{RESET}")
                print(f"{C_ACC}Total balance: {total_balance}{RESET}")
            except Exception as e:
                print(C_BAD + f"[!] Could not fetch user info: {e}" + RESET)
        print()
        print(" WAHO TOOL MENU ".center(40, "="))
        print(f"{C_ACC}1. Show all accounts{RESET}")
        print(f"{C_ACC}2. Claim all eligible accounts (>24h){RESET}")
        print(f"{C_ACC}3. Lucky Draw Status{RESET}")
        print(f"{C_ACC}4. Lucky Draw Auto Spin{RESET}")
        print(f"{C_ACC}5. Update / Add DATA token (login){RESET}")
        print(f"{C_ACC}6. Exit{RESET}")
        choice = input("\nENTER YOUR CHOICE → ").strip()
        if choice == "1":
            if auth:
                show_accounts(auth)
            else:
                print(C_BAD + "No valid auth token. Please update DATA token (option 5)." + RESET)
            input("\nPress ENTER to return to menu...")
        elif choice == "2":
            if auth:
                claim_eligible_accounts(auth)
            else:
                print(C_BAD + "No valid auth token. Please update DATA token (option 5)." + RESET)
            input("\nPress ENTER to return to menu...")
        elif choice == "3":
            if auth:
                lucky_draw_status(auth)
            else:
                print(C_BAD + "No valid auth token. Please update DATA token (option 5)." + RESET)
            input("\nPress ENTER to return to menu...")
        elif choice == "4":
            if auth:
                lucky_draw_auto(auth)
            else:
                print(C_BAD + "No valid auth token. Please update DATA token (option 5)." + RESET)
            input("\nPress ENTER to return to menu...")
        elif choice == "5":
            new_auth = update_data_token_interactive()
            if new_auth:
                auth = new_auth
            input("\nPress ENTER to return to menu...")
        elif choice == "6":
            print(C_INFO + "Bye." + RESET)
            break
        else:
            print(C_BAD + "Invalid input." + RESET)
            time.sleep(1)

if __name__ == "__main__":
    try:
        menu_loop()
    except KeyboardInterrupt:
        print("\n" + C_INFO + "Interrupted. Exiting..." + RESET)
