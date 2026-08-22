# 📖 README.md (Ultra Short)

```markdown
# Python Server

[![GitHub release](https://img.shields.io/github/release/watcher1337/python-server.svg)](https://github.com/watcher1337/python-server/releases/latest)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)

**HTTP file server with upload support for pentesting.**

---

## 🚀 Install

```bash
pipx install python-server
```

## 📖 Usage

```bash
python-server -p 8080 -d /tmp -u admin -P secret
```

## 📤 Upload

```bash
curl -X PUT -T "file.exe" http://10.10.10.8/file.exe
```

## 🔧 Options

| Option | Description |
|--------|-------------|
| `-p` | Port (default: 80) |
| `-d` | Directory |
| `-u` | Username |
| `-P` | Password |
| `-h` | Help |


---

## Even Shorter (One-Liner Style)

```markdown
# Python Server

**HTTP file server with upload for pentesting.**

```bash
pipx install python-server
python-server -p 8080 -u admin -P secret
curl -X PUT -T "file.exe" http://10.10.10.8/file.exe
```
