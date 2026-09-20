# -*- coding: utf-8 -*-
"""KCC Code Club — shared print styling for the Game Makers pack.

Renders the markdown sources to A4 PDFs that share the slide decks' design
language: the same typefaces, the same maroon/gold/green palette taken from the
club logo, and the same Scratch-block rendering — tuned so it survives a
black-and-white photocopy.
"""
import base64, os, re, html as _html
import markdown

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
FONTDIR = os.path.join(ASSETS, "fonts")
LOGO = os.path.join(ASSETS, "kcc-logo.png")

# ---------------------------------------------------------------- palette
CREAM   = "#FBF5E8"
CREAM2  = "#F4E9D2"
PAPER   = "#FFFFFF"
DARK    = "#3A121B"
GOLD    = "#C9A227"
GOLDTX  = "#8A6712"
GREEN   = "#2E6B3A"
MAROON  = "#8C2332"
INK     = "#2E1015"
BODY    = "#4A3A36"
LINE    = "#DCCBA8"

# Scratch categories: (hue used for the ink/edge, target print luminance).
# The luminance targets are deliberately spread so the fills stay apart on a
# mono photocopier; the ink edge and the category tag carry the rest.
CATS = {
    "events":    ("#B88900", 0.93),
    "control":   ("#B8770E", 0.78),
    "sound":     ("#93308F", 0.72),
    "looks":     ("#6B3FB8", 0.68),
    "operators": ("#2A7A2A", 0.64),
    "motion":    ("#2A5FA8", 0.59),
    "sensing":   ("#1F6A88", 0.51),
    "variables": ("#B35C00", 0.44),
    "myblocks":  ("#A83A5E", 0.36),
    "plain":     ("#6E6058", 0.89),
}
CAT_LABEL = {
    "events": "Events", "looks": "Looks", "control": "Control", "sound": "Sound",
    "motion": "Motion", "operators": "Operators", "sensing": "Sensing",
    "variables": "Variables", "myblocks": "My Blocks", "plain": "",
}


def _srgb_to_lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _lum(rgb):
    r, g, b = [_srgb_to_lin(c) for c in rgb]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _mix(rgb, t):
    """Blend toward white by t (0 = hue, 1 = white)."""
    return tuple(round(c + (255 - c) * t) for c in rgb)


def tint_for(hexhue, target):
    """The tint of this hue whose relative luminance is `target`."""
    base = _hex2rgb(hexhue)
    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if _lum(_mix(base, mid)) < target:
            lo = mid
        else:
            hi = mid
    r, g, b = _mix(base, (lo + hi) / 2)
    return "#%02X%02X%02X" % (r, g, b)


FILLS = {k: tint_for(v[0], v[1]) for k, v in CATS.items()}
INKS = {k: v[0] for k, v in CATS.items()}


# ---------------------------------------------------------------- assets
def _b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def font_face(family, pkg, weights):
    out = []
    for w in weights:
        p = os.path.join(FONTDIR, "%s-%d.woff2" % (pkg, w))
        if not os.path.exists(p):
            continue
        out.append("@font-face{font-family:'%s';font-style:normal;font-weight:%d;"
                   "src:url(data:font/woff2;base64,%s) format('woff2');}"
                   % (family, w, _b64(p)))
    return "".join(out)


def fonts_css():
    return (font_face("Fredoka", "fredoka", [400, 500, 600, 700])
            + font_face("Nunito Sans", "nunito-sans", [400, 600, 700, 800]))


def logo_uri():
    return "data:image/png;base64," + _b64(LOGO)


# ---------------------------------------------------------------- blocks
OPENERS = re.compile(r'^(forever|repeat\b|if\b.*\bthen\b|else\b|repeat until\b)', re.I)

RULES = [
    ("myblocks",  [r'^define\b', r'^reset object\b', r'^celebrate\b']),
    ("events",    [r'^when\b', r'^broadcast\b']),
    ("control",   [r'^forever\b', r'^repeat\b', r'^wait\b', r'^if\b', r'^else\b', r'^stop\b']),
    ("sensing",   [r'touching\b', r'\bkey .*pressed\?', r'^ask\b', r'\banswer\b', r'mouse']),
    ("operators", [r'pick random', r'^join\b', r'\bjoin \[']),
    ("variables", [r'^set \[', r'^change \[', r'\bvariable\b',
                   r'^set (score|lives|level|speed|clicks|timeleft|highscore)\b',
                   r'^change (score|lives|level|speed|clicks|timeleft|highscore)\b']),
    ("motion",    [r'^move\b', r'^turn\b', r'^go to\b', r'^change [xy] by', r'^set [xy] to',
                   r'^glide\b', r'^point in direction', r'if on edge']),
    ("looks",     [r'^say\b', r'^think\b', r'^switch costume', r'^next costume',
                   r'^change size', r'^set size', r'^switch backdrop', r'^show\b', r'^hide\b']),
    ("sound",     [r'^start sound', r'^play sound', r'^stop all sounds']),
]


