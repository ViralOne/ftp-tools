# FTP File Downloader

This script is designed to download files from multiple FTP servers concurrently.

## Features

- **Concurrent Downloads**: Utilizes multithreading to download files from multiple FTP servers simultaneously, improving efficiency.
- **Error Handling**: Handles exceptions gracefully to ensure uninterrupted execution.
- **Customizable Settings**: Allows customization of download mode (one-time or periodic) and interval for periodic downloads.
- **Automatic File Cleanup**: Removes downloaded files from the FTP server after successful download to prevent duplication.

## Usage

1. Clone the repository or download the script directly.
2. Ensure Python 3.x is installed on your system.
3. Modify the `servers.json` file to include the FTP server details you want to connect to.
4. Run the script using the command `python ftp_downloader.py`.
5. Optionally, set `periodic_download` to `True` and specify the `interval_minutes` for periodic downloads.

## Configuration

### servers.json

This JSON file contains the details of FTP servers to connect to. Each server object should include the following fields:

- `"host"`: FTP server hostname or IP address.
- `"username"`: FTP server username for authentication.
- `"password"`: FTP server password for authentication.

Example `servers.json`:

```json
[
    {
        "host": "ftp.example.com",
        "username": "user",
        "password": "password123"
    },
    {
        "host": "ftp.anotherexample.com",
        "username": "admin",
        "password": "pass456"
    }
]
```