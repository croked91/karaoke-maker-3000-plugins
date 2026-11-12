"""Inspect or stream one selected MP3; never reads the client's OAuth storage."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import http.client
import json
import os
from pathlib import Path
import re
import ssl
import stat
import sys
import time


UPLOAD_URL = "https://karaokemaker3000.art/api/agent/audio-upload"
MAX_BYTES = 100 * 1024 * 1024
TIMEOUT_SECONDS = 120


@contextmanager
def selected_file(path):
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NONBLOCK", 0))
    try:
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            raise ValueError("Choose a regular MP3 file")
        stream = os.fdopen(descriptor, "rb")
    except BaseException:
        os.close(descriptor)
        raise
    with stream:
        yield stream


def inspect_stream(stream, filename):
    info = os.fstat(stream.fileno())
    if not stat.S_ISREG(info.st_mode) or not 0 < info.st_size <= MAX_BYTES or not filename.lower().endswith(".mp3"):
        raise ValueError("Choose a regular MP3 file of at most 100 MiB")
    digest, size = hashlib.sha256(), 0
    for chunk in iter(lambda: stream.read(1024 * 1024), b""):
        size += len(chunk)
        if size > MAX_BYTES:
            raise ValueError("The selected file exceeds 100 MiB")
        digest.update(chunk)
    stream.seek(0)
    if size != info.st_size:
        raise ValueError("The selected file changed; inspect it again")
    return {"filename": filename, "byte_size": size, "sha256": digest.hexdigest()}


def inspect_file(path):
    path = Path(path)
    with selected_file(path) as stream:
        return inspect_stream(stream, path.name)


def validate_ticket(value, selected, now=None):
    if not isinstance(value, dict) or value.get("upload_url") != UPLOAD_URL or value.get("method") != "PUT":
        raise ValueError("Use the upload ticket returned by this Karaoke service")
    project_id = value.get("project_id")
    if not isinstance(project_id, str) or not re.fullmatch(r"[0-9a-f]{32}", project_id):
        raise ValueError("The upload ticket has an invalid project")
    headers = value.get("headers")
    if (not isinstance(headers, dict) or set(headers) != {"Authorization", "Content-Type"}
            or headers.get("Content-Type") != "audio/mpeg"
            or not isinstance(headers.get("Authorization"), str)
            or not re.fullmatch(r"KaraokeUpload [A-Za-z0-9_.-]{1,8178}", headers["Authorization"])):
        raise ValueError("The upload ticket has invalid headers")
    if value.get("file") != selected or type(value.get("max_bytes")) is not int or not selected["byte_size"] <= value["max_bytes"] <= MAX_BYTES:
        raise ValueError("This upload ticket is for a different file; request a new ticket")
    try:
        expiry = datetime.fromisoformat(value["expires_at"].replace("Z", "+00:00"))
        remaining = (expiry - (now or datetime.now(timezone.utc))).total_seconds()
        if not 0 < remaining <= 600:
            raise ValueError
    except (KeyError, AttributeError, TypeError, ValueError):
        raise ValueError("The upload ticket expired; request a new ticket") from None
    return headers


def upload_file(path, ticket, *, connection_factory=http.client.HTTPSConnection):
    path = Path(path)
    with selected_file(path) as stream:
        selected = inspect_stream(stream, path.name)
        headers = validate_ticket(ticket, selected)
        connection = connection_factory("karaokemaker3000.art", timeout=TIMEOUT_SECONDS,
                                        context=ssl.create_default_context())
        deadline = time.monotonic() + TIMEOUT_SECONDS
        try:
            connection.putrequest("PUT", "/api/agent/audio-upload", skip_accept_encoding=True)
            for name, value in headers.items():
                connection.putheader(name, value)
            connection.putheader("Content-Length", str(selected["byte_size"]))
            connection.putheader("User-Agent", "karaoke-maker-plugin/0.2.0")
            connection.endheaders()
            sent = 0
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError("Upload timed out; retry the same project")
                if connection.sock is not None:
                    connection.sock.settimeout(remaining)
                sent += len(chunk)
                if sent > selected["byte_size"]:
                    raise ValueError("The selected file changed; inspect it again")
                connection.send(chunk)
            if sent != selected["byte_size"]:
                raise ValueError("The selected file changed; inspect it again")
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError("Upload timed out; retry the same project")
            if connection.sock is not None:
                connection.sock.settimeout(remaining)
            response = connection.getresponse()
            if response.status not in {200, 201}:
                # Redirects and response bodies are deliberately never followed or echoed.
                raise ValueError(f"Upload returned HTTP {response.status}; check the project before retrying")
            raw = response.read(16385)
            if len(raw) > 16384:
                raise ValueError("Unexpected upload response; check the project")
            result = json.loads(raw)
            if (not isinstance(result, dict) or result.get("project_id") != ticket["project_id"]
                    or not isinstance(result.get("status"), str) or len(result["status"]) > 80):
                raise ValueError("Unexpected upload result; check the project")
            return {"project_id": result["project_id"], "status": result["status"]}
        finally:
            connection.close()


def main(argv=None, *, stdin=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("inspect", "upload"))
    parser.add_argument("path", help="The MP3 explicitly selected by the user")
    args = parser.parse_args(argv)
    try:
        if args.action == "inspect":
            result = inspect_file(args.path)
        else:
            raw = (stdin or sys.stdin).read(16385)
            if len(raw) > 16384:
                raise ValueError("Upload ticket is too large")
            try:
                ticket = json.loads(raw)
            except (ValueError, TypeError):
                raise ValueError("Pass the upload ticket JSON through standard input") from None
            result = upload_file(args.path, ticket)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (OSError, ValueError, http.client.HTTPException):
        # File paths, signed capabilities and provider bodies stay out of tool output.
        print(json.dumps({"error": "Could not inspect or upload this MP3. Check the file and project, then request a fresh ticket if needed."}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
