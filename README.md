# Python Server

[![GitHub release](https://img.shields.io/github/release/watcher1337/python-server.svg)](https://github.com/watcher1337/python-server/releases/latest)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com/watcher1337/python-server/releases)
[![PyPI](https://img.shields.io/pypi/v/python-server.svg)](https://pypi.org/project/python-server/)
[![License](https://img.shields.io/github/license/watcher1337/python-server.svg)](https://github.com/watcher1337/python-server/blob/main/LICENSE)

**HTTP file server with upload support and authentication - perfect for file transfers during penetration testing and red team engagements.**

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🚀 Quick Install](#-quick-install)
- [📖 Usage](#-usage)
- [📤 Upload Examples](#-upload-examples)
- [🔐 Authentication](#-authentication)
- [🛠️ Development](#️-development)
- [📄 License](#-license)

---

## ✨ Features

- 📤 **File upload support** - POST and PUT methods
- 🔒 **Basic authentication** - Password protect your server
- 📂 **Directory listing** - Browse files via web interface
- 🖥️ **Cross-platform** - Windows, Linux, macOS (x64 & ARM64)
- 🔄 **Unique filename handling** - Auto-rename on conflict
- 📊 **File size display** - Human-readable file sizes
- 🌐 **Automatic IP detection** - Shows all available network interfaces
- ⚡ **Lightweight** - No external dependencies beyond Python
- 🔧 **Security features** - Path traversal protection, file size limits

---

## 🚀 Quick Install

### From PyPI (Recommended)

```bash
# Using pipx (isolated installation)
pipx install python-server

# Using uv
uv tool install python-server

# Windows Download
Download pre-built executables from releases:
