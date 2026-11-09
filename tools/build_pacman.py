"""Build pacman_dark.svg / pacman_light.svg: Pac-Man eating the contribution
graph (cache/calendar.json). Pure SMIL animation, no scripts. Original code."""
import json, datetime as dt
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
data = json.loads((ROOT/"cache/calendar.json").read_text())["days"]
CELL, GAP, PAD, TOP = 14, 3, 20, 30
STEP = CELL + GAP
first = dt.date.fromisoformat(data[0][0])
off = (first.weekday() + 1) % 7            # GitHub weeks start on Sunday
cells = []
for i, (d, lvl, cnt) in enumerate(data):
    k = i + off
    cells.append((k // 7, k % 7, lvl, cnt))
ncols = cells[-1][0] + 1
W = PAD*2 + ncols*STEP
H = TOP + 7*STEP + PAD + 8
SPEED = 0.045                               # seconds per cell step
THEMES = {
 "dark":  dict(bg="#0d1117", empty="#161b22", lv=["#161b22","#0e4429","#006d32","#26a641","#39d353"], pac="#ffd33d", text="#8b949e", ghost="#ff7b72"),
 "light": dict(bg="#ffffff", empty="#ebedf0", lv=["#ebedf0","#9be9a8","#40c463","#30a14e","#216e39"], pac="#e3b100", text="#57606a", ghost="#cf222e"),
}
def cx(c): return PAD + c*STEP + CELL/2
def cy(r): return TOP + r*STEP + CELL/2
# serpentine route: down column 0, up column 1, ...
route = []
for c in range(ncols):
    rows = range(7) if c % 2 == 0 else range(6, -1, -1)
    route += [(c, r) for r in rows]
t_at = {pos: i*SPEED for i, pos in enumerate(route)}
total = len(route)*SPEED
def build(name, t):
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Consolas, \'DejaVu Sans Mono\', monospace">',
         f'<rect width="{W}" height="{H}" rx="10" fill="{t["bg"]}"/>',
         f'<text x="{PAD}" y="20" font-size="12" fill="{t["text"]}">$ pacman --eat contributions  ({sum(c[3] for c in cells)} in the last year)</text>']
    for c, r, lvl, cnt in cells:
        fill = t["lv"][lvl]
        x, y = PAD + c*STEP, TOP + r*STEP
        if lvl == 0:
            o.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" fill="{fill}"/>')
        else:
            tt = t_at[(c, r)]
            o.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" fill="{fill}">'
                     f'<animate attributeName="opacity" values="1;1;0.12;0.12" keyTimes="0;{tt/total:.4f};{min(1,(tt+0.12)/total):.4f};1" dur="{total:.2f}s" repeatCount="indefinite"/></rect>')
    pts = [f"{cx(c):.1f},{cy(r):.1f}" for c, r in route]
    path = "M" + " L".join(pts)
    mouth = "M0,0 L9,-6 A10.5,10.5 0 1,0 9,6 Z"
    closed = "M0,0 L10.5,-0.8 A10.5,10.5 0 1,0 10.5,0.8 Z"
    o.append(f'<g><path d="{mouth}" fill="{t["pac"]}">'
             f'<animate attributeName="d" values="{mouth};{closed};{mouth}" dur="0.35s" repeatCount="indefinite"/></path>'
             f'<animateMotion path="{path}" dur="{total:.2f}s" rotate="auto" repeatCount="indefinite" calcMode="linear"/></g>')
    (ROOT/f"pacman_{name}.svg").write_text("\n".join(o) + "\n</svg>", encoding="utf-8")
for n, t in THEMES.items(): build(n, t)
print("pacman ok", W, H)
