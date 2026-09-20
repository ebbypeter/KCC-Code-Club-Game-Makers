// Renders the KCC pack's non-handout documents as editable Word files, in the
// same design language as the PDFs. Driven by a manifest written by
// build_editable.py.  Usage: node make_editable.js manifest.json
const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, ImageRun, ExternalHyperlink, Table,
  TableRow, TableCell, WidthType, ShadingType, AlignmentType, BorderStyle,
  HeadingLevel, VerticalAlign, Footer, PageNumber, PageOrientation, PageBreak,
} = require('docx');

const MAROON = '8C2332', GOLD = 'C9A227', GOLDTX = '8A6712', GREEN = '2E6B3A';
const INK = '2E1015', BODY = '4A3A36', CREAM = 'FBF5E8', CREAM2 = 'F4E9D2';
const LINE = 'DCCBA8', WHITE = 'FFFFFF';
const DISP = 'Fredoka', TEXT = 'Nunito Sans', MONO = 'Consolas';

const NONE = { style: BorderStyle.NONE, size: 0, color: WHITE };
const NOBORDER = { top: NONE, bottom: NONE, left: NONE, right: NONE };
const HAIR = { style: BorderStyle.SINGLE, size: 4, color: LINE };
const CELLB = { top: HAIR, bottom: HAIR, left: HAIR, right: HAIR };

// ---------------------------------------------------------------- inline
function runs(list, o = {}) {
  const out = [];
  for (const r of list || []) {
    if (r.text === '\n') { out.push(new TextRun({ break: 1 })); continue; }
    const base = {
      text: r.text,
      font: r.code ? MONO : (o.font || TEXT),
      size: o.size || 20,
      bold: r.b || o.bold || false,
      italics: r.i || o.italics || false,
      color: o.color || (r.code ? INK : BODY),
    };
    if (r.ph) { base.bold = true; base.color = INK; base.highlight = 'yellow'; }
    if (r.link) {
      out.push(new ExternalHyperlink({
        link: r.link,
        children: [new TextRun(Object.assign({}, base, { color: GREEN, underline: {} }))],
      }));
    } else {
      out.push(new TextRun(base));
    }
  }
  return out.length ? out : [new TextRun({ text: '', font: TEXT, size: 20 })];
}

const plain = (list) => (list || []).map(r => r.text).join('');

// ---------------------------------------------------------------- blocks
function heading(b) {
  const lvl = b.level;
  if (lvl <= 2) {
    return new Paragraph({
      children: runs(b.text, { font: DISP, size: lvl === 1 ? 32 : 28, bold: true, color: MAROON }),
      heading: lvl === 1 ? HeadingLevel.HEADING_1 : HeadingLevel.HEADING_2,
      spacing: { before: 360, after: 120 }, keepNext: true,
      border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: GOLD, space: 6 } },
    });
  }
  return new Paragraph({
    children: runs(b.text, { font: DISP, size: lvl === 3 ? 23 : 21, bold: true, color: lvl === 3 ? INK : GOLDTX }),
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 260, after: 80 }, keepNext: true,
  });
}

function para(b) {
  return new Paragraph({
    children: runs(b.text), spacing: { after: 130, line: 276 },
  });
}

function bullet(items) {
  return items.map(it => new Paragraph({
    children: [new TextRun({ text: '•  ', font: TEXT, size: 20, color: MAROON, bold: true }), ...runs(it)],
    spacing: { after: 70, line: 264 }, indent: { left: 340, hanging: 340 },
  }));
}

function numbered(items) {
  return items.map((it, i) => new Paragraph({
    children: [new TextRun({ text: (i + 1) + '.  ', font: TEXT, size: 20, color: MAROON, bold: true }), ...runs(it)],
    spacing: { after: 70, line: 264 }, indent: { left: 400, hanging: 400 },
  }));
}

function checks(items) {
  return items.map(it => new Paragraph({
    children: [new TextRun({ text: '☐   ', size: 22, color: INK }), ...runs(it)],
    spacing: { after: 90, line: 264 }, indent: { left: 400, hanging: 400 },
  }));
}

