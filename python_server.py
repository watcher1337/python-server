#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "legacy-cgi>=2.6.4",
#     "netifaces>=0.11.0",
# ]
# ///

import os
import html
import argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler
import cgi
import sys
from datetime import datetime
from urllib.parse import unquote
import socket
import netifaces
import base64

class SecureFileHandler(SimpleHTTPRequestHandler):
    """Enhanced file server with security features and upload support"""
    
    # Maximum file size (100MB)
    MAX_FILE_SIZE = 100 * 1024 * 1024
    
    # Authentication credentials (set via command line)
    AUTH_USERNAME = None
    AUTH_PASSWORD = None
    
    def __init__(self, *args, **kwargs):
        self.directory = os.getcwd()
        super().__init__(*args, **kwargs)
    
    def authenticate(self):
        """Check if request has valid authentication"""
        if not self.AUTH_USERNAME or not self.AUTH_PASSWORD:
            return True  # No authentication required
        
        auth_header = self.headers.get('Authorization')
        if not auth_header:
            return False
        
        try:
            auth_type, auth_data = auth_header.split(' ', 1)
            if auth_type.lower() != 'basic':
                return False
            
            decoded = base64.b64decode(auth_data).decode('utf-8')
            username, password = decoded.split(':', 1)
            
            return username == self.AUTH_USERNAME and password == self.AUTH_PASSWORD
        except:
            return False
    
    def require_auth(self):
        """Send authentication required response"""
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="Secure File Server"')
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(b'<html><body><h1>401 Unauthorized</h1><p>Authentication required</p></body></html>')
        self.log_request(401)
    
    def log_request(self, code='-', size='-'):
        """Log all HTTP requests with method, path, code, and client"""
        client = self.client_address[0]
        method = self.command if hasattr(self, 'command') else 'UNKNOWN'
        path = self.path if hasattr(self, 'path') else 'UNKNOWN'
        
        if code == '-':
            print(f"[*] {client} - {method} {path} - Processing")
        else:
            print(f"[*] {client} - {method} {path} - {code} {size if size != '-' else ''}")
    
    def log_message(self, format, *args):
        pass
    
    def do_GET(self):
        try:
            # Check authentication
            if not self.authenticate():
                self.require_auth()
                return
            
            if self.path == '/':
                self.send_directory_listing()
            else:
                safe_path = self.sanitize_path(self.path)
                if safe_path is None:
                    self.send_error(403, "Forbidden")
                    return
                super().do_GET()
            
            self.log_request(200)
            
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {str(e)}")
            self.log_request(500)
    
    def do_POST(self):
        try:
            # Check authentication
            if not self.authenticate():
                self.require_auth()
                return
            
            if self.path not in ('/upload', '/'):
                self.send_error(404, "Not Found")
                self.log_request(404)
                return
            
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > self.MAX_FILE_SIZE:
                self.send_error(413, "File too large")
                self.log_request(413)
                return
            
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers.get('Content-Type', '')}
            )
            
            if 'file' not in form:
                self.send_error(400, "No file provided")
                self.log_request(400)
                return
            
            file_item = form['file']
            if not file_item.filename:
                self.send_error(400, "Invalid filename")
                self.log_request(400)
                return
            
            filename = self.sanitize_filename(file_item.filename)
            if not filename:
                self.send_error(400, "Invalid filename")
                self.log_request(400)
                return
            
            filepath = self.get_unique_filename(filename)
            with open(filepath, 'wb') as f:
                f.write(file_item.file.read())
            
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(f"Uploaded successfully: {os.path.basename(filepath)}".encode('utf-8'))
            
            print(f"[+] POST upload: {os.path.basename(filepath)} ({content_length} bytes) from {self.client_address[0]}")
            self.log_request(200)
            
        except Exception as e:
            self.send_error(500, f"Upload failed: {str(e)}")
            print(f"[-] POST error: {str(e)}")
            self.log_request(500)
    
    def do_PUT(self):
        try:
            # Check authentication
            if not self.authenticate():
                self.require_auth()
                return
            
            filename = self.sanitize_filename(os.path.basename(unquote(self.path)))
            if not filename:
                filename = f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > self.MAX_FILE_SIZE:
                self.send_error(413, "File too large")
                self.log_request(413)
                return
            
            if content_length == 0:
                self.send_error(400, "No data received")
                self.log_request(400)
                return
            
            file_data = self.rfile.read(content_length)
            filepath = self.get_unique_filename(filename)
            
            with open(filepath, 'wb') as f:
                f.write(file_data)
            
            self.send_response(201)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(f"PUT uploaded: {os.path.basename(filepath)} ({content_length} bytes)".encode('utf-8'))
            
            print(f"[+] PUT upload: {os.path.basename(filepath)} ({content_length} bytes) from {self.client_address[0]}")
            self.log_request(201)
            
        except Exception as e:
            self.send_error(500, f"Upload failed: {str(e)}")
            print(f"[-] PUT error: {str(e)}")
            self.log_request(500)
    
    def do_OPTIONS(self):
        # Check authentication for OPTIONS
        if not self.authenticate():
            self.require_auth()
            return
        
        self.send_response(200)
        self.send_header('Allow', 'GET, POST, PUT, OPTIONS')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        print(f"[+] OPTIONS request from {self.client_address[0]}")
        self.log_request(200)
    
    def send_directory_listing(self):
        try:
            files = os.listdir('.')
        except PermissionError:
            self.send_error(403, "Permission denied")
            return
        except Exception:
            files = []
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>File Server</title>
        </head>
        <body>
            <center>
                <table width="80%" cellpadding="0" cellspacing="0" style="border: 1px solid #ccc; margin-top: 30px;">
                    <tr>
                        <td style="padding: 30px;">
                            <h1 style="border-bottom: 1px solid #ccc; padding-bottom: 15px;">
                                File Server
                            </h1>
                            
                            <div style="margin: 10px 0; padding: 10px;">
                                <form action="/" method="post" enctype="multipart/form-data" id="uploadForm" style="display: inline;">
                                    <input type="file" name="file" id="fileInput" style="display: inline-block; width: auto;">
                                    <input type="submit" value="Upload" style="display: inline-block;">
                                </form>
                                <span id="uploadStatus" style="margin-left: 10px; font-size: 0.9em;"></span>
                            </div>
                            
                            <h2 style="margin: 20px 0 10px;">
                                Directory Contents
                            </h2>
                            <table width="100%" cellpadding="0" cellspacing="0">
        """
        
        if not files:
            html_content += """
                                <tr>
                                    <td align="center" style="padding: 30px;">
                                        No files in this directory
                                    </td>
                                </tr>
                            """
        else:
            for f in sorted(files):
                is_dir = os.path.isdir(f)
                file_size = "" if is_dir else f" ({self.format_size(os.path.getsize(f))})"
                
                html_content += f"""
                                <tr>
                                    <td style="padding: 10px 15px; border-bottom: 1px solid #ddd;">
                                        <a href="/{html.escape(f)}" style="text-decoration: none;">
                                            {html.escape(f)}
                                        </a>
                                        <span style="float: right;">
                                            {file_size}
                                        </span>
                                    </td>
                                </tr>
                                """
        
        html_content += f"""
                            </table>
                            
                            <table width="100%" style="margin-top: 30px; border-top: 1px solid #ddd; padding-top: 20px;">
                                <tr>
                                    <td align="center" style="font-size: 0.85em;">
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </center>
            
            <script>
                document.getElementById('fileInput').addEventListener('change', function() {{
                    var status = document.getElementById('uploadStatus');
                    var files = this.files;
                    if (files.length > 0) {{
                        status.textContent = files.length + ' file(s) selected';
                    }} else {{
                        status.textContent = '';
                    }}
                }});
                
                document.getElementById('uploadForm').addEventListener('submit', function(e) {{
                    var status = document.getElementById('uploadStatus');
                    status.textContent = 'Uploading...';
                }});
            </script>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def sanitize_path(self, path):
        path = unquote(path).lstrip('/')
        if '..' in path or path.startswith('..'):
            return None
        return path
    
    def sanitize_filename(self, filename):
        filename = os.path.basename(filename)
        filename = ''.join(c for c in filename if c.isprintable())
        return filename.strip()
    
    def get_unique_filename(self, filename):
        base, ext = os.path.splitext(filename)
        counter = 1
        new_filename = filename
        
        while os.path.exists(new_filename):
            new_filename = f"{base}_{counter}{ext}"
            counter += 1
        
        return new_filename
    
    @staticmethod
    def format_size(bytes_size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.1f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.1f} TB"

