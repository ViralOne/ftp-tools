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
    with open(file_path, 'r') as file:
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
    parser.add_argument('file_path', default='servers.json', type=str, help='Path to the JSON file containing FTP server details')
    parser.add_argument('-d', '--download-folder', type=str, default='downloads', help='Local folder to save downloaded files (default: downloads)')
    return parser.parse_args()

def download_from_ftp(host, username, password, local_folder):
    if not is_host_reachable(host):
        print(f"Host {host} is unreachable. Skipping download.")
        return
    
    try:
        with FTP(host) as ftp:
            print(f"Connected to {host}")
            ftp.login(username, password)

            host_folder = Path(local_folder) / host
            host_folder.mkdir(parents=True, exist_ok=True)

            ftp.cwd('/')

            files = ftp.nlst()
            for file in files:
                if file in (".ftpquota", ".", ".."):
                    continue
                local_file = host_folder / quote(file)

                file_size = ftp.size(file)
                if file_size > 0:
                    with open(local_file, "wb") as fileu:
                        ftp.retrbinary(f"RETR {file}", fileu.write)
                        ftp.delete(file)
                    print(f'Downloaded locally and removed from host: {file}')
                    time.sleep(1)
                else:
                    ftp.delete(file)
                    print(f'Removing 0KB file: {file}')
    except Exception as e:
        print(f"Error: {e}")

def main():
    args = parse_arguments()
    ftp_servers = load_ftp_servers(args.file_path)
    local_folder = args.download_folder

    with ThreadPoolExecutor() as executor:
        for server in ftp_servers:
            executor.submit(download_from_ftp, server["host"], server["username"], server["password"], local_folder)

if __name__ == "__main__":
    main()
