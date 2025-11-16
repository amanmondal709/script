import random
import shutil
import os
from colorama import Fore, Style, init
import json
import requests
import time
import re
red='\033[31m'
r='\033[31m'
b = '\033[31m'
y = '\033[31m'
g='\033[32m'
TOKEN_FILE = "token.json"
def banner():
	print('\033[31m' + '            ''█████'+'\033[90m'+'╗ '+'\033[90m'+''+'\033[31m'+'███'+'\033[90m'+'╗   '+'\033[90m'+''+'\033[31m'+'███'+'\033[90m'+'╗ '+'\033[90m'+''+'\033[31m'+'█████'+'\033[90m'+'╗ '+'\033[90m'+''+'\033[31m'+'███'+'\033[90m'+'╗   '+'\033[90m'+''+'\033[31m'+'██'+'\033[90m'+'╗')
	print('\033[31m' + '           ''██'+'\033[90m'+'╔══'+'\033[90m'+''+'\033[31m'+'██'+'\033[90m'+'╗'+'\033[90m'+''+'\033[31m'+'████'+'\033[90m'+'╗ '+'\033[90m'+''+'\033[31m'+'████'+'\033[90m'+'║'+'\033[90m'+''+'\033[31m'+'██'+'\033[90m'+'╔══'+'\033[90m'+''+'\033[31m'+'██'+'\033[90m'+'╗'+'\033[90m'+''+'\033[31m'+'████'+'\033[90m'+'╗  '+'\033[90m'+''+'\033[31m'+'██'+'\033[90m'+'║')
	print('\033[31m' + '           ''███████'+'\033[90m'+'║'+'\033[90m'+''+'\033[31m'+'██'+'\033[90m'+'╔'+'\033[90m'+''+'\033[31m'+'████'+'\033[90m'+'╔'+'\033[90m'+''+'\033[31m'+'██'+'\033[90m'+'║'+'\033[90m'+''+'\033[31m'+'███████'+'\033[90m'+'║'+'\033[90m'+''+'\033[31m'+'██'+'\033[90m'+'╔'+'\033[90m'+''+'\033[31m'+'██'+'\033[90m'+'╗ '+'\033[90m'+''+'\033[31m'+'██'+'\033[90m'+'║')
	print('\033[31m' + '           ''██'+'\033[90m'+'╔══'+'\033[90m'+''+'\033[31m'+'██'+'\033[90m'+'║'+'\033[90m'+''+'\033[31m'+'██'+'\033[90m'+'║╚'+'\033[90m'+''+'\033[31m'+'██'+'\033[90m'+'╔╝'+'\033[90m'+''+'\033[31m'+'██'+'\033[90m'+'║'+'\033[90m'+''+'\033[31m'+'██'+'\033[90m'+'╔══'+'\033[90m'+''+'\033[31m'+'██'+'\033[90m'+'║'+'\033[90m'+''+'\033[31m'+'██'+'\033[90m'+'║╚'+'\033[90m'+''+'\033[31m'+'██'+'\033[90m'+'╗'+'\033[90m'+''+'\033[31m'+'██'+'\033[90m'+'║')
	print('\033[31m' + '           ''██'+'\033[90m'+'║  '+'\033[90m'+''+'\033[31m'+'██'+'\033[90m'+'║'+'\033[90m'+''+'\033[31m'+'██'+'\033[90m'+'║ ╚═╝ '+'\033[90m'+''+'\033[31m'+'██'+'\033[90m'+'║'+'\033[90m'+''+'\033[31m'+'██'+'\033[90m'+'║  '+'\033[90m'+''+'\033[31m'+'██'+'\033[90m'+'║'+'\033[90m'+''+'\033[31m'+'██'+'\033[90m'+'║ ╚'+'\033[90m'+''+'\033[31m'+'████'+'\033[90m'+'║')
	print( '\033[90m' + '           ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝')
	print(r +  '[!]This script was written by Muhammed Aman')
	print(y +  '[!]This script is created for auto-claiming WAHO')

