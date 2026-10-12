"""Original score for the Uvaré Discovery Set reel.

Composed in code and rendered with FluidR3_GM samples (MIT, via
gleitz/midi-js-soundfonts), so the track is fully royalty-free.
72 BPM, 4/4: one bar = 3.333s; video cuts land on bar lines.

usage: python3 -I src/compose_music.py <samples_dir> <out.wav>
Samples dir holds <instrument>/<Note><octave>.mp3 (fetched by fetch_samples.sh).
"""
import os, subprocess, sys
import numpy as np

SR = 44100
BPM = 72
BEAT = 60 / BPM
BAR = 4 * BEAT
TOTAL = 24.0
rng = np.random.default_rng(7)

NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
def note_name(m): return f"{NAMES[m % 12]}{m // 12 - 1}"
def n(s):
    # "F#4" / "Bb3" -> midi
    base = {"C":0,"D":2,"E":4,"F":5,"G":7,"A":9,"B":11}[s[0]]
    rest = s[1:]
    if rest.startswith("#"): base += 1; rest = rest[1:]
    elif rest.startswith("b"): base -= 1; rest = rest[1:]
    return base + 12 * (int(rest) + 1)

SAMPLES, _cache = sys.argv[1], {}
def sample(inst, m):
    key = (inst, m)
    if key not in _cache:
        path = os.path.join(SAMPLES, inst, note_name(m) + ".mp3")
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                             capture_output=True, check=True).stdout
        _cache[key] = np.frombuffer(raw, dtype=np.float32).copy()
    return _cache[key]

out = np.zeros((2, int(SR * (TOTAL + 1))), dtype=np.float32)
def place(inst, m, t, dur, vel, pan=0.0, attack=0.005, release=0.6):
    s = sample(inst, m)
    length = min(len(s), int(SR * (dur + release)))
    s = s[:length].copy()
    a = max(1, int(SR * attack)); s[:a] *= np.linspace(0, 1, a)
    r = min(length, int(SR * release)); s[-r:] *= np.linspace(1, 0, r) ** 2
    i = int(SR * t)
    if i >= out.shape[1]: return
    s = s[: out.shape[1] - i]
    g = vel * np.array([np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)])
    out[:, i:i + len(s)] += g[:, None] * s

def sustain(inst, m, t, dur, vel, pan=0.0, attack=0.8, release=1.2):
    # Long notes: overlap re-triggers of the sample with slow fades.
    seg, step = 3.0, 2.2
    k = 0.0
    while k < dur:
        place(inst, m, t + k, min(seg, dur - k + 0.4), vel, pan, attack=attack if k == 0 else 0.9, release=release)
        k += step

# chord voicings per half-bar: (bass, strings, piano arpeggio tones)
C = {
    "Dmaj9":  (["D2"], ["A3", "D4", "F#4", "C#5"], ["D3", "A3", "E4", "F#4", "A4", "C#5"]),
    "Bm9":    (["B1"], ["A3", "D4", "F#4", "C#5"], ["B2", "F#3", "C#4", "D4", "F#4", "A4"]),
    "Gmaj7":  (["G1"], ["B3", "D4", "F#4", "A4"],  ["G2", "D3", "A3", "B3", "D4", "F#4"]),
    "Asus":   (["A1"], ["A3", "D4", "E4", "B4"],   ["A2", "E3", "B3", "D4", "E4", "B4"]),
    "A":      (["A1"], ["A3", "C#4", "E4", "B4"],  ["A2", "E3", "B3", "C#4", "E4", "A4"]),
    "D/F#":   (["F#2"],["A3", "D4", "F#4", "E5"],  ["F#2", "D3", "A3", "E4", "F#4", "A4"]),
    "Gmaj9":  (["G1"], ["B3", "D4", "F#4", "A4"],  ["G2", "D3", "A3", "B3", "F#4", "A4"]),
}
# (bar start index, chord, length in bars)
PROG = [(0, "Dmaj9", 1), (1, "Bm9", 1), (2, "Gmaj7", 1), (3, "Asus", 0.5), (3.5, "A", 0.5),
        (4, "D/F#", 1), (5, "Gmaj9", 0.5), (5.5, "Asus", 0.5), (6, "Dmaj9", 1.2)]

