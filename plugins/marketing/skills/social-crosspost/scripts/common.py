"""Shared helpers: config, token store, state file, video probing."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

_PYLIB = Path(__file__).resolve().parent.parent / ".pylib"
if _PYLIB.is_dir() and str(_PYLIB) not in sys.path:
    sys.path.insert(0, str(_PYLIB))  # packages installed with pip --target .pylib

try:
    from dotenv import load_dotenv  # optional
except ImportError:  # pragma: no cover
    load_dotenv = None

SKILL_DIR = Path(__file__).resolve().parent.parent


def data_dir() -> Path:
    """CROSSPOST_DATA_DIR, else <skill>/.data if present, else ~/.social-crosspost."""
    default = SKILL_DIR / ".data" if (SKILL_DIR / ".data").is_dir() else Path.home() / ".social-crosspost"
    d = Path(os.environ.get("CROSSPOST_DATA_DIR", default)).expanduser()
    d.mkdir(parents=True, exist_ok=True)
    return d


def load_config() -> None:
    """Load .env from the data dir first, then the skill dir (first value wins)."""
    if load_dotenv is None:
        return
    for p in (data_dir() / ".env", SKILL_DIR / ".env", Path.cwd() / ".env"):
        if p.exists():
            load_dotenv(p, override=False)


def env(name: str, default: str | None = None, required: bool = False) -> str | None:
    val = os.environ.get(name, default)
    if required and not val:
        raise ConfigError(f"Missing setting {name}. Add it to {data_dir() / '.env'}")
    return val


class ConfigError(RuntimeError):
    pass


class PlatformError(RuntimeError):
    pass


# ---------- token store (refresh tokens rotate, so we persist the newest) ----------

def _tokens_path() -> Path:
    return data_dir() / "tokens.json"


def _fernet():
    """Fernet cipher from CROSSPOST_TOKEN_KEY, or None. Used only in the cloud, where the
    newest (rotated/refreshed) sign-ins are kept as tokens.enc next to the posting history."""
    key = os.environ.get("CROSSPOST_TOKEN_KEY")
    if not key:
        return None
    from cryptography.fernet import Fernet
    return Fernet(key.encode())


def load_tokens() -> dict:
    p = _tokens_path()
    if p.exists():
        return json.loads(p.read_text())
    enc = data_dir() / "tokens.enc"
    f = _fernet()
    if f and enc.exists():
        return json.loads(f.decrypt(enc.read_bytes()))
    return {}


def save_token(platform: str, data: dict) -> None:
    tokens = load_tokens()
    tokens[platform] = {**tokens.get(platform, {}), **data, "saved_at": int(time.time())}
    p = _tokens_path()
    p.write_text(json.dumps(tokens, indent=2))
    try:
        os.chmod(p, 0o600)
    except OSError:
        pass
    f = _fernet()
    if f:
        (data_dir() / "tokens.enc").write_bytes(f.encrypt(json.dumps(tokens).encode()))


def get_token(platform: str, key: str, env_name: str | None = None) -> str | None:
    """Newest value from tokens.json, falling back to an env var (first-time setup / CI)."""
    val = load_tokens().get(platform, {}).get(key)
    if val:
        return val
    return os.environ.get(env_name) if env_name else None


# ---------- state: which IG media were already handled, per platform ----------

def _state_path() -> Path:
    return Path(os.environ.get("CROSSPOST_STATE_FILE", data_dir() / "state.json")).expanduser()


def load_state() -> dict:
    p = _state_path()
    if p.exists():
        return json.loads(p.read_text())
    return {"baseline_at": None, "media": {}}


def save_state(state: dict) -> None:
    p = _state_path()
    tmp = p.with_name(f"{p.name}.{os.getpid()}.tmp")  # unique per process: overlapping runs don't collide
    tmp.write_text(json.dumps(state, indent=2))
    tmp.replace(p)


class _NoLock:
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def state_lock():
    """Best-effort exclusive lock around read-modify-write of state.json.

    Works between processes on one machine. On some shared/mounted folders flock is not
    honoured, so callers also re-read state right before each change to keep the race tiny.
    """
    try:
        import fcntl
    except ImportError:  # pragma: no cover (Windows)
        return _NoLock()

    class _Lock:
        def __enter__(self):
            try:
                self.f = open(data_dir() / "state.lock", "a+")
                fcntl.flock(self.f, fcntl.LOCK_EX)
            except OSError:
                self.f = None
            return self

        def __exit__(self, *exc):
            if self.f:
                try:
                    fcntl.flock(self.f, fcntl.LOCK_UN)
                finally:
                    self.f.close()
            return False

    return _Lock()


def free_space(path: Path) -> None:
    """Empty a finished download. Truncates instead of deleting, because some connected
    folders don't allow deletes; an empty file is re-downloaded if it's needed again."""
    try:
        path.unlink()
    except OSError:
        try:
            with open(path, "w"):
                pass
        except OSError:
            pass


# ---------- video helpers ----------

def probe_video(path: Path) -> dict:
    """Duration (s), width, height via ffprobe. Empty dict if ffprobe is missing."""
    if not shutil.which("ffprobe"):
        return {}
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height:format=duration", "-of", "json", str(path)],
        capture_output=True, text=True,
    )
    if out.returncode != 0:
        return {}
    info = json.loads(out.stdout or "{}")
    stream = (info.get("streams") or [{}])[0]
    dur = info.get("format", {}).get("duration")
    return {
        "duration": float(dur) if dur else None,
        "width": stream.get("width"),
        "height": stream.get("height"),
    }


def truncate(text: str, limit: int) -> str:
    text = (text or "").strip()
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)
