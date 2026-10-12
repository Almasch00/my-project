"""Original 110 BPM groove for the Uvaré reel (matches the reference's tempo/energy).

Electric piano + finger bass from FluidR3_GM (MIT, via gleitz/midi-js-soundfonts);
drums (kick, snap, hats, shaker) synthesised here. Fully royalty-free.
110 BPM, 4/4: beat = 0.5455s, bar = 2.182s. 7 bars of groove under the shots,
bar 8 drops the drums for the logo.

usage: python3 -I src/compose_groove.py <samples_dir> <out.wav>
"""
import os, subprocess, sys
import numpy as np

SR = 44100
BEAT = 60 / 110
BAR = 4 * BEAT
TOTAL = 18.0
rng = np.random.default_rng(11)
N = int(SR * (TOTAL + 1))
drums = np.zeros((2, N), np.float32)
keys = np.zeros((2, N), np.float32)
bass = np.zeros((2, N), np.float32)

NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
def n(s):
    base = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}[s[0]]
    rest = s[1:]
    if rest[0] in "#b": base += 1 if rest[0] == "#" else -1; rest = rest[1:]
    return base + 12 * (int(rest) + 1)

SAMPLES, _cache = sys.argv[1], {}
def sample(inst, m):
    if (inst, m) not in _cache:
        path = os.path.join(SAMPLES, inst, f"{NAMES[m % 12]}{m // 12 - 1}.mp3")
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                             capture_output=True, check=True).stdout
        _cache[(inst, m)] = np.frombuffer(raw, np.float32).copy()
    return _cache[(inst, m)]

def add(buf, s, t, vel, pan=0.0):
    i = int(SR * t)
    if i >= N: return
    s = s[: N - i]
    g = vel * np.array([np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)])
    buf[:, i:i + len(s)] += g[:, None] * s

def note(buf, inst, m, t, dur, vel, pan=0.0, release=0.25):
    s = sample(inst, m)
    L = min(len(s), int(SR * (dur + release)))
    s = s[:L].copy()
    r = min(L, int(SR * release)); s[-r:] *= np.linspace(1, 0, r) ** 2
    s[:64] *= np.linspace(0, 1, 64)
    add(buf, s, t, vel, pan)

def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x)).astype(np.float32)

# ---- drum voices ----
def kick():
    t = np.arange(int(SR * 0.45)) / SR
    f = 48 + 90 * np.exp(-t * 38)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7.5)
    s[:200] += rng.normal(0, 0.25, 200) * np.linspace(1, 0, 200)
    return np.tanh(s * 1.6).astype(np.float32)
def snap():
    L = int(SR * 0.25); s = np.zeros(L, np.float32)
    for k, d in enumerate((0, 0.009, 0.019)):
        i = int(SR * d); b = rng.normal(0, 1, L - i) * np.exp(-np.arange(L - i) / SR * (60 if k < 2 else 22))
        s[i:] += b
    return band(s, 1100, 6500) * 0.8
def hat(open_=False):
    L = int(SR * (0.22 if open_ else 0.06))
    s = rng.normal(0, 1, L) * np.exp(-np.arange(L) / SR * (14 if open_ else 70))
    return band(s.astype(np.float32), 7000, 16000)
def shaker():
    L = int(SR * 0.09); t = np.arange(L) / SR
    s = rng.normal(0, 1, L) * np.sin(np.pi * t / t[-1]) ** 2
    return band(s.astype(np.float32), 4500, 11000)
K, SN, SH = kick(), snap(), shaker()

GROOVE_BARS = 7
for b in range(GROOVE_BARS):
    t0 = b * BAR
    intro = b == 0
    # kick: 1, &2 (light), 3 — bar 1 only on 1 and 3
    for beat_pos, v in ((0, 0.95), (1.5, 0.45), (2, 0.8)) if not intro else ((0, 0.8), (2, 0.6)):
        add(drums, K, t0 + beat_pos * BEAT, v)
    if not intro:
        for beat_pos in (1, 3):
            add(drums, snap(), t0 + beat_pos * BEAT + rng.normal(0, 0.003), 0.55, 0.1)
    # swung 8th hats + 16th shaker
    for k in range(8):
        sw = 0.04 * BEAT if k % 2 else 0
        add(drums, hat(open_=(k == 7 and b % 2 == 1)), t0 + k * BEAT / 2 + sw, (0.07 if k % 2 else 0.10) * rng.uniform(0.85, 1.1), 0.35)
    for k in range(16):
        if not intro or k >= 8:
            add(drums, SH, t0 + k * BEAT / 4 + (0.02 * BEAT if k % 2 else 0), 0.035 * rng.uniform(0.7, 1.2), -0.4)
