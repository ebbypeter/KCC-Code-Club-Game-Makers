# -*- coding: utf-8 -*-
"""Markdown -> a small JSON AST that make_editable.js renders as Word.

Kept deliberately narrow: the KCC pack only uses headings, paragraphs, tables,
bullet / numbered / checkbox lists, block quotes, rules and links.
"""
import io, json, re, sys
from html.parser import HTMLParser
import markdown

# A fill-in placeholder: [LIKE THIS], [N], or one containing INSERT. Never a
# markdown link, and never the "[ ]" left behind by a checkbox list item.
PLACEHOLDER = re.compile(r'\[[^\]\n]{1,90}\]')


def is_placeholder(s):
    if not (s.startswith("[") and s.endswith("]")):
        return False
    inner = s[1:-1].strip()
    if not inner or inner.lower() == "x":
        return False
    return bool(re.search(r'[A-Z]{2,}', inner) or re.fullmatch(r'[A-Z0-9]', inner))


BLOCK = {"p", "h1", "h2", "h3", "h4", "li", "th", "td", "blockquote"}


class Walker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks = []
        self.inline = []
        self.fmt = {"b": False, "i": False, "code": False, "link": None}
        self.stack = []
        self.list_stack = []
        self.table = None
        self.row = None
        self.in_quote = False

    # ---- inline helpers
    def push_text(self, text):
        if not text:
            return
        f = self.fmt
        for part in PLACEHOLDER.split(text) if False else [text]:
            pass
        # split out placeholders so they can be highlighted
        pos = 0
        for m in PLACEHOLDER.finditer(text):
            if is_placeholder(m.group(0)):
                if m.start() > pos:
                    self._run(text[pos:m.start()])
                self._run(m.group(0), ph=True)
                pos = m.end()
        if pos < len(text):
            self._run(text[pos:])

    def _run(self, text, ph=False):
        if not text:
            return
        if text != "\n":
            # markdown sources wrap at ~95 columns; those newlines are not
            # meaningful, so collapse them or they show up mid-sentence in Word
            text = re.sub(r'\s+', ' ', text)
            if not text.strip():
                text = " "
        self.inline.append({
            "text": text, "b": self.fmt["b"], "i": self.fmt["i"],
            "code": self.fmt["code"], "link": self.fmt["link"], "ph": ph,
        })

    def take(self):
        out = [r for r in self.inline if r["text"].strip() or len(r["text"])]
        self.inline = []
        return out

    # ---- tags
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("strong", "b"):
            self.fmt["b"] = True
        elif tag in ("em", "i"):
            self.fmt["i"] = True
        elif tag == "code":
            self.fmt["code"] = True
        elif tag == "a":
            self.fmt["link"] = a.get("href")
        elif tag == "br":
            self._run("\n")
        elif tag in ("ul", "ol"):
            self.list_stack.append({"t": tag, "items": [], "checks": False})
        elif tag == "table":
            self.table = {"t": "table", "header": [], "rows": []}
        elif tag == "tr":
            self.row = []
        elif tag == "blockquote":
            self.in_quote = True
            self.quote = []
        elif tag in BLOCK:
            self.inline = []
        if tag in ("h1", "h2", "h3", "h4", "p", "li", "th", "td"):
            self.stack.append(tag)

    def handle_data(self, data):
        if self.stack or self.inline:
            self.push_text(data)
        elif data.strip():
            self.push_text(data)

    def handle_endtag(self, tag):
        if tag in ("strong", "b"):
            self.fmt["b"] = False
        elif tag in ("em", "i"):
            self.fmt["i"] = False
        elif tag == "code":
            self.fmt["code"] = False
        elif tag == "a":
            self.fmt["link"] = None

        if tag in ("h1", "h2", "h3", "h4"):
            if self.stack and self.stack[-1] == tag:
                self.stack.pop()
            self.emit({"t": "h", "level": int(tag[1]), "text": self.take()})
        elif tag == "p":
            if self.stack and self.stack[-1] == tag:
                self.stack.pop()
            runs = self.take()
            if any(r["text"].strip() for r in runs):
                self.emit({"t": "p", "text": runs})
        elif tag == "li":
            if self.stack and self.stack[-1] == tag:
                self.stack.pop()
            runs = self.take()
            if self.list_stack:
                # "[ ] " at the start of an item is a checkbox, not text
                if runs and re.match(r'^\s*\[[ xX]\]\s*', runs[0]["text"]):
                    runs[0] = dict(runs[0], text=re.sub(r'^\s*\[[ xX]\]\s*', '', runs[0]["text"]))
                    self.list_stack[-1]["checks"] = True
                self.list_stack[-1]["items"].append(runs)
        elif tag in ("ul", "ol"):
            lst = self.list_stack.pop()
            if lst["items"]:
                self.emit({"t": "ul" if lst["t"] == "ul" else "ol",
                           "items": lst["items"], "checks": lst["checks"]})
        elif tag in ("th", "td"):
            if self.stack and self.stack[-1] == tag:
                self.stack.pop()
            if self.row is not None:
                self.row.append({"cells": self.take(), "head": tag == "th"})
        elif tag == "tr":
            if self.table is not None and self.row:
                if all(c["head"] for c in self.row):
                    self.table["header"] = [c["cells"] for c in self.row]
                else:
                    self.table["rows"].append([c["cells"] for c in self.row])
            self.row = None
        elif tag == "table":
            t = self.table
            self.table = None
            if t and (t["header"] or t["rows"]):
                if t["header"] and not any(any(r["text"].strip() for r in c) for c in t["header"]):
                    t["header"] = []
                self.emit(t)
        elif tag == "blockquote":
            self.in_quote = False
            self.blocks.append({"t": "quote", "blocks": self.quote})
            self.quote = []
        elif tag == "hr":
            self.emit({"t": "hr"})

    def handle_startendtag(self, tag, attrs):
        if tag == "hr":
            self.emit({"t": "hr"})
        elif tag == "br":
            self._run("\n")

    def emit(self, block):
        (self.quote if self.in_quote else self.blocks).append(block)


def convert(md_text):
    html = markdown.markdown(md_text, extensions=["tables", "sane_lists"])
    w = Walker()
    w.feed(html)
    w.close()
    return w.blocks


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    blocks = convert(io.open(src, encoding="utf-8").read())
    io.open(dst, "w", encoding="utf-8").write(json.dumps(blocks, ensure_ascii=False))
    print("%s -> %d blocks" % (src.split("/")[-1], len(blocks)))
