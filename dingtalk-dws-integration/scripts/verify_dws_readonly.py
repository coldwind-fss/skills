"""Run a dependency-free, read-only DWS smoke check.

The script never creates, updates, deletes, or downloads a DingTalk resource.
It reports counts and safe status only; credential-bearing CLI output is not
printed.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


SECRET_PATTERNS = (
    re.compile(r"(?i)(accessToken|refreshToken|clientSecret|appSecret)([\s:=]+)([^\s,}\"]+)"),
    re.compile(r"(?i)(authorization:\s*bearer\s+)[^\s]+"),
    re.compile(r"(?i)(device(code|_code)?|verification(code|_code)?)([\s:=]+)([^\s,}\"]+)"),
)


class DwsCheckError(RuntimeError):
    pass


def redact(value: str) -> str:
    result = value
    result = SECRET_PATTERNS[0].sub(lambda match: f"{match.group(1)}{match.group(2)}<redacted>", result)
    result = SECRET_PATTERNS[1].sub(lambda match: f"{match.group(1)}<redacted>", result)
    result = SECRET_PATTERNS[2].sub(lambda match: f"{match.group(1)}{match.group(3)}<redacted>", result)
    return result[-1600:]


def result(payload: Any) -> Any:
    if isinstance(payload, dict):
        return payload.get("result", payload.get("data", payload))
    return payload


class ReadonlyDws:
    def __init__(self, binary: str, profile: str, home: str, config_dir: str) -> None:
        self.binary = binary
        self.profile = profile
        self.home = home
        self.config_dir = config_dir

    def call(self, *args: str) -> Any:
        command = [self.binary, "--profile", self.profile, *args, "--format", "json"]
        environment = os.environ.copy()
        environment["HOME"] = self.home
        environment["DWS_CONFIG_DIR"] = self.config_dir
        try:
            completed = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                env=environment,
                timeout=60,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            raise DwsCheckError(str(error)) from error
        if completed.returncode:
            message = completed.stderr.strip() or completed.stdout.strip() or "DWS command failed"
            raise DwsCheckError(redact(message))
        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError as error:
            raise DwsCheckError("DWS returned non-JSON output for a JSON command") from error
        if isinstance(payload, dict) and (payload.get("success") is False or payload.get("status") == "error"):
            raise DwsCheckError(redact(str(payload.get("error") or payload.get("errorMsg") or payload)))
        return payload


def profile_matches(profiles: Any, expected: str) -> bool:
    if not isinstance(profiles, list):
        return False
    for item in profiles:
        if not isinstance(item, dict):
            continue
        explicit = item.get("profile")
        derived = f"{item.get('corpId')}:{item.get('userId')}" if item.get("corpId") and item.get("userId") else ""
        if str(explicit or derived) == expected:
            return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only DWS authorization and resource smoke check")
    parser.add_argument("--groups", action="store_true", help="also count visible group conversations")
    args = parser.parse_args()

    profile = os.environ.get("DWS_PROFILE", "").strip()
    home = os.environ.get("DWS_HOME", "").strip()
    config_dir = os.environ.get("DWS_CONFIG_DIR", "").strip()
    binary = os.environ.get("DWS_BINARY_PATH", "dws").strip()
    missing = [name for name, value in (("DWS_PROFILE", profile), ("DWS_HOME", home), ("DWS_CONFIG_DIR", config_dir)) if not value]
    if missing:
        print(json.dumps({"status": "configuration_error", "missing": missing}, ensure_ascii=False))
        return 2
    if shutil.which(binary) is None and not Path(binary).is_file():
        print(json.dumps({"status": "configuration_error", "error": f"DWS binary not found: {binary}"}, ensure_ascii=False))
        return 2

    client = ReadonlyDws(binary, profile, home, config_dir)
    try:
        profiles_payload = client.call("profile", "list")
        profile_list = profiles_payload.get("profiles", []) if isinstance(profiles_payload, dict) else []
        report: dict[str, Any] = {
            "status": "healthy" if profile_matches(profile_list, profile) else "profile_not_found",
            "profile_match": profile_matches(profile_list, profile),
        }
        client.call("contact", "user", "get-self")
        spaces = result(client.call("drive", "list-spaces"))
        bases = result(client.call("aitable", "base", "list"))
        report["current_user_readable"] = True
        report["drive_space_count"] = len(spaces.get("items", [])) if isinstance(spaces, dict) else 0
        report["aitable_base_count"] = len(bases.get("bases", [])) if isinstance(bases, dict) else 0
        if args.groups:
            conversations = result(client.call("chat", "list-all-conversations", "--limit", "100"))
            items = conversations.get("conversations", []) if isinstance(conversations, dict) else []
            report["group_count"] = sum(not bool(item.get("singleChat")) for item in items if isinstance(item, dict))
            report["conversation_has_more"] = bool(conversations.get("hasMore")) if isinstance(conversations, dict) else False
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["status"] == "healthy" else 1
    except DwsCheckError as error:
        print(json.dumps({"status": "failed", "error": str(error)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    sys.exit(main())
