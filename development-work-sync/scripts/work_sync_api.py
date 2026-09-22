"""Secure, browser-free transport for the development-work-sync skill.

The token is loaded from the process environment or a user-only credential
file. It is never accepted as a command-line argument and is never printed.
The script intentionally exposes only the PM work-intake read/write routes.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


DEFAULT_API_BASE = "https://xzkj.flipbeltchina.com/pm/api"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def _credential_file() -> Path:
    configured = str(os.getenv("PM_WORK_SYNC_CREDENTIAL_FILE") or "").strip()
    if configured:
        return Path(configured)
    profile = Path(os.environ.get("USERPROFILE") or Path.home())
    return profile / ".pm-work-sync" / "development-work-sync.token"


def _load_token() -> str:
    token = str(os.getenv("PM_WORK_SYNC_TOKEN") or "").strip()
    if token:
        return token
    path = _credential_file()
    try:
        token = path.read_text(encoding="utf-8").strip()
    except (OSError, UnicodeError):
        token = ""
    if len(token) < 32:
        return ""
    return token


def _request(method: str, path: str, payload: dict | None = None):
    base = str(os.getenv("PM_WORK_SYNC_API_BASE") or DEFAULT_API_BASE).rstrip("/")
    token = _load_token()
    if not token:
        raise RuntimeError(
            "缺少工作同步服务凭证。请配置 PM_WORK_SYNC_TOKEN 或用户安全凭证文件，未执行任何写入。"
        )
    body = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {"Accept": "application/json", "X-PM-Work-Sync-Token": token}
    if body is not None:
        headers["Content-Type"] = "application/json"
    request = Request(base + path, data=body, headers=headers, method=method)
    try:
        with urlopen(request, timeout=30) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            detail = json.loads(raw)
        except json.JSONDecodeError:
            detail = {"error": raw[:1000]}
        raise RuntimeError(f"PM API {exc.code}: {json.dumps(detail, ensure_ascii=False)}") from exc
    except URLError as exc:
        raise RuntimeError(f"PM API 连接失败：{exc.reason}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description="Development work sync API transport")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("schema")
    sub.add_parser("projects")
    requirements = sub.add_parser("requirements")
    requirements.add_argument("--project-id", required=True)
    batch = sub.add_parser("batch")
    batch.add_argument("--batch-id", required=True)
    sync = sub.add_parser("sync")
    sync.add_argument("--payload-file", required=True)
    owners = sub.add_parser("owner-correction")
    owners.add_argument("--payload-file", required=True)
    rollback = sub.add_parser("rollback")
    rollback.add_argument("--batch-id", required=True)
    args = parser.parse_args()

    if args.command == "schema":
        result = _request("GET", "/work-intake/schema")
    elif args.command == "projects":
        result = _request("GET", "/projects")
    elif args.command == "requirements":
        result = _request("GET", "/requirements/live?projectId=" + quote(args.project_id, safe=""))
    elif args.command == "batch":
        result = _request("GET", "/work-intake/" + quote(args.batch_id, safe=""))
    elif args.command == "sync":
        payload = json.loads(Path(args.payload_file).read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise RuntimeError("payload 必须是 JSON 对象")
        result = _request("POST", "/work-intake", payload)
    elif args.command == "owner-correction":
        payload = json.loads(Path(args.payload_file).read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise RuntimeError("payload 必须是 JSON 对象")
        result = _request("POST", "/work-intake/owner-correction", payload)
    else:
        result = _request("POST", "/work-intake/" + quote(args.batch_id, safe="") + "/rollback", {})

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