EIGHTH = BEAT / 2
PATTERN = [0, 1, 2, 3, 4, 3, 5, 2]  # index into arpeggio tones
for bar, name, length in PROG:
    t0 = bar * BAR
    bass, strings, arp = C[name]
    last = bar == 6
    # bass: low piano + soft string root
    for b in bass:
        place("acoustic_grand_piano", n(b), t0, BAR * length, 0.55 if not last else 0.7, -0.1, release=1.5)
    # strings enter from bar 2, swelling in
    if bar >= 1:
        sv = 0.11 + 0.025 * min(bar, 5)
        for j, s in enumerate(strings):
            sustain("string_ensemble_1", n(s), t0, BAR * length + (2.5 if last else 0.15), sv, pan=-0.5 + j / 3)
    # warm pad bed throughout
    for s in strings[:3]:
        sustain("pad_2_warm", n(s) - 12, t0, BAR * length + (2.5 if last else 0.15), 0.07, pan=0.0, attack=1.2)
    # piano arpeggio (8ths), humanised
    if not last:
        steps = int(round(8 * length))
        for k in range(steps):
            idx = PATTERN[(k + (4 if bar % 1 else 0)) % 8]
            tone = n(arp[idx])
            t = t0 + k * EIGHTH + rng.normal(0, 0.008)
            vel = (0.30 if k % 4 == 0 else 0.22) * (0.75 if bar == 0 else 1.0) * rng.uniform(0.9, 1.08)
            place("acoustic_grand_piano", tone, max(0, t), EIGHTH * 2, vel, pan=0.15 * np.sin(k), release=1.4)

# Simple top-line melody on the piano from bar 3 (sparse, upper register)
MELODY = [(2.0, "F#5", 1.5), (2.5, "E5", 0.5), (3.0, "D5", 0.75), (3.5, "C#5", 0.5),
          (4.0, "A5", 1.25), (4.75, "F#5", 0.25), (5.0, "B5", 0.5), (5.5, "A5", 0.5)]
for bar, note, beats_ in MELODY:
    place("acoustic_grand_piano", n(note), bar * BAR + rng.normal(0, 0.006), beats_ * BAR, 0.34, 0.2, release=1.6)

# Final chord: rolled piano + celesta sparkle on the logo (bar 7 = 20.0s)
tf = 6 * BAR
for k, s in enumerate(["D3", "A3", "E4", "F#4", "A4", "C#5", "E5"]):
    place("acoustic_grand_piano", n(s), tf + k * 0.06, 4.0, 0.3, -0.3 + k * 0.1, release=2.0)
for k, s in enumerate(["A5", "D6", "F#6", "A6", "C#7"]):
    place("celesta", n(s), tf + 0.35 + k * 0.17, 1.5, 0.16, 0.4 - k * 0.15, release=2.0)

# Reverb: stereo convolution with a decaying-noise impulse response (2.8s)
L = int(SR * 2.8)
tt = np.arange(L) / SR
env = np.exp(-tt * 2.6) * (1 - np.exp(-tt * 200))
ir = np.stack([rng.normal(0, 1, L) * env, rng.normal(0, 1, L) * env]).astype(np.float32)
ir /= np.sqrt((ir ** 2).sum(axis=1, keepdims=True))
def fftconv(x, h):
    N = 1 << int(np.ceil(np.log2(len(x) + len(h))))
    return np.fft.irfft(np.fft.rfft(x, N) * np.fft.rfft(h, N), N)[: len(x)]
wet = np.stack([fftconv(out[c], ir[c]) for c in range(2)])
mix = 0.72 * out + 0.42 * wet

# Fade in/out to the video length, normalise to about -1 dBFS
end = int(SR * TOTAL)
mix = mix[:, :end]
fi = int(SR * 0.4); mix[:, :fi] *= np.linspace(0, 1, fi)
fo = int(SR * 2.2); mix[:, -fo:] *= np.linspace(1, 0, fo) ** 1.5
mix = np.tanh(mix / np.abs(mix).max() * 1.1) / np.tanh(1.1) * 0.89
pcm = (mix.T * 32767).astype("<i2").tobytes()
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "2", "-i", "-", sys.argv[2]],
               input=pcm, check=True)
print("wrote", sys.argv[2])