function quote(b, W) {
  const inner = [];
  for (const c of b.blocks || []) {
    if (c.t === 'p') inner.push(new Paragraph({ children: runs(c.text, { size: 19 }), spacing: { after: 60, line: 264 } }));
    else if (c.t === 'ul') inner.push(...bullet(c.items));
    else if (c.t === 'h') inner.push(new Paragraph({ children: runs(c.text, { font: DISP, size: 21, bold: true, color: MAROON }), spacing: { after: 60 } }));
  }
  if (!inner.length) inner.push(new Paragraph({ children: [] }));
  return new Table({
    columnWidths: [W], width: { size: W, type: WidthType.DXA },
    rows: [new TableRow({
      children: [new TableCell({
        children: inner, width: { size: W, type: WidthType.DXA },
        shading: { type: ShadingType.CLEAR, fill: CREAM, color: 'auto' },
        borders: {
          top: NONE, bottom: NONE, right: NONE,
          left: { style: BorderStyle.SINGLE, size: 18, color: GOLD },
        },
        margins: { top: 130, bottom: 130, left: 180, right: 160 },
      })],
    })],
  });
}

function hr() {
  return new Paragraph({
    children: [], spacing: { before: 130, after: 130 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: LINE, space: 2 } },
  });
}

function widthsFor(t, W) {
  const cols = Math.max(t.header.length, ...t.rows.map(r => r.length), 1);
  const score = new Array(cols).fill(1);
  const sample = t.header.length ? [t.header, ...t.rows] : t.rows;
  for (const row of sample) {
    row.forEach((c, i) => {
      if (i < cols) score[i] = Math.max(score[i], Math.min(plain(c).length, 90));
    });
  }
  const total = score.reduce((a, b) => a + b, 0);
  // A minimum that is always affordable: a 14-column tracker can't give every
  // column 900 twips, and the leftover would go negative.
  const MIN = Math.max(420, Math.min(900, Math.floor(W / cols / 2)));
  const w = score.map(s => Math.max(MIN, Math.round(W * s / total)));
  let sum = w.reduce((a, b) => a + b, 0);
  while (sum > W) {                       // squeeze the widest column first
    const i = w.indexOf(Math.max(...w));
    const take = Math.min(sum - W, w[i] - MIN);
    if (take <= 0) break;
    w[i] -= take; sum -= take;
  }
  if (sum !== W) w[w.indexOf(Math.max(...w))] += W - sum;
  return w.every(x => x > 0) ? w : new Array(cols).fill(Math.floor(W / cols));
}

function table(t, W) {
  const w = widthsFor(t, W);
  const rows = [];
  if (t.header.length) {
    rows.push(new TableRow({
      tableHeader: true, cantSplit: true,
      children: t.header.map((c, i) => new TableCell({
        children: [new Paragraph({ children: runs(c, { bold: true, color: INK, size: 18 }), spacing: { after: 0 } })],
        width: { size: w[i], type: WidthType.DXA },
        shading: { type: ShadingType.CLEAR, fill: CREAM2, color: 'auto' },
        borders: CELLB, margins: { top: 90, bottom: 90, left: 110, right: 110 },
      })),
    }));
  }
  for (const r of t.rows) {
    rows.push(new TableRow({
      cantSplit: true,
      children: w.map((cw, i) => new TableCell({
        children: [new Paragraph({
          children: runs(r[i] || [], { size: 18, color: i === 0 && !t.header.length ? INK : BODY, bold: i === 0 && !t.header.length }),
          spacing: { after: 0 },
        })],
        width: { size: cw, type: WidthType.DXA },
        borders: CELLB, margins: { top: 90, bottom: 90, left: 110, right: 110 },
        verticalAlign: VerticalAlign.TOP,
      })),
    }));
  }
  return new Table({ rows, columnWidths: w, width: { size: W, type: WidthType.DXA } });
}

