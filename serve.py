"""Simple local server — run this to preview the app on your Mac or phone."""
import http.server
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
port = 8080
print(f"Serving at http://localhost:{port}")
print(f"On iPhone (same Wi-Fi): open http://<your-mac-ip>:{port}")
print("Press Ctrl+C to stop\n")
http.server.HTTPServer(("0.0.0.0", port),
    http.server.SimpleHTTPRequestHandler).serve_forever()
