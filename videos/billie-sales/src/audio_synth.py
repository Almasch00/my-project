"""Synthesize background music bed + SFX track for the 5-year-plan edit.
Outputs music.wav and sfx.wav (stereo, 48 kHz, float) of TOTAL seconds."""
import sys, wave
import numpy as np

SR = 48000
TOTAL = 69.0
OUT = sys.argv[1]
rng = np.random.default_rng(7)


def n(sec):
    return int(sec * SR)


def onepole_lp(x, cutoff):
    """Time-varying one-pole lowpass; cutoff may be scalar or array (Hz)."""
    cutoff = np.broadcast_to(np.asarray(cutoff, dtype=float), x.shape)
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x)
    s = 0.0
    for i in range(len(x)):
        s = (1 - a[i]) * x[i] + a[i] * s
        y[i] = s
    return y


def lp_static(x, cutoff):
    """Fast FFT brickwall-ish lowpass with soft rolloff."""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / np.sqrt(1 + (f / cutoff) ** 4)
    return np.fft.irfft(X, len(x))


def hp_static(x, cutoff):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / np.sqrt(1 + (cutoff / np.maximum(f, 1)) ** 4)
    return np.fft.irfft(X, len(x))


# ---------------------------------------------------------------- SFX
def whoosh(dur=0.55, lo=300, hi=4000, peak=0.6):
    t = np.linspace(0, 1, n(dur))
    noise = rng.standard_normal(len(t))
    sweep = lo * (hi / lo) ** np.sin(np.pi * t * 0.5 + 0.0) ** 2 * np.sin(np.pi * t) + lo
    y = onepole_lp(noise, sweep)
    y = y - onepole_lp(y, 150)
    env = np.sin(np.pi * t ** peak) ** 2
    y *= env
    return y / (np.abs(y).max() + 1e-9)


def pop(f0=900, f1=320, dur=0.12):
    t = np.arange(n(dur)) / SR
    f = f1 + (f0 - f1) * np.exp(-t / 0.018)
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.sin(ph) * np.exp(-t / 0.035)
    y[: n(0.002)] *= np.linspace(0, 1, n(0.002))
    return y / np.abs(y).max()


def swipe(dur=0.2):
    t = np.linspace(0, 1, n(dur))
    y = hp_static(rng.standard_normal(len(t)), 2500)
    y *= np.sin(np.pi * t ** 0.4) ** 2
    return y / np.abs(y).max()


def impact(dur=1.2):
    t = np.arange(n(dur)) / SR
    f = 38 + 60 * np.exp(-t / 0.08)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.35)
    crack = lp_static(rng.standard_normal(len(t)), 1800) * np.exp(-t / 0.04)
    y = boom + 0.5 * crack / (np.abs(crack).max() + 1e-9)
    y = np.tanh(1.6 * y)
    return y / np.abs(y).max()


def chime(f=1046.5, dur=2.2):
    t = np.arange(n(dur)) / SR
    y = np.zeros_like(t)
    for base in (f, f * 1.5):
        for mult, amp, dec in ((1, 1.0, 1.2), (2.76, 0.35, 0.5), (5.4, 0.15, 0.25)):
            y += amp * np.sin(2 * np.pi * base * mult * t) * np.exp(-t / dec)
    y[: n(0.003)] *= np.linspace(0, 1, n(0.003))
    return y / np.abs(y).max()


sfx = np.zeros(n(TOTAL))


def place(sig, at, gain_db):
    i = n(at)
    j = min(len(sfx), i + len(sig))
    sfx[i:j] += sig[: j - i] * 10 ** (gain_db / 20)


W = whoosh()
Wsoft = whoosh(0.45, 200, 2500)
P = pop()
Psmall = pop(1300, 600, 0.08)
S = swipe()
I = impact()
C = chime()

def ring(dur=0.9):
    t = np.arange(n(dur)) / SR
    gate = (np.floor(t / 0.05) % 2 == 0).astype(float)
    y = (np.sin(2 * np.pi * 1320 * t) + np.sin(2 * np.pi * 1660 * t)) * gate * np.exp(-t / 0.6)
    return y / np.abs(y).max()