function masthead(doc, logoBuf, W) {
  const right = [
    new Paragraph({
      children: [new TextRun({ text: 'KCC Code Club  ·  Game Makers', font: TEXT, size: 15, bold: true, color: GOLDTX, allCaps: true, characterSpacing: 60 })],
      spacing: { after: 110 },
    }),
    new Paragraph({
      children: [new TextRun({ text: doc.title, font: DISP, size: 40, bold: true, color: MAROON })],
      spacing: { after: doc.sub ? 40 : 0 },
    }),
  ];
  if (doc.sub) {
    right.push(new Paragraph({
      children: [new TextRun({ text: doc.sub, font: TEXT, size: 20, color: BODY })],
      spacing: { after: 0 },
    }));
  }
  return [
    new Table({
      columnWidths: [1350, W - 1350], width: { size: W, type: WidthType.DXA },
      rows: [new TableRow({
        children: [
          new TableCell({
            children: [new Paragraph({
              children: [new ImageRun({ type: 'png', data: logoBuf, transformation: { width: 68, height: 68 } })],
              spacing: { after: 0 },
            })],
            width: { size: 1350, type: WidthType.DXA }, borders: NOBORDER,
            verticalAlign: VerticalAlign.CENTER, margins: { top: 0, bottom: 0, left: 0, right: 140 },
          }),
          new TableCell({
            children: right, width: { size: W - 1350, type: WidthType.DXA },
            borders: NOBORDER, verticalAlign: VerticalAlign.CENTER, margins: { top: 0, bottom: 0, left: 0, right: 0 },
          }),
        ],
      })],
    }),
    new Paragraph({
      children: [], spacing: { before: 60, after: 200 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 14, color: MAROON, space: 4 } },
    }),
  ];
}

// ---------------------------------------------------------------- build
const manifest = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const logoBuf = fs.readFileSync(path.join(__dirname, 'assets', 'kcc-logo-small.png'));

(async () => {
  for (const doc of manifest.docs) {
    const W = doc.landscape ? 14570 : 9638;
    const blocks = JSON.parse(fs.readFileSync(doc.ast, 'utf8'));
    const kids = masthead(doc, logoBuf, W);

    if (doc.note) {
      kids.push(quote({ blocks: [{ t: 'p', text: [{ text: doc.note, b: true }] }] }, W));
      kids.push(new Paragraph({ children: [], spacing: { after: 160 } }));
    }

    for (const b of blocks) {
      if (b.t === 'h') {
        if (doc.newpage && doc.newpage.includes(plain(b.text))) {
          kids.push(new Paragraph({ children: [new PageBreak()] }));
        }
        kids.push(heading(b));
      } else if (b.t === 'p') kids.push(para(b));
      else if (b.t === 'ul') kids.push(...(b.checks ? checks(b.items) : bullet(b.items)));
      else if (b.t === 'ol') kids.push(...numbered(b.items));
      else if (b.t === 'table') { kids.push(table(b, W)); kids.push(new Paragraph({ children: [], spacing: { after: 140 } })); }
      else if (b.t === 'quote') { kids.push(quote(b, W)); kids.push(new Paragraph({ children: [], spacing: { after: 140 } })); }
      else if (b.t === 'hr') kids.push(hr());
    }

    const d = new Document({
      creator: 'Kerala Cultural Club',
      title: 'KCC Code Club: Game Makers — ' + doc.title,
      description: doc.sub || '',
      styles: { default: { document: { run: { font: TEXT, size: 20, color: BODY } } } },
      sections: [{
        properties: {
          page: {
            margin: { top: 1134, right: 1134, bottom: 1134, left: 1134 },
            size: doc.landscape ? { orientation: PageOrientation.LANDSCAPE } : undefined,
          },
        },
        footers: {
          default: new Footer({
            children: [new Paragraph({
              alignment: AlignmentType.LEFT,
              children: [
                new TextRun({ text: 'KCC Code Club · Game Makers — ' + doc.title + '    ', font: TEXT, size: 14, color: '8A7A72' }),
                new TextRun({ children: [PageNumber.CURRENT], font: TEXT, size: 14, color: '8A7A72' }),
              ],
            })],
          }),
        },
        children: kids,
      }],
    });

    const buf = await Packer.toBuffer(d);
    fs.writeFileSync(doc.out, buf);
    console.log('  ' + path.basename(doc.out));
  }
  console.log('wrote ' + manifest.docs.length + ' documents');
})();
