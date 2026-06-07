#!/usr/bin/env python3
import hashlib
import json
import mimetypes
import os
import pathlib
import urllib.request

SITE_ID = "fb32884f-43ab-4175-b600-c64bd16bc52f"
BASE_URL = "https://api.netlify.com/api/v1"
ROOT = pathlib.Path(__file__).resolve().parent
FILES = {
    "index.html": ROOT / "loto-foot-app.html",
    "manifest.json": ROOT / "manifest.json",
    "sw.js": ROOT / "sw.js",
    "icon.svg": ROOT / "icon.svg",
}


def load_local_env():
    env_path = ROOT / ".env.local"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def request(url, token, method="GET", data=None, content_type="application/json"):
    headers = {"Authorization": f"Bearer {token}"}
    if data is not None:
        headers["Content-Type"] = content_type
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req) as response:
        return response.read()


def read_deploy_file(deploy_path, source_path):
    if deploy_path != "index.html":
        return source_path.read_bytes()
    html = source_path.read_text(encoding="utf-8")
    odds_token = os.environ.get("ODDS_API_TOKEN", "")
    if odds_token:
        html = html.replace("const ODDS_API_KEY = '';", f"const ODDS_API_KEY = '{odds_token}';")
    return html.encode("utf-8")


def main():
    load_local_env()
    token = os.environ.get("NETLIFY_TOKEN")
    if not token:
        raise SystemExit("NETLIFY_TOKEN manquant. Definis la variable puis relance le script.")

    payload_files = {}
    path_by_hash = {}
    contents = {}
    for deploy_path, source_path in FILES.items():
        data = read_deploy_file(deploy_path, source_path)
        contents[deploy_path] = data
        file_hash = hashlib.sha1(data).hexdigest()
        payload_files[deploy_path] = file_hash
        path_by_hash[file_hash] = deploy_path

    payload = json.dumps({"files": payload_files}).encode("utf-8")
    deploy = json.loads(
        request(
            f"{BASE_URL}/sites/{SITE_ID}/deploys",
            token,
            method="POST",
            data=payload,
        )
    )

    deploy_id = deploy["id"]
    required = deploy.get("required", list(FILES.keys()))
    for required_item in required:
        deploy_path = required_item if required_item in contents else path_by_hash[required_item]
        data = contents[deploy_path]
        content_type = mimetypes.guess_type(deploy_path)[0] or "application/octet-stream"
        request(
            f"{BASE_URL}/deploys/{deploy_id}/files/{deploy_path}",
            token,
            method="PUT",
            data=data,
            content_type=content_type,
        )

    url = deploy.get("ssl_url") or deploy.get("url") or "https://melodious-figolla-46b637.netlify.app"
    print(f"Deploy termine: {url}")


if __name__ == "__main__":
    main()
