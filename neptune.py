import sys, os, time, threading, requests, socks, socket, json, ctypes, concurrent.futures
from pystyle import Write, System, Colors
from colorama import Fore
from datetime import datetime

lock = threading.Lock()


def neptune():
    ctypes.windll.kernel32.SetConsoleTitleW(f"[ Scraper & Checker ] Naxn1a")
    System.Clear()
    Write.Print(
        f"""
\t\t         ,--.                                                                   
\t\t       ,--.'|                        ___                                        
\t\t   ,--,:  : |          ,-.----.    ,--.'|_                                      
\t\t,`--.'`|  ' :          \    /  \   |  | :,'          ,--,      ,---,            
\t\t|   :  :  | |          |   :    |  :  : ' :        ,'_ /|  ,-+-. /  |           
\t\t:   |   \ | :   ,---.  |   | .\ :.;__,'  /    .--. |  | : ,--.'|'   |   ,---.   
\t\t|   : '  '; |  /     \ .   : |: ||  |   |   ,'_ /| :  . ||   |  ,"' |  /     \  
\t\t'   ' ;.    ; /    /  ||   |  \ ::__,'| :   |  ' | |  . .|   | /  | | /    /  | 
\t\t|   | | \   |.    ' / ||   : .  |  '  : |__ |  | ' |  | ||   | |  | |.    ' / | 
\t\t'   : |  ; .''   ;   /|:     |`-'  |  | '.'|:  | : ;  ; ||   | |  |/ '   ;   /| 
\t\t|   | '`--'  '   |  / |:   : :     ;  :    ;'  :  `--'   \   | |--'  '   |  / | 
\t\t'   : |      |   :    ||   | :     |  ,   / :  ,      .-./   |/      |   :    | 
\t\t;   |.'       \   \  / `---'.|      ---`-'   `--`----'   '---'        \   \  /  
\t\t'---'          `----'    `---`                                         `----'   

\t\t============   Scraper & Checker http, socks4 and socks5 proxies.   ============\n
""",
        Colors.blue_to_purple,
        interval=0,
    )
    time.sleep(1)


def local_time():
    current_date = datetime.now()
    hour = current_date.hour
    minute = current_date.minute
    second = current_date.second
    current_time = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
    return current_time


def logger(title, text):
    print(
        f"{Fore.MAGENTA}{local_time()}{Fore.RESET} [ {Fore.LIGHTBLUE_EX}{title}{Fore.RESET} ] ",
        end="",
    )
    Write.Print(text, Colors.blue_to_purple, interval=0.000)


def get_proxies_list(type):
    data = json.loads(open("./config.json").read())
    return data[type]


def save_scrape_proxy(link, listName):
    proxies = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        results = executor.map(get_scrape_proxy, link)
        for result in results:
            proxies.extend(result)
    with open(f"{listName}", "w") as file:
        for proxy in proxies:
            if ":" in proxy and not any(c.isalpha() for c in proxy):
                file.write(proxy + "\n")
    return proxies


def get_scrape_proxy(link):
    response = requests.get(link)
    if response.status_code == 200:
        with lock:
            if len(link) < 60:
                logger("GET", link[:60] + "\n")
            else:
                logger("GET", link[:60] + "***\n")
        proxies = response.text.splitlines()
        return proxies
    return []


def check_proxy_http(proxy):
    global folder
    try:
        url = "http://httpbin.org/get"
        r = requests.get(
            url,
            proxies={"http": "http://" + proxy, "https": "https://" + proxy},
            timeout=30,
        )
        if r.status_code == 200:
            with lock:
                logger("SUCCESS", f"HTTP/S: {proxy}\n")
            with open(f"{folder}/http.txt", "a+") as f:
                f.write(proxy + "\n")
    except requests.exceptions.RequestException as e:
        pass