def rgb_color(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"
RESET = "\033[0m"
def get_ip():
    url = "https://api.ipify.org/?format=jsonp&callback=getIP"
    headers = {
        "Host": "api.ipify.org",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; Pixel Build/NHG47O) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.117 Mobile Safari/537.36",
        "Accept": "*/*",
        "X-Requested-With": "mark.via",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Dest": "script",
        "Referer": "https://waho.pro/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    r = requests.get(url, headers=headers)
    text = r.text  # example: getIP({"ip":"223.184.138.73"});
    match = re.search(r'"ip":"([^"]+)"', text)
    return match.group(1) if match else None
ip = get_ip()
def countdown_rgb(seconds):
    colors = [
        (255, 0, 0),     # Red
        (0, 255, 0),     # Green
        (0, 0, 255)      # Blue
    ]
    idx = 0  # Start color index
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer = f"{mins:02d}:{secs:02d}"
        r, g, b = colors[idx]
        color = rgb_color(r, g, b)
        print(color + timer + RESET, end="\r")
        time.sleep(1)
        seconds -= 1
        idx = (idx + 1) % len(colors)
    print(rgb_color(255, 0, 0) + "Lets Claim Next Account!" + RESET,end="\r")
os.system("clear")
init(autoreset=True)
# COLORS
C_ACC   = Fore.MAGENTA
C_QR    = Fore.CYAN
C_MONEY = Fore.GREEN
C_TIME  = Fore.YELLOW
C_OK    = Fore.GREEN
C_BAD   = Fore.RED
RESET   = Style.RESET_ALL

# -----------------------------------------------------
# 🔐 TOKEN MANAGER
# -----------------------------------------------------
def load_token():
    """Load token from token.json or ask user to create one"""
    if not os.path.exists(TOKEN_FILE):
        print(C_BAD + "No token found. Please add a token first." + RESET)
        save_token()

    with open(TOKEN_FILE, "r") as f:
        data = json.load(f)
        return data.get("token", "")


def save_token():
    """Ask user for token and save to token.json"""
    token = input("\nEnter your Waho token:\n> ").strip()

    with open(TOKEN_FILE, "w") as f:
        json.dump({"token": token}, f, indent=4)

    print(C_OK + "\nToken saved successfully!\n" + RESET)
    time.sleep(1)
    return token

# ---------- REQUEST HEADERS ----------
headers = {
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
    "accept-language": "ru,en;q=0.7"
}
# -----------------------------------------------------
# 🔍 FUNCTION: GET INFO
# -----------------------------------------------------
def get_info(auth):
 global ip
 url = f"https://api.waho.pro/member/index?token={auth}&ip={ip}"
 data = '{"httpRequestIndex":0,"httpRequestCount":0}'
 response = requests.post(url, headers=headers,data=data)
 data = json.loads(response.text)
 user_key = data["data"]["user_key"]
 today_commission = data["data"]["today_commission"]
 yesterday_commission = data["data"]["money"]
 return user_key,today_commission,yesterday_commission
# -----------------------------------------------------
# 🔍 FUNCTION: GET ALL ACCOUNTS
# -----------------------------------------------------
def get_account(auth):
    global ip
    url = f"https://api.waho.pro//newlogin/getwxlist?token={auth}&ip={ip}"
    data = '{"page":1,"limit":1000,"httpRequestIndex":0,"httpRequestCount":0}'
    response = requests.post(url, headers=headers, data=data)
    data = json.loads(response.text)

    items = data["data"]["list"]

    width = shutil.get_terminal_size().columns
    line = "-" * width

    for idx, item in enumerate(items, start=1):
        print(f"[{idx}]")
        print(f"{C_ACC}ACCOUNT:      {item.get('account','')}{RESET}")
        print(f"{C_QR}QR ID:        {item.get('qr_id','')}{RESET}")
        print(f"{C_MONEY}MONEY:        {item.get('money','')}{RESET}")
        print(f"{C_TIME}ONLINE TIME:  {item.get('online_time','')}{RESET}")
        print(line)


# -----------------------------------------------------
# 💰 FUNCTION: CLAIM REWARDS (only if online_time >= 24h)
# -----------------------------------------------------
def claim():
    global ip
    print("\nChecking accounts before claiming...\n")
    url_list = f"https://api.waho.pro//newlogin/getwxlist?token={auth}&ip={ip}"
    data = '{"page":1,"limit":1000,"httpRequestIndex":0,"httpRequestCount":0}'

    response = requests.post(url_list, headers=headers, data=data)
    acc_data = json.loads(response.text)["data"]["list"]

    for acc in acc_data:
        qr_id = acc["qr_id"]
        online_time = acc["online_time"]
        hours = online_time
        if hours < 24:
            print(f"{C_BAD}[SKIP] {acc['account']} —> Online {hours}h (<24h){RESET}")
            continue
        # ---------------- CLAIM ----------------
        claim_url = f"https://api.waho.pro/Activity/ClaimOnlineRewards?token={auth}&ip={ip}"
        payload = json.dumps({"qr_id": qr_id, "httpRequestIndex": 0, "httpRequestCount": 0})

        res = requests.post(claim_url, headers=headers, data=payload)
        result = json.loads(res.text)

        if result["code"] == 0:
            amount = result["data"]["Amount"]
            print(f"{C_OK}[CLAIMED] {acc['account']} -> +{amount} 💵{RESET}")
        else:
            print(f"{C_BAD}[FAILED] {acc['account']} → {result.get('msg','Error')}{RESET}")

        countdown_rgb(random.randint(5, 6))

    print("\nDone.\n")


# -----------------------------------------------------
# 🧭 MENU
# -----------------------------------------------------
def menu():
    banner()
    auth = load_token()
    user_key,today_commission,yesterday_commission = get_info(auth)
    width = shutil.get_terminal_size().columns
    print(" USER INFO ".center(width, "="))
    print(f"{C_ACC}USER IP: {ip}")
    print(f"{C_ACC}LOGIN ACCOUNT : {user_key}")
    print(f"{C_ACC}Today Commission : {today_commission}")
    print(f"{C_ACC}Total balance : {yesterday_commission}")
    print(" WAHO TOOL MENU ".center(width, "="))
    print(f"{C_ACC}1. Show all accounts")
    print(f"{C_ACC}2. Claim all eligible accounts (>24h)")
    print(f"{C_ACC}3. Exit{RESET}")

    choice = input("\nENTER YOUR CHOICE ")

    if choice == "1":
        get_account(auth)
    elif choice == "2":
        claim()
    elif choice == "3":
        exit()
    else:
        print("Invalid input!")

    input("\nPress ENTER to return to menu...")
    os.system("clear")
    menu()


menu()
#get_info(auth)
