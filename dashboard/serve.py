#!/usr/bin/env python3
"""
Simple HTTP server for the Bridgewater Forecasting Dashboard
"""

import http.server
import socketserver
import webbrowser
import sys
from pathlib import Path

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers to allow iframe embedding
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def log_message(self, format, *args):
        # Colorful logging
        print(f"\033[94m[{self.log_date_time_string()}]\033[0m {format % args}")

def main():
    # Change to the dashboard directory
    dashboard_dir = Path(__file__).parent

    print("\n" + "="*60)
    print("🎯 Bridgewater x Metaculus 2026 Dashboard")
    print("="*60)
    print(f"\n📁 Serving from: {dashboard_dir}")
    print(f"🌐 Server starting on port {PORT}...")

    Handler = MyHTTPRequestHandler

    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            url = f"http://localhost:{PORT}"
            print(f"\n✅ Dashboard is running!")
            print(f"\n🔗 Open in browser: \033[92m{url}\033[0m")
            print(f"\n⌨️  Keyboard Shortcuts:")
            print("   R - Refresh all questions")
            print("   F - Toggle fullscreen")
            print("   1-5 - Filter by category")
            print(f"\n💡 Press Ctrl+C to stop the server\n")
            print("="*60 + "\n")

            # Automatically open browser
            try:
                webbrowser.open(url)
                print(f"🌍 Opening browser automatically...\n")
            except:
                pass

            httpd.serve_forever()

    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!\n")
        sys.exit(0)
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print(f"\n❌ Error: Port {PORT} is already in use!")
            print(f"   Try: lsof -i :{PORT} to see what's using it")
            print(f"   Or change PORT in this script\n")
        else:
            print(f"\n❌ Error: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
