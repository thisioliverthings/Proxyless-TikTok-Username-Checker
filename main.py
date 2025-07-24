try:
    import requests, ctypes, time, os, threading, platform, random, string
    from colorama import Fore, init
except ImportError:
    input("Error while importing modules. Please install the modules in requirements.txt")

init(autoreset=True)

ascii_text = f"""
{Fore.RED}        _   _ _    _        _    
{Fore.RED}       | | (_) |  | |      | |   
{Fore.RED}       | |_ _| | _| |_ ___ | | __
{Fore.RED}       | __| | |/ / __/ _ \| |/ /
{Fore.RED}       | |_| |   <| || (_) |   < 
{Fore.RED}        \__|_|_|\_\\__\___/|_|\_\\
"""

IS_WINDOWS = platform.system() == "Windows"
clear = "cls" if IS_WINDOWS else "clear"

class TikTokTool:

    def __init__(self):
        self.lock = threading.Lock()
        self.checking = True
        self.usernames = []
        self.unavailable = 0
        self.available = 0
        self.counter = 0
        self.token = input(f"{Fore.RED}       [TOKEN] {Fore.CYAN}Enter your bot token: ")
        self.chat_id = input(f"{Fore.RED}       [CHAT_ID] {Fore.CYAN}Enter your Telegram chat ID: ")

    def update_title(self):
        if IS_WINDOWS:
            remaining = len(self.usernames) - (self.available + self.unavailable)
            ctypes.windll.kernel32.SetConsoleTitleW(
                f"TikTok Username Checker | Available: {self.available} | Unavailable: {self.unavailable} | Checked: {(self.available + self.unavailable)} | Remaining: {remaining} | Developed by @oli17"
            )

    def safe_print(self, arg):
        self.lock.acquire()
        print(arg)
        self.lock.release()

    def print_console(self, status, arg, color=Fore.RED):
        self.safe_print(f"       {Fore.LIGHTBLACK_EX}[{color}{status}{Fore.LIGHTBLACK_EX}] {color}{arg}")

    def send_to_telegram(self, username):
        message = f"✨ 𝑨𝒗𝒂𝒊𝒍𝒂𝒃𝒍𝒆 𝑼𝒔𝒆𝒓 ✨\n\n➤ @{username}\n\n🚀 تم الحصول عليه بواسطة بوت الفحص\n👤 المطور: @oli17"
        try:
            url = f"https://api.telegram.org/bot{self.token}/sendMessage"
            data = {"chat_id": self.chat_id, "text": message}
            requests.post(url, data=data)
        except:
            self.print_console("Error", "Failed to send to Telegram", Fore.YELLOW)

    def check_username(self, username):
        if username.isdigit():
            self.unavailable += 1
            self.print_console("Unavailable", username)
            return
        with requests.Session() as session:
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US",
                "content-type": "application/json"
            }
            r = session.head(f"https://www.tiktok.com/@{username}", headers=headers)
            if r.status_code == 200:
                self.unavailable += 1
                self.print_console("Unavailable", username)
            elif r.status_code == 404:
                self.available += 1
                self.print_console("Available or Banned", username, Fore.GREEN)
                self.send_to_telegram(username)
                with open("Available.txt", "a") as f:
                    f.write(username + "\n")
            self.update_title()

    def load_usernames(self):
        if not os.path.exists("usernames.txt"):
            self.print_console("Console", "File usernames.txt not found")
            time.sleep(10)
            os._exit(0)
        with open("usernames.txt", "r", encoding="UTF-8") as f:
            for line in f.readlines():
                line = line.strip()
                self.usernames.append(line)
            if not len(self.usernames):
                self.print_console("Console", "No usernames loaded in usernames.txt")
                time.sleep(10)
                os._exit(0)

    def generate_usernames(self):
        amount = int(input(f"       {Fore.RED}[INPUT]{Fore.CYAN} Amount of usernames: "))
        length = int(input(f"       {Fore.RED}[INPUT]{Fore.CYAN} Length of each username: "))
        with open("usernames.txt", "a") as f:
            for _ in range(amount):
                generated = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
                print(f"       {Fore.GREEN}[Generated] {Fore.CYAN}{generated}")
                f.write(generated + "\n")
        input(f"\n       {Fore.YELLOW}[Done]{Fore.CYAN} Press Enter to return...")

    def delete_usernames(self):
        if os.path.exists("usernames.txt"):
            os.remove("usernames.txt")
            self.print_console("Console", "usernames.txt deleted.", Fore.YELLOW)
        else:
            self.print_console("Console", "No usernames.txt file found.", Fore.YELLOW)
        input(f"\n       {Fore.YELLOW}[Return]{Fore.CYAN} Press Enter to return...")

    def main(self):
        while True:
            os.system(clear)
            if IS_WINDOWS:
                ctypes.windll.kernel32.SetConsoleTitleW("TikTok Username Tool | Developed by @oli17")
            print(ascii_text)
            print(f"       {Fore.MAGENTA}[1] {Fore.CYAN}Generate Usernames")
            print(f"       {Fore.MAGENTA}[2] {Fore.CYAN}Check Usernames")
            print(f"       {Fore.MAGENTA}[3] {Fore.CYAN}Delete usernames.txt")
            print(f"       {Fore.MAGENTA}[4] {Fore.CYAN}Exit\n")
            choice = input(f"       {Fore.RED}[CHOICE]{Fore.CYAN} Enter choice: ")

            if choice == "1":
                self.generate_usernames()
            elif choice == "2":
                os.system(clear)
                print(ascii_text)
                self.load_usernames()
                threads = int(input(f"       {Fore.RED}[INPUT]{Fore.CYAN} Threads (max 5): "))
                if threads >= 5:
                    threads = 5
                print()
                def thread_starter():
                    self.check_username(self.usernames[self.counter])
                while self.checking:
                    if threading.active_count() <= threads:
                        try:
                            threading.Thread(target=thread_starter).start()
                            self.counter += 1
                        except:
                            pass
                        if len(self.usernames) <= self.counter:
                            self.checking = None
                input(f"\n       {Fore.YELLOW}[Done]{Fore.CYAN} Press Enter to return...")
            elif choice == "3":
                self.delete_usernames()
            elif choice == "4":
                break
            else:
                self.print_console("Console", "Invalid choice.", Fore.RED)
                time.sleep(2)

if __name__ == "__main__":
    obj = TikTokTool()
    obj.main()