class CustomHelpFormatter(argparse.HelpFormatter):
    def format_help(self):
        """Override to provide clean, minimal help output"""
        help_text = """
╔══════════════════════════════════════════════════════════════════╗
║             FILE PYTHON SERVER - HTTP                            ║
╚══════════════════════════════════════════════════════════════════╝

USAGE:
  python-server [OPTIONS]

OPTIONS:
  -p, --port PORT        Port (default: 80)
  -d, --dir DIR          Directory to serve
  -u, --user USER        Basic auth username
  -P, --password PASS    Basic auth password
  -h, --help             Show this help message

EXAMPLES:
  python-server                          HTTP on port 80
  python-server -p 3000 -d /tmp          HTTP on port 3000
  python-server -u admin -P secret       HTTP with authentication

UPLOAD CMD EXAMPLES:
  powershell.exe -c "Invoke-WebRequest -useb -Uri http://10.10.10.8/windows.exe -Method PUT -InFile 'windows.exe'"
  curl.exe -X PUT -T "windows.exe" http://10.10.10.8/windows.exe
  curl.exe -X PUT -T "windows.exe" http://admin:secret@10.10.10.8/windows.exe
  powershell.exe -c "wget -useb http://10.10.10.8/windows.exe -o windows.exe"
  certutil.exe -urlcache -split -f http://10.10.10.8/windows.exe windows.exe

"""
        return help_text

