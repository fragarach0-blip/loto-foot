#!/usr/bin/env python3
"""
Serveur local pour le Loto Foot 2026.
Sert le fichier HTML et proxifie les appels football-data.org
pour contourner les restrictions CORS en développement.

Usage :
    python dev-server.py
Puis ouvrir : http://localhost:8082/loto-foot-app.html
"""
import http.server
import urllib.request
import os

API_KEY  = '537561c0fa7943d69a67c7ad53c671f3'
FD_BASE  = 'https://api.football-data.org/v4/'
PROXY_PFX = '/api-proxy/'
PORT     = 8082

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith(PROXY_PFX):
            api_path = self.path[len(PROXY_PFX):]
            url = FD_BASE + api_path
            try:
                req = urllib.request.Request(url, headers={'X-Auth-Token': API_KEY})
                with urllib.request.urlopen(req, timeout=15) as r:
                    data = r.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(data)
            except urllib.error.HTTPError as e:
                body = e.read()
                self.send_response(e.code)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(body)
            except Exception as e:
                self.send_response(502)
                self.end_headers()
                self.wfile.write(str(e).encode())
        else:
            super().do_GET()

    def log_message(self, fmt, *args):
        if self.path.startswith(PROXY_PFX):
            print(f'[proxy] {args[0]} {self.path}')

os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(f'\nServeur local pret : http://localhost:{PORT}/loto-foot-app.html\n')
try:
    http.server.HTTPServer(('', PORT), Handler).serve_forever()
except KeyboardInterrupt:
    print('\nArret du serveur.')
