import os
from ftplib import FTP
import time
import json
from concurrent.futures import ThreadPoolExecutor

def load_ftp_servers(file_path):
    with open(file_path, 'r') as file:
        ftp_servers = json.load(file)
    return ftp_servers

def download_from_ftp(host, username, password, local_folder):
    try:
        # Connect to FTP server
        ftp = FTP(host)
        print(f"Connected to {host}")
        ftp.login(username, password)

        # Create a local directory for the host if it doesn't exist
        host_folder = os.path.join(local_folder, host)
        os.makedirs(host_folder, exist_ok=True)

        # Change to the remote directory
        ftp.cwd('/')

        # List files and download each one
        files = ftp.nlst()
        for file in files:
            if file == ".ftpquota" or file == "." or file == "..":
                continue
            valid_file_name = file.replace('<', '').replace('>', '').replace(':', '').replace('"', '').replace('/', '').replace('\\', '').replace('|', '').replace('?', '').replace('*', '')
            local_file = os.path.join(host_folder, valid_file_name)

            # Get the size of the file
            file_size = ftp.size(file)

            # Check if the file size is greater than 0 before downloading
            if file_size > 0:
                with open(local_file, "wb") as fileu:
                    ftp.retrbinary(f"RETR {file}", fileu.write)
                    ftp.delete(file)
                print(f'Downloaded locally and removed from host: {file}')
                time.sleep(1)
            else:
                print(f'Skipping download of 0KB file: {file}')

        # Close FTP connection
        ftp.quit()
    except Exception as e:
        print(f"Error: {e}")

def main():
    # Load FTP server credentials from file
    ftp_servers = load_ftp_servers("servers.json")

    # Local folder to save the files
    local_folder = "downloads"

    # Download mode: Set to True for periodic job, False for one-time job
    periodic_download = False

    # Interval in minutes for periodic job
    interval_minutes = 30

    # Download from each FTP server in parallel
    with ThreadPoolExecutor() as executor:
        for server in ftp_servers:
            executor.submit(download_from_ftp, server["host"], server["username"], server["password"], local_folder)

    if periodic_download:
        # Sleep for the specified interval
        print(f"Sleeping for {interval_minutes} minutes...")
        time.sleep(interval_minutes * 60)

if __name__ == "__main__":
    main()