def get_ip_addresses():
    """Get all local IP addresses (excluding loopback)"""
    ip_list = []
    
    try:
        # Try netifaces first (more reliable)
        interfaces = netifaces.interfaces()
        for interface in interfaces:
            addrs = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addrs:
                for addr in addrs[netifaces.AF_INET]:
                    ip = addr.get('addr')
                    if ip and not ip.startswith('127.'):
                        if ip not in ip_list:
                            ip_list.append(ip)
    except:
        # Fallback to socket method
        try:
            # Get the local IP by connecting to an external address
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip_list.append(s.getsockname()[0])
            s.close()
        except:
            pass
    
    return ip_list

def main():
    parser = argparse.ArgumentParser(
        formatter_class=CustomHelpFormatter,
        add_help=False,
        description=""
    )
    
    parser.add_argument("-h", "--help", 
                       action="help",
                       default=argparse.SUPPRESS,
                       help="Show this help message")
    parser.add_argument("-p", "--port", 
                       type=int, 
                       default=80,
                       help="Port to listen on (default: 80)")
    parser.add_argument("-d", "--dir", 
                       dest="directory",
                       help="Directory to serve (default: current directory)")
    parser.add_argument("-u", "--user",
                       dest="username",
                       help="Username for basic authentication")
    parser.add_argument("-P", "--password",
                       dest="http_password",
                       help="Password for basic authentication")
    
    args = parser.parse_args()
    
    # Validate port
    if args.port < 1 or args.port > 65535:
        print("Error: Port must be between 1 and 65535")
        sys.exit(1)
    
    # Set authentication credentials
    if args.username or args.http_password:
        if not args.username:
            print("Error: -u/--user required when using -P/--password")
            sys.exit(1)
        if not args.http_password:
            print("Error: -P/--password required when using -u/--user")
            sys.exit(1)
        SecureFileHandler.AUTH_USERNAME = args.username
        SecureFileHandler.AUTH_PASSWORD = args.http_password
        print(f"[+] Authentication enabled: username='{args.username}'")
    else:
        SecureFileHandler.AUTH_USERNAME = None
        SecureFileHandler.AUTH_PASSWORD = None
        print("[*] Authentication disabled (no credentials provided)")
    
    # Change directory
    if args.directory:
        try:
            os.chdir(args.directory)
        except FileNotFoundError:
            print(f"Error: Directory '{args.directory}' not found.")
            sys.exit(1)
        except NotADirectoryError:
            print(f"Error: '{args.directory}' is not a directory.")
            sys.exit(1)
        except PermissionError:
            print(f"Error: Permission denied for '{args.directory}'.")
            sys.exit(1)
    
    server = HTTPServer(('0.0.0.0', args.port), SecureFileHandler)
    
    print(f"\n[+] HTTP Server started successfully")
    print(f"[+] Serving: {os.getcwd()}")
    print(f"[+] Serving HTTP on 0.0.0.0 port {args.port}")
    
    if SecureFileHandler.AUTH_USERNAME:
        print(f"[+] Authentication: Basic (username='{args.username}')")
    
    # Get and display IP addresses
    ips = get_ip_addresses()
    if ips:
        print(f"[+] Available on:")
        for ip in ips:
            print(f"    http://{ip}:{args.port}")
    else:
        print("[!] Could not determine local IP addresses")
        print(f"[+] Access via: http://localhost:{args.port}")
    
    print(f"[+] Press Ctrl+C to stop HTTP server\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[+] HTTP server stopped")
        server.shutdown()
        sys.exit(0)

if __name__ == "__main__":
    main()