# Checked before everything: blocks whose leading word belongs to another
# category ("if on edge, bounce" is Motion, not Control).
PRIORITY = [("motion", r'^if on edge')]


def classify(text):
    low = text.strip().lower()
    for cat, p in PRIORITY:
        if re.search(p, low):
            return cat
    # A block belongs to the category of the block itself, so anchored rules
    # (what the block starts with) beat rules that merely appear inside it —
    # otherwise "go to x: (pick random ...)" reads as an Operators block.
    for anchored in (True, False):
        for cat, pats in RULES:
            for p in pats:
                if p.startswith("^") == anchored and re.search(p, low):
                    return cat
    return "plain"


def _indent_unit(lines):
    widths = [len(l) - len(l.lstrip(" ")) for l in lines if l.strip() and l.startswith(" ")]
    return min(widths) if widths else 4


def parse_stack(src):
    """Indented pseudo-Scratch -> nested [(text, cat, [children])]."""
    lines = [l.rstrip() for l in src.split("\n") if l.strip()]
    unit = _indent_unit(lines) or 4
    root, stack = [], [(-1, None)]
    for l in lines:
        ind = (len(l) - len(l.lstrip(" "))) // unit
        node = [l.strip(), classify(l), []]
        while stack and stack[-1][0] >= ind:
            stack.pop()
        parent = stack[-1][1]
        (root if parent is None else parent[2]).append(node)
        stack.append((ind, node))
    return root


def _blk(text, cat, tag, radius_cls=""):
    fill, ink = FILLS[cat], INKS[cat]
    label = CAT_LABEL[cat] if tag and cat != "plain" else ""
    tagspan = ('<span class="btag" style="color:%s">%s</span>' % (ink, _html.escape(label))) if label else ""
    return ('<div class="blk %s" style="background:%s;border-color:%s">'
            '<span class="bedge" style="background:%s"></span>'
            '<span class="btxt">%s</span>%s</div>'
            % (radius_cls, fill, ink, ink, _html.escape(text), tagspan))


def render_nodes(nodes, prev_cat=None):
    out = []
    for text, cat, kids in nodes:
        tag = (cat != prev_cat)
        prev_cat = cat
        if kids:
            inner, prev_cat = render_nodes(kids, prev_cat)
            out.append(
                '<div class="cwrap">%s'
                '<div class="nest" style="border-color:%s">%s</div>'
                '<div class="bfoot" style="background:%s;border-color:%s">'
                '<span class="bedge" style="background:%s"></span></div></div>'
                % (_blk(text, cat, tag, "blk-top"), INKS[cat], inner,
                   FILLS[cat], INKS[cat], INKS[cat]))
        else:
            out.append(_blk(text, cat, tag))
    return "".join(out), prev_cat


ARROW = re.compile(r'\s*(?:→|->)\s*')


def render_code(src):
    """A fenced block becomes either a block stack or a labelled chain."""
    lines = [l for l in src.split("\n") if l.strip()]
    if any(ARROW.search(l) for l in lines):
        rows = []
        for l in lines:
            label = ""
            m = re.match(r'^\s*([A-Za-z][\w \-]{0,18}):\s+(.*)$', l)
            body = l.strip()
            if m and not re.match(r'^(go to|set|say|switch|wait|repeat|if)\b', m.group(1).lower()):
                label, body = m.group(1), m.group(2)
            parts = [p for p in ARROW.split(body) if p.strip()]
            chain = '<span class="carrow">&rarr;</span>'.join(
                _blk(p.strip(), classify(p), True) for p in parts)
            rows.append('<div class="chainrow">%s<div class="chain">%s</div></div>'
                        % ('<div class="clabel">%s</div>' % _html.escape(label) if label else "", chain))
        return '<div class="stack chainstack">%s</div>' % "".join(rows)
    inner, _ = render_nodes(parse_stack(src))
    return '<div class="stack">%s</div>' % inner


