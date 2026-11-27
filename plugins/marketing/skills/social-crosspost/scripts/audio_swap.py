"""Give a video a new background track while keeping its voices.

Used for TikTok when YouTube has blocked an episode for claimed music: the episode is
held (posts.tiktok.status = HELD_SOUND_SWAP on the history branch) until a claim-free
track is available, then this swaps the sound before it goes to Buffer.

How: Demucs (open-source source separation) pulls the voices out of the original mix,
the new track is looped/trimmed to the video's length, ducked under the voices, and the
result is muxed back with the untouched picture (video stream copied, not re-encoded).

Settings:
  TIKTOK_SWAP_MUSIC      a file, or a folder of .mp3/.wav/.m4a files (one is picked per
                         episode, so episodes don't all share one track). Unset or empty
                         = no swap possible, held episodes stay held.
  SWAP_MUSIC_GAIN_DB     level of the new track under the voices (default -15)
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from common import PlatformError, env, log

HELD = "HELD_SOUND_SWAP"
MUSIC_EXT = {".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg"}


def music_files() -> list[Path]:
    raw = (env("TIKTOK_SWAP_MUSIC", "") or "").strip()
    if not raw:
        return []
    p = Path(raw)
    if p.is_file():
        return [p]
    if p.is_dir():
        return sorted(f for f in p.iterdir() if f.suffix.lower() in MUSIC_EXT)
    return []


def ready() -> bool:
    return bool(music_files())


def pick_music(media_id: str) -> Path:
    files = music_files()
    if not files:
        raise PlatformError("No claim-free track set (TIKTOK_SWAP_MUSIC); episode stays held")
    i = int(hashlib.sha1(media_id.encode()).hexdigest(), 16) % len(files)
    return files[i]


def _run(cmd: list[str]) -> str:
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise PlatformError(f"{Path(cmd[0]).name} failed: {(r.stderr or r.stdout)[-600:]}")
    return r.stdout


def duration(path: Path) -> float:
    out = _run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)])
    return float(json.loads(out)["format"]["duration"])


def _mean_db(path: Path) -> float:
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af", "volumedetect", "-f", "null", "-"],
                       capture_output=True, text=True)
    for line in r.stderr.splitlines():
        if "mean_volume:" in line:
            return float(line.split("mean_volume:")[1].split("dB")[0])
    return -99.0


def _ensure_demucs() -> None:
    if importlib.util.find_spec("demucs"):
        return
    log("Installing Demucs (CPU) for voice separation ...")
    pip = [sys.executable, "-m", "pip", "install", "-q"]
    subprocess.run(pip + ["torch", "torchaudio", "--index-url", "https://download.pytorch.org/whl/cpu"],
                   check=False)
    _run(pip + ["demucs", "soundfile"])


def separate_voices(video: Path, work: Path) -> Path:
    """Return a WAV of the voices only (everything Demucs files as vocals)."""
    _ensure_demucs()
    mix = work / "mix.wav"
    _run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(video),
          "-vn", "-ac", "2", "-ar", "44100", str(mix)])
    _run([sys.executable, "-m", "demucs", "--two-stems=vocals", "-n", "htdemucs",
          "-o", str(work / "sep"), str(mix)])
    vocals = work / "sep" / "htdemucs" / "mix" / "vocals.wav"
    if not vocals.exists():
        raise PlatformError("Demucs produced no voice track")
    return vocals


def swap(video: Path, music: Path, out: Path | None = None) -> dict:
    """Write <video>_newsound.mp4: original picture + original voices + `music`."""
    out = out or video.with_name(video.stem + "_newsound.mp4")
    gain = float(env("SWAP_MUSIC_GAIN_DB", "-15"))
    dur = duration(video)
    work = Path(tempfile.mkdtemp(prefix="swap_"))
    try:
        vocals = separate_voices(video, work)
        voice_db = _mean_db(vocals)
        fade_out = max(0.0, dur - 1.5)
        graph = (
            f"[2:a]aformat=sample_rates=44100:channel_layouts=stereo,atrim=0:{dur:.3f},asetpts=N/SR/TB,"
            f"afade=t=in:d=0.4,afade=t=out:st={fade_out:.3f}:d=1.5,volume={gain}dB[m];"
            f"[1:a]aformat=sample_rates=44100:channel_layouts=stereo,apad=whole_dur={dur:.3f},asplit=2[v][key];"
            f"[m][key]sidechaincompress=threshold=0.03:ratio=4:attack=15:release=350[md];"
            f"[v][md]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.93[a]"
        )
        _run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
              "-i", str(video), "-i", str(vocals), "-stream_loop", "-1", "-i", str(music),
              "-filter_complex", graph, "-map", "0:v:0", "-map", "[a]",
              "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{dur:.3f}",
              "-movflags", "+faststart", str(out)])
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return {"path": out, "music": music.name, "voice_mean_db": round(voice_db, 1)}
