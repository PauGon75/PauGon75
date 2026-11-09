"""Build the three link-button SVGs (dark + light). Original code for PauGon75."""
import html
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
W, H = 300, 56
BUTTONS = [("portfolio", "Portfolio", "paugon75.github.io/PauGon75"),
           ("linkedin", "LinkedIn", "in/paugonzalezcayuela"),
           ("itch", "itch.io", "paugonzalez.itch.io")]
# One dark button works on both GitHub themes.
THEMES = {"": dict(bg="#161b22", border="#30363d", key="#ffa657", val="#8b949e")}
for slug, label, sub in BUTTONS:
    for name, t in THEMES.items():
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Consolas, 'DejaVu Sans Mono', 'Courier New', monospace">
<rect x="4" y="4" width="{W-8}" height="{H-8}" rx="8" fill="{t['bg']}" stroke="{t['border']}" stroke-width="1.5"/>
<text x="{W/2}" y="26" text-anchor="middle" font-size="15" font-weight="bold" fill="{t['key']}">[ {html.escape(label)} ]</text>
<text x="{W/2}" y="43" text-anchor="middle" font-size="11" fill="{t['val']}">{html.escape(sub)}</text>
</svg>'''
        (ROOT/f"link_{slug}.svg").write_text(svg, encoding="utf-8")
print("links ok")
