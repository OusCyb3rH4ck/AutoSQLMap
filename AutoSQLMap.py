#!/usr/bin/env python3

import os, time, signal, sys
from colorama import Fore, Style, init
from InquirerPy import inquirer

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

def menu(options):
    selected_options = inquirer.checkbox(
        message="[-] Select the additional options you want to include:",
        choices=options,
        instruction="Use SPACE to select, ENTER to confirm",
    ).execute()

    extracted_options = [option[0] for option in selected_options]

    print(f"{Fore.LIGHTGREEN_EX}\n[*] Selected options:{Style.RESET_ALL}")
    for option in extracted_options:
        print(option)
    
    additional_inputs = {}
    for option in extracted_options:
        if "=" in option:
            prompt = f"{Fore.LIGHTMAGENTA_EX}[!] Enter value for option{Style.RESET_ALL} '{option}':"
            value = get_input(prompt)
            additional_inputs[option] = value
        elif any(char.isupper() for char in option):
            # For options that are uppercase but don't use `=`, request a value
            prompt = f"{Fore.LIGHTMAGENTA_EX}[!] Enter value for option{Style.RESET_ALL} '{option}':"
            value = get_input(prompt)
            additional_inputs[option] = value
        else:
            # For options without `=` and not in uppercase, no value needed
            additional_inputs[option] = None
    
    return additional_inputs

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
    more_options = get_input(f"{Fore.CYAN}\n[+] Do you want to add more additional options? (yes/no, default is no){Style.RESET_ALL}", "no")
    
    options = [
        ("-v VERBOSE", "Verbosity level: 0-6 (default 1)"),
        ("-d DIRECT", "Connection string for direct database connection"),
        ("-l LOGFILE", "Parse target(s) from Burp or WebScarab proxy log file"),
        ("-m BULKFILE", "Scan multiple targets given in a textual file"),
        ("-r REQUESTFILE", "Load HTTP request from a file"),
        ("-g GOOGLEDORK", "Process Google dork results as target URLs"),
        ("-c CONFIGFILE", "Load options from a configuration INI file"),

        ("--method=METHOD", "Force usage of given HTTP method (e.g. PUT)"),
        ("--data=DATA", "Data string to be sent through POST (e.g. \"id=1\")"),
        ("--param-del=PARAMDEL", "Character used for splitting parameter values (e.g. &)"),
        ("--cookie=COOKIE", "HTTP Cookie header value (e.g. \"PHPSESSID=a8d127e..\")"),
        ("--cookie-del=COOKIEDEL", "Character used for splitting cookie values (e.g. ;)"),
        ("--live-cookies=LIVECOOKIES", "Live cookies file used for loading up-to-date values"),
        ("--load-cookies=LOADCOOKIES", "File containing cookies in Netscape/wget format"),
        ("--drop-set-cookie", "Ignore Set-Cookie header from response"),
        ("--mobile", "Imitate smartphone through HTTP User-Agent header"),
        ("--host=HOST", "HTTP Host header value"),
        ("--referer=REFERER", "HTTP Referer header value"),
        ("--headers=HEADERS", "Extra headers (e.g. \"Accept-Language: fr\nETag: 123\")"),
        ("--auth-type=AUTHTYPE", "HTTP authentication type (Basic, Digest, Bearer, ...)"),
        ("--auth-cred=AUTHCRED", "HTTP authentication credentials (name:password)"),
        ("--auth-file=AUTHFILE", "HTTP authentication PEM cert/private key file"),
        ("--abort-code=ABORTCODE", "Abort on (problematic) HTTP error code(s) (e.g. 401)"),
        ("--ignore-code=IGNORECODE", "Ignore (problematic) HTTP error code(s) (e.g. 401)"),
        ("--ignore-proxy", "Ignore system default proxy settings"),
        ("--ignore-redirects", "Ignore redirection attempts"),
        ("--ignore-timeouts", "Ignore connection timeouts"),
        ("--proxy=PROXY", "Use a proxy to connect to the target URL"),
        ("--proxy-cred=PROXYCRED", "Proxy authentication credentials (name:password)"),
        ("--proxy-file=PROXYFILE", "Load proxy list from a file"),
        ("--proxy-freq=PROXYFREQ", "Requests between change of proxy from a given list"),
        ("--tor", "Use Tor anonymity network"),
        ("--tor-port=TORPORT", "Set Tor proxy port other than default"),
        ("--tor-type=TORTYPE", "Set Tor proxy type (HTTP, SOCKS4 or SOCKS5 (default))"),
        ("--check-tor", "Check to see if Tor is used properly"),
        ("--delay=DELAY", "Delay in seconds between each HTTP request"),
        ("--timeout=TIMEOUT", "Seconds to wait before timeout connection (default 30)"),
        ("--retries=RETRIES", "Retries when the connection timeouts (default 3)"),
        ("--retry-on=RETRYON", "Retry request on regexp matching content (e.g. \"drop\")"),
        ("--randomize=RPARAM", "Randomly change value for given parameter(s)"),
        ("--safe-url=SAFEURL", "URL address to visit frequently during testing"),
        ("--safe-post=SAFEPOST", "POST data to send to a safe URL"),
        ("--safe-req=SAFEREQ", "Load safe HTTP request from a file"),
        ("--safe-freq=SAFEFREQ", "Regular requests between visits to a safe URL"),
        ("--skip-urlencode", "Skip URL encoding of payload data"),
        ("--csrf-token=CSRFTOKEN", "Parameter used to hold anti-CSRF token"),
        ("--csrf-url=CSRFURL", "URL address to visit for extraction of anti-CSRF token"),
        ("--csrf-method=CSRFMETHOD", "HTTP method to use during anti-CSRF token page visit"),
        ("--csrf-data=CSRFDATA", "POST data to send during anti-CSRF token page visit"),
        ("--csrf-retries=CSRFRERIES", "Retries for anti-CSRF token retrieval (default 0)"),
        ("--force-ssl", "Force usage of SSL/HTTPS"),
        ("--chunked", "Use HTTP chunked transfer encoded (POST) requests"),
        ("--hpp", "Use HTTP parameter pollution method"),
        ("--eval=EVALCODE", "Evaluate provided Python code before the request (e.g. \"import hashlib;id2=hashlib.md5(id).hexdigest()\")"),

        ("-o", "Turn on all optimization switches"),
        ("--predict-output", "Predict common queries output"),
        ("--keep-alive", "Use persistent HTTP(s) connections"),
        ("--null-connection", "Retrieve page length without actual HTTP response body"),

        ("-p TESTPARAMETER", "Testable parameter(s)"),
        ("--skip=SKIP", "Skip testing for given parameter(s)"),
        ("--skip-static", "Skip testing parameters that not appear to be dynamic"),
        ("--param-exclude=PARAMEXCLUDE", "Regexp to exclude parameters from testing (e.g. \"ses\")"),
        ("--param-filter=PARAMFILTER", "Select testable parameter(s) by place (e.g. \"POST\")"),
        ("--dbms=DBMS", "Force back-end DBMS to provided value"),
        ("--dbms-cred=DBMSCREDS", "DBMS authentication credentials (user:password)"),
        ("--os=OS", "Force back-end DBMS operating system to provided value"),
        ("--invalid-bignum", "Use big numbers for invalidating values"),
        ("--invalid-logical", "Use logical operations for invalidating values"),
        ("--invalid-string", "Use random strings for invalidating values"),
        ("--no-cast", "Turn off payload casting mechanism"),
        ("--no-escape", "Turn off string escaping mechanism"),
        ("--prefix=PREFIX", "Prefix to prepend to user-defined value"),
        ("--suffix=SUFFIX", "Suffix to append to user-defined value"),
        ("--prefix-suffix=PREFIXSUFFIX", "Prefix and suffix to add to each parameter value (e.g. \"userID=0,1\")"),

        ("--opt=OPT", "Perform optimizations for queries based on the provided value"),
        ("--tech=TECH", "Force usage of SQL injection technique(s) (e.g. \"B\")"),
        ("--tech-no-verbose", "Force usage of SQL injection technique(s) (e.g. \"BE\")"),
        ("--tables", "List tables after testing"),
        ("--columns", "List columns after testing"),
        ("--schema", "Show schema for tables and columns"),
        ("--dump", "Dump database contents (requires --tables)"),
        ("--dump-all", "Dump all database contents (requires --tables)"),
        ("--search=SEARCH", "Search for text within database content"),
        ("--search-text=SEARCHTEXT", "Search for text within database content (using --dump)"),
        ("--scan-time=SCANTIME", "Time to scan each target URL in seconds")
    ]
    
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

    if more_options.lower() == "yes":
        additional_inputs = menu(options)
        for option, value in additional_inputs.items():
            if value is None:
                sqlmap_command += f" {option}"
            elif "=" in option:
                option_name = option.split('=')[0]
                sqlmap_command += f" {option_name}={value}"
            else:
                if any(char.isupper() for char in option):
                    option_name = option.split()[0]
                    sqlmap_command += f" {option_name} {value}"
                else:
                    sqlmap_command += f" {option} {value}"

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