def check_proxy_socks(proxy):
    global folder, type
    try:
        match type:
            case "socks4":
                socks.setdefaultproxy(
                    socks.PROXY_TYPE_SOCKS4,
                    proxy.split(":")[0],
                    int(proxy.split(":")[1]),
                )
                typetext = "SOCKS4"
            case "socks5":
                socks.setdefaultproxy(
                    socks.PROXY_TYPE_SOCKS5,
                    proxy.split(":")[0],
                    int(proxy.split(":")[1]),
                )
                typetext = "SOCKS5"
        socket.socket = socks.socksocket
        socket.create_connection(("www.google.com", 443), timeout=5)
        with lock:
            logger("SUCCESS", f"{typetext}: {proxy}\n")
        with open(f"{folder}/{typetext.lower()}.txt", "a+") as f:
            f.write(proxy + "\n")
    except (socks.ProxyConnectionError, socket.timeout, OSError):
        pass


def validate(proxy_type):
    global type
    if proxy_type == "http":
        with open(f"temp_{proxy_type}.txt", "r") as f:
            proxies = f.read().splitlines()
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(proxies)) as execute:
            execute.map(check_proxy_http, proxies)
    elif proxy_type == "socks4":
        with open(f"temp_{proxy_type}.txt", "r") as f:
            proxies = f.read().splitlines()
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(proxies)) as execute:
            type = "socks4"
            execute.map(check_proxy_socks, proxies)
    elif proxy_type == "socks5":
        with open(f"temp_{proxy_type}.txt", "r") as f:
            proxies = f.read().splitlines()
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(proxies)) as execute:
            type = "socks5"
            execute.map(check_proxy_socks, proxies)


folder = "./data"
type = ""
proxies_type = ["http", "socks4", "socks5"]


def run():
    neptune()

    global folder, type, proxies_type
    type = "http"

    temp_http = "temp_http.txt"
    temp_socks4 = "temp_socks4.txt"
    temp_socks5 = "temp_socks5.txt"

    if len(sys.argv) > 1:
        if sys.argv[1] == "4":
            type = "socks4"
        elif sys.argv[1] == "5":
            type = "socks5"
        elif sys.argv[1] == "0":
            type = "all"

    http_list = get_proxies_list("http")
    socks4_list = get_proxies_list("socks4")
    socks5_list = get_proxies_list("socks5")

    if type == "http":
        proxies = save_scrape_proxy(http_list, temp_http)
    elif type == "socks4":
        proxies = save_scrape_proxy(socks4_list, temp_socks4)
    elif type == "socks5":
        proxies = save_scrape_proxy(socks5_list, temp_socks5)
    elif type == "all":
        proxies = []
        for x in [0, 1, 2]:
            match x:
                case 0:
                    proxies.append(save_scrape_proxy(http_list, temp_http))
                case 1:
                    proxies.append(save_scrape_proxy(socks4_list, temp_socks4))
                case 2:
                    proxies.append(save_scrape_proxy(socks5_list, temp_socks5))
        proxies = [item for sublist in proxies for item in sublist]

    logger("INFO", f"Scraped {len(proxies)} proxies.\n")

    time.sleep(1)
    if not os.path.exists(folder):
        os.mkdir(folder)
        open(f"{folder}/http.txt", "w").close()
        open(f"{folder}/socks4.txt", "w").close()
        open(f"{folder}/socks5.txt", "w").close()

    threads = []
    for proxy_type in proxies_type:
        if os.path.exists(f"temp_{proxy_type}.txt"):
            t = threading.Thread(target=validate, args=(proxy_type,))
            t.start()
            threads.append(t)
    for t in threads:
        t.join()

    for file in proxies_type:
        if os.path.exists(f"temp_{file}.txt"):
            os.remove(f"temp_{file}.txt")

    for file in os.listdir(folder):
        if os.path.exists(f"{folder}/{file}"):
            with open(f"{folder}/{file}", "r") as f:
                lines = f.read().splitlines()
            lines = [line for line in lines if line.strip() != ""]
            with open(f"{folder}/{file}", "w") as f:
                for line in lines:
                    f.write(line + "\n")
            logger("INFO", f"Validated {len(lines)} {file} proxies.\n")
    logger("DONE", "Press enter to exit..\n")
    input()


if __name__ == "__main__":
    run()