def tick():
    return pop(2200, 1400, 0.05)


R = ring()
K = tick()
place(S, 9.62, -26)
place(I, 9.99, -19)
place(S, 14.75, -27)
place(R, 20.3, -24)
place(S, 22.2, -24)
place(S, 32.45, -26); place(S, 33.35, -26)
place(S, 50.25, -24)
place(I, 61.95, -14)


# ---------------------------------------------------------------- MUSIC
def midi(m):
    return 440 * 2 ** ((m - 69) / 12)


BPM = 100
beat = 60 / BPM
bar = 4 * beat
chords = [  # C, G, Am, F — bright corporate
    [48, 52, 55, 60, 64],  # C
    [43, 50, 55, 59, 62],  # G/B-ish
    [45, 52, 57, 60, 64],  # Am
    [41, 48, 53, 57, 60],  # F
]
music = np.zeros(n(TOTAL) + n(3))
t_all = np.arange(len(music)) / SR

# pad: one chord per bar, soft triangle-ish tones, slow attack/release
for k in range(int(TOTAL / bar) + 2):
    ch = chords[k % 4]
    start = k * bar
    L = n(bar + 1.2)
    t = np.arange(L) / SR
    env = np.minimum(1, t / 0.8) * np.where(t > bar, np.exp(-(t - bar) / 0.4), 1)
    tone = np.zeros(L)
    for m in ch:
        f = midi(m)
        for det in (-0.12, 0.12):
            ff = f * 2 ** (det / 12)
            tone += np.sin(2 * np.pi * ff * t) + 0.18 * np.sin(4 * np.pi * ff * t)
    tone *= env * 0.08
    i = n(start)
    j = min(len(music), i + L)
    music[i:j] += tone[: j - i]

# plucked arpeggio (8th notes) an octave up
arp_pat = [0, 2, 3, 4, 3, 2, 1, 2]
for k in range(int(TOTAL / (beat / 2)) + 1):
    start = k * beat / 2
    ch = chords[int(start / bar) % 4]
    m = ch[arp_pat[k % 8]] + 12
    t = np.arange(n(0.6)) / SR
    y = (np.sin(2 * np.pi * midi(m) * t) + 0.3 * np.sin(4 * np.pi * midi(m) * t)) * np.exp(-t / 0.18)
    y[: n(0.004)] *= np.linspace(0, 1, n(0.004))
    i = n(start)
    j = min(len(music), i + len(y))
    music[i:j] += 0.11 * y[: j - i]

# soft kick on 1 & 3, shaker on off-beats
for k in range(int(TOTAL / beat) + 1):
    start = k * beat
    if k % 2 == 0:
        t = np.arange(n(0.35)) / SR
        y = np.sin(2 * np.pi * np.cumsum(50 + 90 * np.exp(-t / 0.03)) / SR) * np.exp(-t / 0.12)
        g = 0.35
    else:
        y = hp_static(rng.standard_normal(n(0.08)), 6000) * np.exp(-np.arange(n(0.08)) / SR / 0.02)
        g = 0.05
    i = n(start)
    j = min(len(music), i + len(y))
    music[i:j] += g * y[: j - i]

music = lp_static(music, 5000)[: n(TOTAL)]
music /= np.abs(music).max()
# arrangement envelope: fade in, sit low, lift for end card, fade out
t = np.arange(len(music)) / SR
lvl = np.interp(t, [0, 0.8, 66.3, 67.0, TOTAL - 1.5, TOTAL], [0.0, 1.0, 1.0, 1.8, 1.8, 0.0])
music *= lvl * 10 ** (-21 / 20)


def write(path, mono, width=0.0):
    y = np.clip(mono, -1, 1)
    st = np.stack([y, y], axis=1)
    if width:  # tiny Haas widening
        d = n(0.012)
        st[d:, 1] = y[:-d] * (1 - width) + y[d:] * width
    data = (st * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())


write(f"{OUT}/sfx.wav", sfx)
print("ok", np.abs(sfx).max(), np.abs(music).max())
