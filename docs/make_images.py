"""Generates the README illustrations (docs/*.svg).

Run:  python3 docs/make_images.py
"""
from pathlib import Path
from html import escape

OUT = Path(__file__).parent
W = 820                      # image width
PAD = 24                     # outer padding
FONT = "font-family='-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif'"

C = dict(
    bg="#f6f8fa", frame="#1f2023", strip="#1f2023", tab="#2b2d31", active="#3a3c41",
    text="#e8eaed", muted="#9aa0a6", bar="#2b2d31", accent="#ff6a3d",
    ok="#2ea043", label="#24292f", sub="#57606a",
)

TAB_W, TAB_H = 150, 32


def tab(x, y, title, active=False, spare=False):
    fill = C["active"] if active else C["tab"]
    color = C["text"] if active else C["muted"]
    s = (f"<path d='M{x} {y+TAB_H} v-{TAB_H-8} q0 -8 8 -8 h{TAB_W-16} q8 0 8 8 "
         f"v{TAB_H-8} z' fill='{fill}'/>")
    if spare:
        s += (f"<rect x='{x+1.5}' y='{y+1.5}' width='{TAB_W-3}' height='{TAB_H-3}' rx='7' "
              f"fill='none' stroke='{C['accent']}' stroke-width='2' stroke-dasharray='5 4'/>")
        s += f"<text x='{x+14}' y='{y+21}' font-size='15' fill='{C['accent']}'>+</text>"
        tx = x + 30
    else:
        s += f"<circle cx='{x+18}' cy='{y+16}' r='5' fill='{color}' opacity='.7'/>"
        tx = x + 32
    s += f"<text x='{tx}' y='{y+21}' font-size='13' fill='{color}'>{escape(title)}</text>"
    return s


def badge(x, y, text, color):
    bw = 7.4 * len(text) + 20
    bx = x + TAB_W / 2 - bw / 2
    return (f"<rect x='{bx}' y='{y}' width='{bw}' height='22' rx='11' fill='{color}'/>"
            f"<text x='{x+TAB_W/2}' y='{y+15}' font-size='12' font-weight='600' fill='#fff' "
            f"text-anchor='middle'>{escape(text)}</text>")


def browser(y, tabs, address, typing=False):
    """tabs: list of dicts(title, active, spare, badge=(text,color))"""
    h = 44 + 42
    x0 = PAD
    s = f"<rect x='{x0}' y='{y}' width='{W-2*PAD}' height='{h}' rx='10' fill='{C['frame']}'/>"
    # window dots
    for i, col in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
        s += f"<circle cx='{x0+18+i*16}' cy='{y+22}' r='5' fill='{col}'/>"
    tx = x0 + 74
    badges = ""
    for t in tabs:
        s += tab(tx, y + 12, t["title"], t.get("active"), t.get("spare"))
        if t.get("badge"):
            badges += badge(tx, y - 26, *t["badge"])
        tx += TAB_W + 4
    # toolbar + address bar
    s += f"<rect x='{x0}' y='{y+44}' width='{W-2*PAD}' height='42' fill='{C['active']}'/>"
    s += f"<rect x='{x0+12}' y='{y+51}' width='{W-2*PAD-24}' height='28' rx='14' fill='{C['frame']}'/>"
    addr_color = C["text"] if address else C["muted"]
    s += (f"<text x='{x0+30}' y='{y+70}' font-size='13' fill='{addr_color}'>"
          f"{escape(address or 'Search or type a URL')}</text>")
    if typing:
        cx = x0 + 30 + 6.7 * len(address) + 2
        s += (f"<rect x='{cx}' y='{y+57}' width='1.5' height='16' fill='{C['text']}'>"
              f"<animate attributeName='opacity' values='1;0;1' dur='1s' repeatCount='indefinite'/></rect>")
    return s + badges, h


def step_label(y, n, title, desc):
    return (f"<circle cx='{PAD+12}' cy='{y}' r='12' fill='{C['label']}'/>"
            f"<text x='{PAD+12}' y='{y+4.5}' font-size='13' font-weight='700' fill='#fff' text-anchor='middle'>{n}</text>"
            f"<text x='{PAD+34}' y='{y+5}' font-size='15' font-weight='600' fill='{C['label']}'>{escape(title)}"
            f"<tspan font-weight='400' fill='{C['sub']}'>  {escape(desc)}</tspan></text>")


def figure(name, heading, steps):
    y = PAD + 10
    body = (f"<text x='{PAD}' y='{y+8}' font-size='18' font-weight='700' fill='{C['label']}'>"
            f"{escape(heading)}</text>")
    y += 44
    for i, st in enumerate(steps, 1):
        body += step_label(y, i, st["title"], st["desc"])
        y += 26 + (30 if any(t.get("badge") for t in st["tabs"]) else 4)
        b, h = browser(y, st["tabs"], st.get("address", ""), st.get("typing", False))
        body += b
        y += h + 30
    H = y - 6
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H}' viewBox='0 0 {W} {H}' {FONT}>"
           f"<rect width='{W}' height='{H}' rx='14' fill='{C['bg']}'/>{body}</svg>")
    (OUT / name).write_text(svg, encoding="utf-8")
    print("wrote", OUT / name)


SPARE = dict(title="New Tab", spare=True)

figure("how-it-works.svg", "How it works", [
    dict(title="A blank tab is always waiting on the right.", desc="",
         tabs=[dict(title="Docs", active=True), dict(title="Mail"), SPARE],
         address="example.com/docs"),
    dict(title="Click it and type your search.", desc="",
         tabs=[dict(title="Docs"), dict(title="Mail"), dict(title="New Tab", active=True)],
         address="weather istanbul", typing=True),
    dict(title="A fresh blank tab appears next to it.", desc="Automatically, in the background.",
         tabs=[dict(title="Docs"), dict(title="Mail"), dict(title="weather istanbul", active=True),
               dict(title="New Tab", spare=True, badge=("added", C["ok"]))],
         address="search.example/?q=weather+istanbul"),
])

figure("no-pile-up.svg", "Blank tabs never pile up", [
    dict(title="You open another tab with Ctrl+T.", desc="Now there are two blank tabs.",
         tabs=[dict(title="Docs"), SPARE, dict(title="New Tab", active=True, badge=("Ctrl+T", C["label"]))]),
    dict(title="You search in it.", desc="The existing blank tab is moved to the end instead of opening a new one.",
         tabs=[dict(title="Docs"), dict(title="pasta recipe", active=True),
               dict(title="New Tab", spare=True, badge=("moved", C["accent"]))],
         address="search.example/?q=pasta+recipe"),
    dict(title="Links you open land to the left of it.", desc="The blank tab stays last.",
         tabs=[dict(title="Docs"), dict(title="pasta recipe", active=True),
               dict(title="Article", badge=("from link", C["label"])), SPARE],
         address="search.example/?q=pasta+recipe"),
])
