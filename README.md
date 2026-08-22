# Python Server

[![GitHub release](https://img.shields.io/github/release/watcher1337/python-server.svg)](https://github.com/watcher1337/python-server/releases/latest)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com/watcher1337/python-server/releases)


**HTTP file server with upload support and authentication - perfect for file transfers during penetration testing and red team engagements.**


---

## 🚀 Quick Install

### Linux / macOS  (pipx / uv )

```bash
pipx install python-server
```
```bash
uv tool install python-server
```

### Windows (pipx)

```bash
python -m pipx install python-server
```
```bash
python -m pipx ensurepath
```
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
curl.exe -X PUT -T "file.exe" http://10.10.10.8/file.exe

# Upload with POST
curl.exe -F "file=@file.exe" http://10.10.10.8/

# Upload with authentication
curl.exe -u admin:secret -X PUT -T "file.exe" http://10.10.10.8/file.exe

curl.exe -X PUT -T "file.exe" http://admin:secret@10.10.10.8/file.exe
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
