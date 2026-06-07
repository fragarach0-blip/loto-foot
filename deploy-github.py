#!/usr/bin/env python3
"""
Déploiement GitHub Pages — branche gh-pages.
Usage : python deploy-github.py
"""
import os
import pathlib
import shutil
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent
GH_URL = 'https://github.com/fragarach0-blip/loto-foot.git'
PAGES_URL = 'https://fragarach0-blip.github.io/loto-foot'
NETLIFY_URL = 'https://melodious-figolla-46b637.netlify.app'

def run(cmd, **kw):
    subprocess.run(cmd, check=True, **kw)

def main():
    tmp = pathlib.Path(tempfile.mkdtemp())
    try:
        # Copie et adaptation du HTML
        html = (ROOT / 'loto-foot-app.html').read_text(encoding='utf-8')
        html = html.replace(NETLIFY_URL, PAGES_URL)
        (tmp / 'index.html').write_text(html, encoding='utf-8')

        # Manifest adapté pour le sous-chemin GitHub Pages
        manifest = (ROOT / 'manifest.json').read_text(encoding='utf-8')
        manifest = manifest.replace('"start_url": "loto-foot-app.html"', '"start_url": "/loto-foot/"')
        (tmp / 'manifest.json').write_text(manifest, encoding='utf-8')

        for f in ['sw.js', 'icon.svg']:
            shutil.copy(ROOT / f, tmp / f)

        # Push vers gh-pages
        run(['git', 'init'], cwd=tmp)
        run(['git', 'checkout', '-b', 'gh-pages'], cwd=tmp)
        run(['git', 'config', 'user.email', 'fragarach0@gmail.com'], cwd=tmp)
        run(['git', 'config', 'user.name', 'Charlotte'], cwd=tmp)
        run(['git', 'add', '.'], cwd=tmp)
        run(['git', 'commit', '-m', 'Deploy'], cwd=tmp)
        run(['git', 'remote', 'add', 'origin', GH_URL], cwd=tmp)
        run(['git', 'push', '-f', 'origin', 'gh-pages'], cwd=tmp)

        print(f'\nDeploy OK : {PAGES_URL}/\n')
        print('Active GitHub Pages dans Settings > Pages > Branch: gh-pages / root')
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

if __name__ == '__main__':
    main()
