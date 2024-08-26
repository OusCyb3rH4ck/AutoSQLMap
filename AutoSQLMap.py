#!/usr/bin/env python3

import os, time, signal, sys
from colorama import Fore, Style, init

init(autoreset=True)

def signal_handler(signal, frame):
    print(f"\n\n{Fore.RED}[!] Quitting...{Fore.RESET}\n")
    sys.exit(1)

signal.signal(signal.SIGINT, signal_handler)

def print_banner():
    os.system('clear')
    os.system("figlet AutoSQLMap | lolcat")
    print(f"{Fore.GREEN}Made by OusCyb3rH4ck{Style.RESET_ALL}\n")

def get_input(prompt, default=""):
    user_input = input(prompt + f" [{default}]: ")
    return user_input if user_input else default

def main():
    print_banner()
    
    url = get_input(f"{Fore.YELLOW}Enter the target URL (e.g., http://example.com/page.php?id=1){Style.RESET_ALL}")
    technique = get_input(f"{Fore.YELLOW}Enter the injection techniques (e.g., BEUSQT){Style.RESET_ALL}", "BEUSQT")
    tamper = get_input(f"{Fore.YELLOW}Enter tamper scripts (comma-separated, e.g., space2comment,charencode){Style.RESET_ALL}", "")
    level = get_input(f"{Fore.YELLOW}Enter the level of tests (1-5, default is 5){Style.RESET_ALL}", "5")
    risk = get_input(f"{Fore.YELLOW}Enter the risk level (1-3, default is 3){Style.RESET_ALL}", "3")
    threads = get_input(f"{Fore.YELLOW}Enter the number of threads (default is 5){Style.RESET_ALL}", "5")
    random_agent = get_input(f"{Fore.YELLOW}Use random User-Agent? (yes/no, default is yes){Style.RESET_ALL}", "yes")
    dbs = get_input(f"{Fore.YELLOW}List databases after testing? (yes/no, default is yes){Style.RESET_ALL}", "yes")
    batch = get_input(f"{Fore.YELLOW}Run in batch mode? (yes/no, default is no){Style.RESET_ALL}", "no")
    
    sqlmap_command = f"sqlmap -u \"{url}\""
    
    if technique:
        sqlmap_command += f" --technique={technique}"
    
    if tamper:
        sqlmap_command += f" --tamper={tamper}"
    
    sqlmap_command += f" --level={level}"
    sqlmap_command += f" --risk={risk}"
    sqlmap_command += f" --threads={threads}"

    if random_agent.lower() == "yes":
        sqlmap_command += " --random-agent"
    
    if dbs.lower() == "yes":
        sqlmap_command += " --dbs"
    
    if batch.lower() == "yes":
        sqlmap_command += " --batch"
    
    print(f"\n{Fore.CYAN}Constructed SQLMap command:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{sqlmap_command}{Style.RESET_ALL}")
    
    execute = get_input(f"\n{Fore.YELLOW}Do you want to execute this command? (yes/no, default is yes){Style.RESET_ALL}", "yes").lower()
    
    if execute == "yes":
        try:
            time.sleep(2)
            os.system(sqlmap_command)
        except Exception as e:
            print(f"\n\n{Fore.RED}[!] An error occurred: {e}{Style.RESET_ALL}\n")
            sys.exit(1)
    else:
        print(f"\n\n{Fore.RED}[!] Command execution canceled.{Style.RESET_ALL}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
