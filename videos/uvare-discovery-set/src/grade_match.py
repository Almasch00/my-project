"""Grade the raw clips to match the reference reel's look, by measurement.

Reference (Salt & Stone tester reel): neutral whites, saturation ~0.13,
luma p5/p50/p95 = 0.11 / 0.67 / 0.87. For each clip we compute a white
balance (highlight neutralisation), a saturation factor and a tone curve
that maps the clip's luma percentiles onto the reference's, then encode
1080x1920 H.264. HLG HDR iPhone MOVs are tone-mapped to SDR first.

usage: python3 -I src/grade_match.py <raw_dir> <out_dir>
"""
import subprocess, sys, numpy as np

RAW, OUT = sys.argv[1], sys.argv[2]
REF_HI = np.array([0.884, 0.875, 0.845])
REF_SAT = 0.127
REF_P = (0.11, 0.67, 0.87)
HDR = ("zscale=tin=arib-std-b67:pin=bt2020:min=bt2020nc:t=linear:npl=203,format=gbrpf32le,"
       "zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p")
CLIPS = {  # name: (file, pre-filter, mid-tone target override)
    "img_1176": ("IMG_1176.MOV", HDR, None),
    "img_1179": ("IMG_1179.MOV", HDR, 0.62),
    "img_1205": ("IMG_1205.MP4", "scale=in_range=pc:out_range=tv", 0.58),
    "img_1208": ("IMG_1208.MP4", "scale=in_range=pc:out_range=tv", None),
    "img_1209": ("IMG_1209.MP4", "scale=in_range=pc:out_range=tv", None),
}

def frames(path, vf):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", vf + ",fps=2,scale=180:320,format=rgb24",
                          "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, 320, 180, 3).astype(np.float32) / 255

def measure(a):
    L = a.mean(-1)
    hi = a[L > np.percentile(L, 85)].mean(0)
    mx, mn = a.max(-1), a.min(-1)
    return hi, ((mx - mn) / (mx + 1e-6)).mean(), [np.percentile(L, p) for p in (5, 50, 95)]

for name, (src, pre, mid) in CLIPS.items():
    path = f"{RAW}/{src}"
    hi, sat, P = measure(frames(path, pre))
    # 1) white balance: make the clip's highlight tint match the reference's
    g = (REF_HI / REF_HI.mean()) / (hi / hi.mean())
    wb = f"colorchannelmixer=rr={g[0]:.4f}:gg={g[1]:.4f}:bb={g[2]:.4f}"
    a2 = np.clip(frames(path, f"{pre},{wb}"), 0, 1)
    _, sat2, P = measure(a2)
    # 2) saturation, 3) tone curve onto the reference percentiles
    s = REF_SAT / sat2
    tgt = (REF_P[0], mid or REF_P[1], REF_P[2])
    pts = [(0, 0)] + list(zip(P, tgt)) + [(1, 0.97)]
    curve = " ".join(f"{x:.3f}/{y:.3f}" for x, y in pts)
    grade = f"{wb},eq=saturation={s:.3f},curves=all='{curve}'"
    vf = f"{pre},{grade},scale=1080:1920:flags=lanczos"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-vf", vf, "-c:v", "libx264", "-preset", "slow", "-crf", "16",
                    "-pix_fmt", "yuv420p", "-r", "30", "-g", "15", "-an", "-movflags", "+faststart",
                    "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", f"{OUT}/{name}.mp4"], check=True)
    hi3, sat3, P3 = measure(frames(f"{OUT}/{name}.mp4", "null"))
    print(f"{name}: sat {sat:.3f}->{sat3:.3f}  hi {np.round(hi3,3)}  luma {np.round(P3,2)}")
