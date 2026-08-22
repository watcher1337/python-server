# Python Server

[![GitHub release](https://img.shields.io/github/release/watcher1337/python-server.svg)](https://github.com/watcher1337/python-server/releases/latest)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com/watcher1337/python-server/releases)


**HTTP file server with upload support and authentication - perfect for file transfers during penetration testing and red team engagements.**

---

## 📋 Table of Contents

- [Features](#-features)
- [Quick Install](#-quick-install)
- [Usage](#-usage)

---

## ✨ Features

- 📤 File upload – POST and PUT methods for file transfers
- 🔒 Basic authentication – Password protect your server
- 📂 Directory listing – Browse files via web interface
- 🖥️ Cross-platform – Windows, Linux, macOS (x64 & ARM64)
- 🔄 Auto-rename – Automatic unique filename on conflict
- 🌐 IP detection – Shows all available network interfaces
- 🛡️ Security – Path traversal protection, file size limits


---

## 🚀 Quick Install

### Linux / macOS / Windows (pipx)

```bash
pipx install python-server
```

### uv

```bash
uv tool install python-server
```

### pip

```bash
pip install python-server
```

### Windows / Linux / macOS (Binary)

Download from [releases](https://github.com/watcher1337/python-server/releases/latest):
- `python-server-windows-x64.exe`
- `python-server-linux-x64`
- `python-server-linux-arm64`
- `python-server-macos-x64`
- `python-server-macos-arm64`

---

## 📖 Usage

```bash
python-server                    # HTTP on port 80
python-server -p 8080            # HTTP on port 8080
python-server -d /tmp            # Serve /tmp directory
python-server -u admin -P secret # With authentication
python-server -h                 # Show help
```

**Options:**
- `-p, --port PORT` - Port to listen on (default: 80)
- `-d, --dir DIR` - Directory to serve (default: current directory)
- `-u, --user USER` - Username for basic authentication
- `-P, --password PASS` - Password for basic authentication
- `-h, --help` - Show help

### Upload Examples

```bash
# Upload with PUT
curl -X PUT -T "file.exe" http://10.10.10.8/file.exe

# Upload with POST
curl -F "file=@file.exe" http://10.10.10.8/

# Upload with authentication
curl -u admin:secret -X PUT -T "file.exe" http://10.10.10.8/file.exe
```

**Windows Upload Commands:**
```powershell
# PowerShell upload
powershell.exe -c "Invoke-WebRequest -useb -Uri http://10.10.10.8/windows.exe -Method PUT -InFile 'windows.exe'"

# PowerShell download
powershell.exe -c "wget -useb http://10.10.10.8/windows.exe -o windows.exe"

# certutil download
certutil.exe -urlcache -split -f http://10.10.10.8/windows.exe windows.exe
```
