"""Synthesize an original, claim-free backing track ("Kings Groove") from scratch.

Every sound is generated here from sine waves and noise (no samples), so nothing in it
can match a Content ID reference. Needs numpy.
Usage: python make_backing_track.py out.wav [seconds] [seed]
"""
import sys
import wave

import numpy as np

SR = 44100
BPM = 112
BEAT = 60 / BPM
BAR = 4 * BEAT
rng = np.random.default_rng(int(sys.argv[3]) if len(sys.argv) > 3 else 7)


def env_exp(n, tau):
    t = np.arange(n) / SR
    return np.exp(-t / tau)


def adsr(n, a=0.005, r=0.05):
    e = np.ones(n)
    na, nr = int(a * SR), int(r * SR)
    na, nr = min(na, n), min(nr, n)
    if na:
        e[:na] = np.linspace(0, 1, na)
    if nr:
        e[-nr:] *= np.linspace(1, 0, nr)
    return e


def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def lowpass(x, cutoff):
    # one-pole lowpass, run twice
    a = np.exp(-2 * np.pi * cutoff / SR)
    for _ in range(2):
        y = np.empty_like(x)
        acc = 0.0
        for i, v in enumerate(x):
            acc = (1 - a) * v + a * acc
            y[i] = acc
        x = y
    return x


def highpass(x, cutoff):
    return x - lowpass(x, cutoff)


# ---- instruments -------------------------------------------------------------
def kick():
    n = int(0.35 * SR)
    t = np.arange(n) / SR
    f = 45 + 95 * np.exp(-t / 0.035)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * env_exp(n, 0.11) * 0.95


_noise = rng.standard_normal(SR)


def snare():
    n = int(0.22 * SR)
    t = np.arange(n) / SR
    body = np.sin(2 * np.pi * 190 * t) * env_exp(n, 0.04) * 0.5
    nz = highpass(_noise[:n].copy(), 1500) * env_exp(n, 0.07) * 0.6
    return body + nz


HAT_BASE = highpass(_noise[: int(0.06 * SR)].copy(), 7000)


def hat(open_=False):
    n = int((0.18 if open_ else 0.05) * SR)
    src = np.resize(HAT_BASE, n)
    return src * env_exp(n, 0.06 if open_ else 0.015) * 0.28


def clap():
    n = int(0.2 * SR)
    out = np.zeros(n)
    for d in (0, 0.01, 0.02):
        k = int(d * SR)
        seg = highpass(_noise[1000:1000 + n - k].copy(), 1200) * env_exp(n - k, 0.03)
        out[k:] += seg * 0.3
    return out


