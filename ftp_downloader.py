import os
import json
import time
import socket
import argparse
from concurrent.futures import ThreadPoolExecutor
from ftplib import FTP
from urllib.parse import quote
from pathlib import Path

def load_ftp_servers(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        ftp_servers = json.load(file)
    return ftp_servers

def is_host_reachable(host):
    try:
        socket.gethostbyname(host)
        return True
    except socket.error:
        return False

def parse_arguments():
    parser = argparse.ArgumentParser(description='FTP File Downloader')
    parser.add_argument('file_path', nargs='?', default='servers.json', type=str, help='Path to the JSON file containing FTP server details')
    parser.add_argument('-d', '--download-folder', type=str, default='downloads', help='Local folder to save downloaded files (default: downloads)')
    parser.add_argument('-p', '--periodic', action='store_true', help='Enable periodic checking')
    parser.add_argument('-r', '--remove', action='store_true', help='Remove file after being downloaded')
    parser.add_argument('-i', '--interval', type=int, default=30, help='Interval in minutes for periodic download (default: 30)')
    return parser.parse_args()

def download_from_ftp(host, username, password, local_folder):
    args = parse_arguments()
    if not is_host_reachable(host):
        print(f"Host {host} is unreachable. Skipping download.")
        return

    try:
        with FTP(host) as ftp:
            ftp.login(username, password)
            ftp.cwd('/')
            files = ftp.nlst()
            for file in files:
                if file in (".ftpquota", ".", ".."):
                    continue
                local_file = Path(local_folder) / host / quote(file)
                if not local_file.parent.exists():
                    local_file.parent.mkdir(parents=True, exist_ok=True)
                try:
                    file_size = ftp.size(file)
                except:
                    file_size = 0
                if file_size > 0:
                    with open(local_file, "wb") as fileu:
                        ftp.retrbinary(f"RETR {file}", fileu.write)
                        if args.remove:
                            ftp.delete(file)
                            print(f'Downloaded locally and removed from {host}: {file}')
                        else:
                            print(f'Downloaded locally from {host}: {file}')
                    time.sleep(5)
                else:
                    if args.remove:
                        ftp.delete(file)
                        print(f'Removed 0KB file: {file}')
    except Exception as e:
        print(f"Error: {e} - {host}")

def main():
    args = parse_arguments()
    ftp_servers = load_ftp_servers(args.file_path)
    local_folder = args.download_folder

    with ThreadPoolExecutor() as executor:
        if args.periodic:
            while True:
                for server in ftp_servers:
                   executor.submit(download_from_ftp, server["host"], server["username"], server["password"], local_folder)
                time.sleep(args.interval * 60)
        else:
            for server in ftp_servers:
                executor.submit(download_from_ftp, server["host"], server["username"], server["password"], local_folder)

if __name__ == "__main__":
    main()