# ---------------------------------------------------------------- css
def css(kind="doc", landscape=False):
    size = "A4 landscape" if landscape else "A4"
    accent = MAROON if kind == "student" else DARK
    return """
%(fonts)s
@page { size: %(size)s; margin: 15mm 14mm 16mm; }
* { box-sizing: border-box; }
html, body { margin:0; padding:0; }
body {
  font-family:'Nunito Sans', Carlito, Arial, sans-serif;
  font-size:10.4pt; line-height:1.5; color:%(body)s; background:#fff;
  -webkit-print-color-adjust:exact; print-color-adjust:exact;
}
h1,h2,h3,h4 { font-family:'Fredoka', Carlito, Arial, sans-serif; font-weight:600;
  color:%(ink)s; line-height:1.18; margin:0 0 2mm; break-after:avoid; }
h1 { font-size:21pt; color:%(accent)s; }
h2 { font-size:14.5pt; margin-top:7mm; padding-bottom:1.2mm;
     border-bottom:0.5mm solid %(line)s; }
h3 { font-size:12pt; margin-top:5mm; color:%(accent)s; }
h4 { font-size:10.6pt; margin-top:4mm; }
p { margin:0 0 2.6mm; }
strong { color:%(ink)s; font-weight:700; }
em { color:%(body)s; }
a { color:%(green)s; text-decoration:none; border-bottom:0.2mm solid %(line)s; }
code { font-family:'DejaVu Sans Mono', monospace; font-size:0.87em;
  background:%(cream2)s; border:0.2mm solid %(line)s; border-radius:1mm;
  padding:0.3mm 1.2mm; color:%(ink)s; }
hr { border:0; border-top:0.4mm solid %(line)s; margin:5mm 0; }
ul, ol { margin:0 0 3mm; padding-left:6mm; }
li { margin-bottom:1.4mm; }
blockquote { margin:3mm 0; padding:2.5mm 4mm; background:%(cream)s;
  border-left:1.2mm solid %(gold)s; border-radius:0 1.5mm 1.5mm 0; }
blockquote p:last-child { margin-bottom:0; }
blockquote.warn { background:#FDF3E2; border-left-color:%(maroon)s; }
table { border-collapse:collapse; width:100%%; margin:3mm 0 4mm; font-size:9.6pt; }
th { background:%(cream2)s; color:%(ink)s; font-weight:700; text-align:left;
  border:0.25mm solid %(line)s; padding:1.6mm 2mm; }
td { border:0.25mm solid %(line)s; padding:1.6mm 2mm; vertical-align:top; }
tr { break-inside:avoid; }

/* masthead */
.mast { display:flex; align-items:center; gap:5mm; padding-bottom:3.5mm;
  border-bottom:0.8mm solid %(accent)s; margin-bottom:5mm; }
.mast img { width:17mm; height:17mm; object-fit:contain; }
.mast .mt { flex:1; }
.mast .club { font-size:8.2pt; font-weight:800; letter-spacing:0.16em;
  text-transform:uppercase; color:%(goldtx)s; margin-bottom:0.8mm; }
.mast h1 { margin:0; }
.mast .sub { font-size:10pt; color:%(body)s; margin-top:0.8mm; }
.mast .wk { font-family:'Fredoka', sans-serif; font-size:9pt; font-weight:600;
  color:#fff; background:%(accent)s; border-radius:8mm; padding:1.4mm 4mm;
  white-space:nowrap; }

/* name line on student sheets */
.nameline { display:flex; align-items:flex-end; gap:3mm; margin:0 0 5mm;
  font-family:'Fredoka', sans-serif; font-size:11pt; color:%(ink)s; }
.nameline .rule { flex:1; border-bottom:0.4mm solid %(ink)s; height:6mm; }

/* checkbox lists */
ul.checks { list-style:none; padding-left:0; }
ul.checks li { position:relative; padding-left:7mm; margin-bottom:2mm; }
ul.checks li:before { content:""; position:absolute; left:0; top:0.9mm;
  width:4.2mm; height:4.2mm; border:0.4mm solid %(ink)s; border-radius:0.8mm;
  background:#fff; }
.tickbox { display:inline-block; width:4.2mm; height:4.2mm; border:0.4mm solid %(ink)s;
  border-radius:0.8mm; background:#fff; vertical-align:-0.7mm; margin-right:1.4mm; }

/* scratch blocks */
.stack { margin:2.5mm 0 4mm; }
.cwrap { margin-bottom:0.9mm; break-inside:avoid; }
.blk { display:flex; align-items:center; gap:2mm; border:0.3mm solid;
  break-inside:avoid;
  border-radius:1.8mm; padding:1.5mm 2.5mm 1.5mm 0; margin-bottom:0.9mm;
  overflow:hidden; break-inside:avoid; }
.blk.blk-top { border-radius:1.8mm 1.8mm 0 0; border-bottom:none;
  margin-bottom:0; }
.bedge { width:2mm; align-self:stretch; min-height:5.5mm; flex:none;
  border-radius:0.6mm 0 0 0.6mm; }
.btxt { font-family:'DejaVu Sans Mono', monospace; font-size:8.9pt;
  font-weight:700; color:#16110E; flex:1; line-height:1.3; }
.btag { font-family:'Nunito Sans', sans-serif; font-size:6.6pt; font-weight:800;
  letter-spacing:0.09em; text-transform:uppercase; white-space:nowrap;
  opacity:0.92; }
.nest { border-left:2mm solid; padding:1mm 0 0.2mm 3mm; break-inside:avoid; }
.bfoot { display:flex; align-items:stretch; height:4mm; overflow:hidden;
  border:0.3mm solid; border-top:none; border-radius:0 0 1.8mm 1.8mm; }
.bfoot .bedge { border-radius:0 0 0 0.6mm; }
.chainstack .chainrow { display:flex; align-items:center; gap:2.5mm;
  margin-bottom:1.6mm; flex-wrap:wrap; }
.chainstack .clabel { font-family:'Fredoka', sans-serif; font-weight:600;
  font-size:9pt; color:%(accent)s; min-width:16mm; }
.chainstack .chain { display:flex; align-items:center; gap:1.6mm;
  flex-wrap:wrap; flex:1; }
.chainstack .blk { margin-bottom:0; }
.carrow { color:%(body)s; font-weight:700; }

/* footer note */
.newpage { break-before:page; }
.endnote { margin-top:6mm; padding-top:2.5mm; border-top:0.4mm solid %(line)s;
  font-size:8.4pt; color:#7A6A62; }
""" % dict(fonts=fonts_css(), size=size, body=BODY, ink=INK, accent=accent,
           line=LINE, green=GREEN, cream=CREAM, cream2=CREAM2, gold=GOLD,
           goldtx=GOLDTX, maroon=MAROON)


