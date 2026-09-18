#!/usr/bin/env python3
"""Sync public Google Drive folder media into preshoot-media.json."""

from __future__ import annotations

import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

FOLDER_ID = "1GckkRAYaA7xPZnm4rI3InbouSqPO77U9"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "preshoot-media.json"
FOLDER_URL = f"https://drive.google.com/drive/folders/{FOLDER_ID}?usp=sharing"
EMBED_URL = f"https://drive.google.com/embeddedfolderview?id={FOLDER_ID}#grid"
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)
EMBED_ENTRY = re.compile(
    r'id="entry-([A-Za-z0-9_-]+)"[\s\S]*?'
    r"type/(image|video)/([a-zA-Z0-9.+-]+)\"[\s\S]*?"
    r'flip-entry-title">([^<]+)',
    re.IGNORECASE,
)


def fetch_html(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=90) as response:
        return response.read().decode("utf-8", "replace")


def pretty_name(name: str) -> str:
    stem = re.sub(r"\.[^.]+$", "", name)
    stem = re.sub(r"[_-]+", " ", stem).strip()
    return stem or name


def media_item(file_id: str, name: str, kind: str, mime: str) -> dict:
    return {
        "id": file_id,
        "name": pretty_name(name),
        "type": kind,
        "mime": mime,
    }


def parse_embedded(html: str) -> list[dict]:
    files: list[dict] = []
    seen: set[str] = set()
    for match in EMBED_ENTRY.finditer(html):
        file_id, kind, subtype, name = match.groups()
        if file_id in seen:
            continue
        seen.add(file_id)
        files.append(media_item(file_id, name, kind.lower(), f"{kind.lower()}/{subtype}"))
    return files


def parse_drive_ivd(html: str) -> list[dict]:
    match = re.search(r"window\['_DRIVE_ivd'\]\s*=\s*'((?:\\'|[^'])*)'", html)
    if not match:
        return []

    raw = match.group(1).encode("utf-8").decode("unicode_escape")
    data = json.loads(raw)
    entries = data[0] if data and data[0] else []
    files: list[dict] = []

    for entry in entries:
        if not isinstance(entry, list) or len(entry) < 4:
            continue
        file_id, name, mime = entry[0], entry[2], entry[3]
        if not isinstance(file_id, str) or not isinstance(name, str) or not isinstance(mime, str):
            continue
        if mime.startswith("image/"):
            kind = "image"
        elif mime.startswith("video/"):
            kind = "video"
        else:
            continue
        files.append(media_item(file_id, name, kind, mime))

    return files


def existing_files() -> list[dict]:
    if not OUT.exists():
        return []
    try:
        payload = json.loads(OUT.read_text(encoding="utf-8"))
        files = payload.get("files")
        return files if isinstance(files, list) else []
    except (OSError, json.JSONDecodeError):
        return []


def main() -> None:
    files = parse_embedded(fetch_html(EMBED_URL))
    if not files:
        files = parse_drive_ivd(fetch_html(FOLDER_URL))

    if not files:
        previous = existing_files()
        if previous:
            print(f"Drive listing was empty; keeping {len(previous)} existing file(s).", file=sys.stderr)
            sys.exit(1)
        print("Drive folder has no public photographs or films yet.", file=sys.stderr)

    files.reverse()
    payload = {
        "folderId": FOLDER_ID,
        "folderUrl": FOLDER_URL,
        "updatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "files": files,
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(files)} file(s) to {OUT}")


if __name__ == "__main__":
    main()