# little fill into the drop
for k, v in enumerate((0.3, 0.4, 0.55)):
    add(drums, snap(), 6 * BAR + (3 + k / 3) * BEAT, v, 0.1)

# ---- chords: Fmaj9 Em7 Dm9 Cmaj9 ----
CH = {
    "Fmaj9": ("F2", ["A3", "C4", "E4", "G4"]),
    "Em7":   ("E2", ["G3", "B3", "D4", "F#4"]),
    "Dm9":   ("D2", ["F3", "A3", "C4", "E4"]),
    "Cmaj9": ("C2", ["E3", "G3", "B3", "D4"]),
}
PROG = ["Fmaj9", "Em7", "Dm9", "Cmaj9", "Fmaj9", "Em7", "Dm9"]
for b, name in enumerate(PROG):
    t0 = b * BAR
    root, voicing = CH[name]
    for pos, dur, v in ((0, 1.4, 0.30), (1.5, 0.4, 0.22), (2.5, 1.4, 0.26)):
        for j, s in enumerate(voicing):
            note(keys, "electric_piano_1", n(s), t0 + pos * BEAT + j * 0.006, dur * BEAT, v, -0.3 + j * 0.2)
    if b > 0:
        r = n(root)
        for pos, m, dur in ((0, r, 1.3), (1.5, r, 0.4), (2.5, r + 7, 0.9), (3.5, r + 12, 0.4)):
            note(bass, "electric_bass_finger", m, t0 + pos * BEAT, dur * BEAT, 0.6)
# top-line hook bars 5-7
for bar, pos, s, d in ((4, 0, "E5", 1), (4, 1.5, "G5", 0.5), (4, 2, "A5", 1.5), (5, 0, "G5", 1), (5, 1.5, "F#5", 0.5),
                       (5, 2, "D5", 1.5), (6, 0, "F5", 1), (6, 1.5, "E5", 0.5), (6, 2, "C5", 1.5)):
    note(keys, "electric_piano_1", n(s), bar * BAR + pos * BEAT, d * BEAT, 0.24, 0.2, release=0.4)
# bar 8 — the drop: Cmaj9 rings out for the logo
tf = 7 * BAR
for j, s in enumerate(["C3", "G3", "B3", "D4", "E4", "G4"]):
    note(keys, "electric_piano_1", n(s), tf + j * 0.03, 2.6, 0.32, -0.3 + j * 0.12, release=1.2)
note(bass, "electric_bass_finger", n("C2"), tf, 2.0, 0.6, release=0.8)

# ---- mix ----
def reverb(x, secs, decay, mix):
    L = int(SR * secs); tt = np.arange(L) / SR
    env = np.exp(-tt * decay) * (1 - np.exp(-tt * 300))
    out = np.empty_like(x)
    for c in range(2):
        ir = (rng.normal(0, 1, L) * env).astype(np.float32); ir /= np.sqrt((ir ** 2).sum())
        M = 1 << int(np.ceil(np.log2(x.shape[1] + L)))
        out[c] = np.fft.irfft(np.fft.rfft(x[c], M) * np.fft.rfft(ir, M), M)[: x.shape[1]]
    return x + mix * out

# kick-keyed duck on keys for pump
duck = np.ones(N, np.float32)
for b in range(1, GROOVE_BARS):
    for pos in (0, 2):
        i = int(SR * (b * BAR + pos * BEAT)); L = int(SR * 0.25)
        duck[i:i + L] = np.minimum(duck[i:i + L], 1 - 0.35 * np.exp(-np.arange(L) / SR * 12))
keys *= duck
mix = 0.7 * reverb(drums, 0.6, 9, 0.25) + 1.25 * reverb(keys, 2.2, 3.2, 0.5) + bass * 1.0
end = int(SR * TOTAL); mix = mix[:, :end]
fi = int(SR * 0.05); mix[:, :fi] *= np.linspace(0, 1, fi)
fo = int(SR * 1.2); mix[:, -fo:] *= np.linspace(1, 0, fo) ** 1.5
mix = np.tanh(mix / np.abs(mix).max() * 1.4) / np.tanh(1.4) * 0.89
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "2", "-i", "-", sys.argv[2]],
               input=(mix.T * 32767).astype("<i2").tobytes(), check=True)
print("wrote", sys.argv[2])