# ---------------------------------------------------------------- markdown
EMOJI = re.compile("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\uFE0F\u2B00-\u2BFF]+")
CODEBLOCK = re.compile(r'<pre><code[^>]*>(.*?)</code></pre>', re.S)
CHECKITEM = re.compile(r'<li>\s*\[([ xX])\]\s*')


def md_to_html(text):
    html = markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"])

    def swap(m):
        return render_code(_html.unescape(m.group(1)))
    html = CODEBLOCK.sub(swap, html)

    # checkbox lists
    def mark(m):
        return '<li>'
    if CHECKITEM.search(html):
        parts = []
        for chunk in re.split(r'(<ul>.*?</ul>)', html, flags=re.S):
            if chunk.startswith("<ul>") and CHECKITEM.search(chunk):
                chunk = chunk.replace("<ul>", '<ul class="checks">', 1)
                chunk = CHECKITEM.sub(mark, chunk)
            parts.append(chunk)
        html = "".join(parts)

    # A ballot box is a form field, not decoration — turn it into a real
    # printed tick box BEFORE the emoji strip, which would otherwise eat it.
    html = html.replace("\u2610", '<span class="tickbox"></span>')
    # Emoji have no place in a printed handout — most printers render them as
    # a tofu box. Strip them and tidy the space they leave behind.
    html = EMOJI.sub("", html)
    html = re.sub(r'[ \t]+([.,!?:;])', r'\1', html)
    html = re.sub(r'[ \t]{2,}', ' ', html)
    html = re.sub(r'([>\w])\s+</(h[1-4]|p|strong|em|li)>', r'\1</\2>', html)
    # A markdown table with no header still emits a <tr> of empty <th>; that
    # prints as a stray coloured bar, so drop it.
    html = re.sub(r'<thead>\s*<tr>(?:\s*<th[^>]*>\s*</th>)+\s*</tr>\s*</thead>',
                  '', html)
    html = re.sub(r'<blockquote>\s*<p><strong>(Golden rule|Warning|Careful)',
                  r'<blockquote class="warn"><p><strong>\1', html)
    return html


def masthead(title, sub, badge, kind):
    b = '<div class="wk">%s</div>' % _html.escape(badge) if badge else ""
    s = '<div class="sub">%s</div>' % _html.escape(sub) if sub else ""
    return ('<div class="mast"><img src="%s" alt="Kerala Cultural Club">'
            '<div class="mt"><div class="club">KCC Code Club &middot; Game Makers</div>'
            '<h1>%s</h1>%s</div>%s</div>'
            % (logo_uri(), _html.escape(title), s, b))


def page(body_html, title, sub="", badge="", kind="doc", landscape=False,
         nameline=False, endnote=""):
    name = ('<div class="nameline">Name'
            '<div class="rule"></div></div>') if nameline else ""
    end = '<div class="endnote">%s</div>' % endnote if endnote else ""
    return ("<!doctype html><html><head><meta charset='utf-8'><title>%s</title>"
            "<style>%s</style></head><body>%s%s%s%s</body></html>"
            % (_html.escape(title), css(kind, landscape),
               masthead(title, sub, badge, kind), name, body_html, end))
