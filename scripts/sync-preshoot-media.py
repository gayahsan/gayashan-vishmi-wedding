#!/usr/bin/env python3
"""Sync public Google Drive folder media into preshoot-media.json."""

from __future__ import annotations

import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

FOLDER_ID = "1GckkRAYaA7xPZnm4rI3InbouSqPO77U9"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "preshoot-media.json"
FOLDER_URL = f"https://drive.google.com/drive/folders/{FOLDER_ID}?usp=sharing"


def fetch_html() -> str:
    req = urllib.request.Request(
        FOLDER_URL,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
            )
        },
    )
    with urllib.request.urlopen(req, timeout=90) as response:
        return response.read().decode("utf-8", "replace")


def parse_files(html: str) -> list[dict]:
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
        file_id = entry[0]
        name = entry[2]
        mime = entry[3]
        if not isinstance(file_id, str) or not isinstance(name, str) or not isinstance(mime, str):
            continue
        if mime.startswith("image/"):
            media_type = "image"
        elif mime.startswith("video/"):
            media_type = "video"
        else:
            continue
        files.append(
            {
                "id": file_id,
                "name": pretty_name(name),
                "type": media_type,
                "mime": mime,
            }
        )

    return files


def pretty_name(name: str) -> str:
    stem = re.sub(r"\.[^.]+$", "", name)
    stem = re.sub(r"[_-]+", " ", stem).strip()
    return stem or name


def main() -> None:
    html = fetch_html()
    files = parse_files(html)
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