def bass_note(midi, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = hz(midi)
    x = sum(np.sin(2 * np.pi * f * k * t) / k ** 1.4 for k in range(1, 7))
    x = lowpass(x, 700)
    return x * adsr(n, 0.004, 0.03) * env_exp(n, 0.5) * 0.55


def epiano(midis, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = np.zeros(n)
    for m in midis:
        f = hz(m)
        trem = 1 + 0.15 * np.sin(2 * np.pi * 5.5 * t)
        x += (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t) * env_exp(n, 0.08)
              + 0.12 * np.sin(2 * np.pi * 3.01 * f * t) * env_exp(n, 0.04)) * trem
    return x / max(1, len(midis)) * adsr(n, 0.003, 0.06) * env_exp(n, 0.35) * 0.32


def lead(midi, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = hz(midi) * (1 + 0.004 * np.sin(2 * np.pi * 5 * t) * (t > 0.08))
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) + 0.25 * np.sin(2 * ph) + 0.1 * np.sin(3 * ph)
    return x * adsr(n, 0.012, 0.06) * 0.2


def pluck(midi, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = hz(midi)
    x = np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * 2 * f * t) * env_exp(n, 0.05)
    return x * env_exp(n, 0.12) * adsr(n, 0.002, 0.02) * 0.22


# ---- arrangement -------------------------------------------------------------
def main():
    out_path = sys.argv[1]
    seconds = float(sys.argv[2]) if len(sys.argv) > 2 else 72
    n_bars = int(np.ceil(seconds / BAR))
    total = int((n_bars * BAR + 2) * SR)
    L = np.zeros(total)
    R = np.zeros(total)

    def place(sig, at, pan=0.0, gain=1.0):
        i = int(at * SR)
        j = min(total, i + len(sig))
        s = sig[: j - i] * gain
        L[i:j] += s * np.sqrt((1 - pan) / 2) * 1.414
        R[i:j] += s * np.sqrt((1 + pan) / 2) * 1.414

    # F major: F  Dm  Bb  C   (I vi IV V), roots as bass midi
    prog = [(41, [65, 69, 72, 76]), (38, [62, 65, 69, 72]), (46, [62, 65, 70, 74]), (36, [64, 67, 70, 72])]
    bass_rhythm = [(0, 0.75, 0), (0.75, 0.25, 12), (1.5, 0.5, 0), (2.5, 0.5, 7), (3, 0.5, 0), (3.5, 0.5, 10)]
    melody_bank = [
        [(0, 0.5, 72), (0.5, 0.5, 74), (1, 1, 77), (2.5, 0.5, 74), (3, 1, 72)],
        [(0, 0.5, 69), (0.5, 0.5, 72), (1, 0.5, 74), (1.5, 1.5, 72), (3.5, 0.5, 69)],
        [(0, 1, 70), (1, 0.5, 69), (1.5, 0.5, 67), (2, 1, 65), (3, 1, 67)],
        [(0, 0.5, 67), (0.5, 0.5, 69), (1, 0.5, 70), (1.5, 0.5, 72), (2, 2, 76)],
    ]

    for b in range(n_bars):
        t0 = b * BAR
        root, chord = prog[b % 4]
        section = b // 4  # 0 intro, then groove; every 4th section a lighter break
        intro = section == 0
        brk = section > 0 and section % 4 == 3
        # drums
        if not intro:
            for beat in range(4):
                bt = t0 + beat * BEAT
                if beat in (0, 2) or (beat == 3 and b % 2):
                    if not brk or beat == 0:
                        place(kick(), bt + (0.5 * BEAT if beat == 3 else 0), 0, 0.9)
                if beat in (1, 3):
                    place(snare(), bt, 0.05, 0.6 if not brk else 0.35)
                    place(clap(), bt, -0.1, 0.5)
                for s in range(2):
                    place(hat(open_=(s == 1 and beat == 3)), bt + s * BEAT / 2 + (0.02 * s), 0.35,
                          0.9 if s == 0 else 0.7)
        else:
            for beat in range(4):
                place(hat(), t0 + beat * BEAT, 0.35, 0.6)
        # bass
        if not intro or b % 4 >= 2:
            for st, du, iv in bass_rhythm:
                place(bass_note(root + iv, du * BEAT * 0.95), t0 + st * BEAT, 0, 0.9 if not brk else 0.6)
        # e-piano stabs on the offbeats
        for st in (0.5, 1.5, 2.75, 3.5):
            place(epiano(chord, 0.45 * BEAT), t0 + st * BEAT, -0.3, 0.9)
        # plucked arpeggio (sparkle)
        if not intro:
            for k in range(8):
                place(pluck(chord[k % 4] + 12, 0.4 * BEAT), t0 + k * BEAT / 2 + BEAT / 4, 0.45, 0.5)
        # lead melody every other phrase
        if section % 2 == 1 and not brk:
            for st, du, m in melody_bank[b % 4]:
                place(lead(m, du * BEAT * 0.92), t0 + st * BEAT, 0.15, 1.0)

    # light room reverb (a few feedback delays)
    for buf, offs in ((L, (1553, 2311, 3121)), (R, (1693, 2477, 3307))):
        wet = np.zeros_like(buf)
        for d in offs:
            wet[d:] += buf[:-d] * 0.18
        wet[4000:] += wet[:-4000] * 0.25
        buf += lowpass(wet, 5000) * 0.6

    n_out = int(seconds * SR)
    L, R = L[:n_out], R[:n_out]
    fade = int(2.0 * SR)
    ramp = np.linspace(1, 0, fade)
    L[-fade:] *= ramp
    R[-fade:] *= ramp
    peak = max(np.abs(L).max(), np.abs(R).max())
    L, R = L / peak * 0.89, R / peak * 0.89
    pcm = (np.stack([L, R], 1) * 32767).astype("<i2")
    with wave.open(out_path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


if __name__ == "__main__":
    main()
