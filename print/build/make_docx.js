// KCC Code Club — Game Makers programme summary, in the club design language.
const fs = require('fs');
const d = require('docx');
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell,
  WidthType, ShadingType, AlignmentType, BorderStyle, HeadingLevel, PageBreak,
  VerticalAlign,
} = d;

const MAROON = '8C2332', GOLD = 'C9A227', GOLDTX = '8A6712', GREEN = '2E6B3A';
const INK = '2E1015', BODY = '4A3A36', CREAM = 'FBF5E8', CREAM2 = 'F4E9D2';
const LINE = 'DCCBA8', DARK = '3A121B', WHITE = 'FFFFFF';
const DISP = 'Fredoka', TEXT = 'Nunito Sans';
const W = 9638;
const NONE = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const NOBORDER = { top: NONE, bottom: NONE, left: NONE, right: NONE };
const HAIR = { style: BorderStyle.SINGLE, size: 4, color: LINE };
const CELLB = { top: HAIR, bottom: HAIR, left: HAIR, right: HAIR };

const run = (text, o = {}) => new TextRun({
  text, font: o.font || TEXT, size: o.size || 20, bold: o.bold || false,
  italics: o.italics || false, color: o.color || BODY,
  allCaps: o.caps || false, characterSpacing: o.spacing || 0,
});

const para = (text, o = {}) => new Paragraph({
  children: Array.isArray(text) ? text : [run(text, o)],
  alignment: o.align, spacing: { before: o.before || 0, after: o.after === undefined ? 120 : o.after, line: o.line || 276 },
  border: o.border, indent: o.indent, heading: o.heading, outlineLevel: o.outlineLevel,
  keepNext: o.keepNext, shading: o.shading,
});

const h2 = (text) => new Paragraph({
  children: [run(text, { font: DISP, size: 30, bold: true, color: MAROON })],
  heading: HeadingLevel.HEADING_1,
  spacing: { before: 380, after: 130 }, keepNext: true,
  border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: GOLD, space: 6 } },
});

const eyebrow = (text) => para([run(text, { size: 15, bold: true, color: GOLDTX, caps: true, spacing: 60 })], { after: 60 });

const cell = (children, o = {}) => new TableCell({
  children, width: { size: o.w, type: WidthType.DXA },
  shading: o.fill ? { type: ShadingType.CLEAR, fill: o.fill, color: 'auto' } : undefined,
  borders: o.borders || CELLB, verticalAlign: o.valign || VerticalAlign.TOP,
  margins: { top: 90, bottom: 90, left: 110, right: 110 },
});

const table = (rows, widths) => new Table({
  rows, columnWidths: widths, width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA },
});

// ---------------------------------------------------------------- content
const STATS = [
  ['8 weeks', 'per term'], ['90 minutes', 'per session'], ['1 : 5', 'adults to kids'],
  ['16 students', 'pilot cap'], ['$40', 'per term  ·  $5 a session'],
];

const RHYTHM = [
  ['0:00–0:10', 'Show & Tell', "Two or three students demo last week's homework. The strongest motivator in the programme, and it costs nothing."],
  ['0:10–0:25', 'New concept, live demo', 'You code on the projector and deliberately make mistakes. Watching an adult debug calmly is the lesson.'],
  ['0:25–0:55', 'Class activity', 'Small, throwaway, everyone does it. Practising the concept with no risk to their real project.'],
  ['0:55–1:05', 'Break', 'Non-negotiable. Ninety minutes of screen time without a break is not a thing 9-year-olds can do.'],
  ['1:05–1:25', 'Project build', "Add this week's layer to their own game."],
  ['1:25–1:30', 'Save, share, homework', 'Everyone saves and backs up. Nobody leaves with a broken game.'],
];

const CHECKPOINTS = [
  ['Week 1', 'A themed character that says hello'],
  ['Week 2', 'You can drive it left and right'],
  ['Week 3', 'Things fall from the sky'],
  ['Week 4', 'Catching works — actually playable'],
  ['Week 5', 'It keeps score'],
  ['Week 6', 'Lives, title screen, game over'],
  ['Week 7', 'It gets harder as you improve'],
  ['Week 8', 'Finished, shared, demoed'],
];

const WEEKS = [
  ['WEEK 1  ·  LOOKS & MOTION', 'Meet Scratch',
   "A program is a list of instructions, carried out in order, exactly as written. Computers don't guess what you meant — not because they're stupid, but because they're very obedient.",
   'when green flag clicked · move · turn · go to x y · say for n secs · next costume · change size by',
   'Name Dance — a sprite that says your name, then dances',
   'Player sprite and themed backdrop; the character greets you',
   'A four-line joke with the timing right; theme your player sprite'],
  ['WEEK 2  ·  EVENTS & MOTION', 'Events and Movement',
   "Code doesn't only run when you click the flag — it runs when things happen. And position is just two numbers.",
   'when key pressed · when this sprite clicked · change x by · set x to · glide n secs to x y · point in direction',
   'Treasure Hunt, then Drive the Car — and tune the speed until it feels right',
   'Arrow keys move the player along the bottom of the stage',
   'Up/down movement or screen wrap; face the direction of travel'],
  ['WEEK 3  ·  CONTROL & OPERATORS', 'Loops and Randomness',
   "If you're about to do the same thing twenty times — don't. And when you want the game to surprise you, ask for a random number.",
   'repeat n · forever · repeat until · wait n secs · pick random a to b',
   'Dancing Sprite, then Rain — the dress rehearsal for the project build',
   'One object falls from a random point at the top, over and over',
   'A second falling object; random falling speed each drop'],
  ['WEEK 4  ·  CONTROL & SENSING', 'Decisions and Sensing  (biggest week)',
   'The computer can ask a yes-or-no question about the world and act on the answer. Today the project stops being an animation and becomes a game.',
   'if … then · if … then … else · touching? · key pressed? · start sound',
   'Traffic Light, then Bumper Sprite',
   'Catching works, with a sound. Playtest and swap seats',
   "Make catching feel like something; add a thing you shouldn't catch"],
  ['WEEK 5  ·  VARIABLES', 'Variables and Score',
   'A variable is a labelled box. Set replaces what’s inside; change adds to it. That one distinction is the whole class.',
   'set [var] to · change [var] by · show variable · hide variable',
   'Click Counter, then Countdown Timer — combine them into a whole small game',
   'Score on the stage. Good catches add, bad ones subtract',
   'A high score that survives a restart; make the readout look good'],
  ['WEEK 6  ·  EVENTS & CONTROL', 'Broadcasts and Game Over',
   "Sprites can't read each other's code, but one can shout a message that everyone hears. It doesn't know or care who's listening — that's the clever part.",
   'broadcast · when I receive · broadcast and wait · switch backdrop to · stop all',
   'Magic Wand, then a two-scene story that runs itself',
   'Lives, a title screen, a game over screen and a restart',
   'A way to win; play again without the green flag'],
  ['WEEK 7  ·  OPERATORS & MY BLOCKS', 'Operators, My Blocks and Levels',
   '“How do you make a cup of tea?” — seven steps. Draw a box round them, call it make tea, and four cups is four words instead of twenty-eight steps. That’s abstraction, arrived at by a nine-year-old in under a minute.',
   '+ − × / · < = > · and / or / not · join · ask and wait · define',
   'Quiz Sprite, deliberately repetitive — then a My Block that cleans it up',
   'Speed ramps with score, level-up messages, a rare high-value item',
   'Finish the rare treasure; turn repeated code into a My Block'],
  ['WEEK 8  ·  CONSOLIDATION', 'Polish, Test and Showcase  (families invited)',
   'Finishing is a skill. Making something work for you is one thing; making it work for someone who has never seen it is completely different.',
   'no new blocks · debugging · playtesting · sharing safely',
   "Find the Bug, then Playtest Swap. The author isn't allowed to defend their game — they read the card and say thank you",
   "Title screen, instructions, credits, sound. Cut scope, don't add",
   'The showcase. Two minutes each: what it is, thirty seconds of play, and the hardest bug they fixed'],
];

const RULES = [
  ['Two adults in the room, minimum, always.',
   'Size the class to the volunteers you have — one per five students, 1:4 if the group skews young, capped at 16 for the pilot and 20 thereafter. If you drop below two on the day and have no backup, cancel rather than running it solo.'],
  ['Never take the mouse.',
   'Ask what they expected and what happened instead, then put your hands behind your back. Most children solve their own bug halfway through answering, and that moment is the entire product.'],
  ['Make mistakes on purpose.',
   'Every live demo has a planted error. Children arrive believing adults who are good at computers never get errors — watching you be confused and calm, weekly, is worth more than any concept in the syllabus.'],
  ['Nothing is graded.',
   "Homework is never collected, marked or chased. A child who does none of it and turns up every week is a success; one who feels behind and stops coming is the failure you're designing against."],
  ['Everyone leaves with a working game.',
   "Check the screens at the end — don't take their word for it."],
];

const RESOURCES = [
  ['Intro to Scratch\nprojects.raspberrypi.org', 'Sprites, scripts and loops. Self-guided projects a child can follow alone', 'Weeks 1–3'],
  ['More Scratch\nprojects.raspberrypi.org', "Broadcast, decisions and variables. “Don't fall in!” is the closest thing to Sky Catcher", 'Weeks 4–6'],
  ['Further Scratch\nprojects.raspberrypi.org', 'Clones, My Blocks and boolean logic. Where to send anyone racing ahead', 'Beyond'],
  ['Code Club Aotearoa\ncodeclub.nz', 'Hundreds of free projects with a local context, plus a volunteer network worth joining later', 'Any week'],
  ['Scratch for Educators\nscratch.mit.edu/educators', "Teacher accounts, class management and MIT's own teaching guides", 'Setup'],
];

// ---------------------------------------------------------------- build
const kids = [];

// masthead
kids.push(new Table({
  columnWidths: [1500, 8138],
  width: { size: W, type: WidthType.DXA },
  rows: [new TableRow({
    children: [
      cell([new Paragraph({ children: [new ImageRun({
        type: 'png', data: fs.readFileSync(__dirname + '/kcc-logo.png'),
        transformation: { width: 82, height: 82 },
      })], spacing: { after: 0 } })], { w: 1500, borders: NOBORDER, valign: VerticalAlign.CENTER }),
      cell([
        para([run('KCC Code Club  ·  Volunteer programme  ·  Pilot', { size: 15, bold: true, color: GOLDTX, caps: true, spacing: 60 })], { after: 110 }),
        para([run('Game Makers', { font: DISP, size: 52, bold: true, color: MAROON })], { after: 30 }),
        para([run('Scratch programming for ages 7–12', { size: 21, color: BODY })], { after: 0 }),
      ], { w: 8138, borders: NOBORDER, valign: VerticalAlign.CENTER }),
    ],
  })],
}));
kids.push(para('', { after: 60, border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: MAROON, space: 4 } } }));
kids.push(para('Eight weeks of Scratch for kids aged 7–12, most of whom have never written a line of code. By the last session every one of them demos a game they built, debugged and finished themselves. The first class running under KCC Code Club.',
  { size: 21, after: 200 }));

// stat tiles
kids.push(table([new TableRow({
  children: STATS.map(([big, small], i) => cell([
    para([run(big, { font: DISP, size: 28, bold: true, color: MAROON })], { align: AlignmentType.CENTER, after: 20 }),
    para([run(small, { size: 15, color: BODY })], { align: AlignmentType.CENTER, after: 0 }),
  ], { w: i < 3 ? 1928 : 1927, fill: CREAM, borders: CELLB })),
})], [1928, 1928, 1928, 1927, 1927]));
kids.push(para('', { after: 60 }));

// class rhythm
kids.push(h2('The shape of every class'));
kids.push(para('The same rhythm every week. Children settle fastest into a predictable structure, and a predictable structure is what lets a stand-in volunteer run a session cold from the plan.'));
kids.push(table([
  new TableRow({
    tableHeader: true,
    children: ['Time', 'Segment', "Why it's there"].map((t, i) =>
      cell([para([run(t, { bold: true, color: INK, size: 18 })], { after: 0 })],
        { w: [1700, 2600, 5338][i], fill: CREAM2 })),
  }),
  ...RHYTHM.map(([a, b, c]) => new TableRow({
    children: [
      cell([para([run(a, { bold: true, color: MAROON, size: 18 })], { after: 0 })], { w: 1700 }),
      cell([para([run(b, { bold: true, color: INK, size: 18 })], { after: 0 })], { w: 2600 }),
      cell([para([run(c, { size: 18 })], { after: 0 })], { w: 5338 }),
    ],
  })),
], [1700, 2600, 5338]));
kids.push(para([run('Fifteen minutes of talking, fifty of building.', { font: DISP, size: 24, bold: true, color: GREEN })],
  { before: 200, after: 40 }));
kids.push(para('The two segments never to cut are Show & Tell and the save at the end.', { after: 160 }));

// long project
kids.push(h2('The long project — Sky Catcher'));
kids.push(para('Things fall from the sky; you catch the good ones and dodge the bad. Deliberately unoriginal, because every concept in the course has an obvious home inside it — loops make things fall, conditionals make catching work, variables are the score, broadcasts are game over. Students pick their own theme in week one and keep it: mangoes into a basket, a fielder catching balls, a dog catching bones.'));
kids.push(para([run('It is playable at the end of every single class.', { bold: true, color: INK, size: 21 })], { after: 140 }));
kids.push(table([
  new TableRow({
    tableHeader: true,
    children: ['Week', 'State of the game at the end of class'].map((t, i) =>
      cell([para([run(t, { bold: true, color: INK, size: 18 })], { after: 0 })], { w: [1900, 7738][i], fill: CREAM2 })),
  }),
  ...CHECKPOINTS.map(([w, s]) => new TableRow({
    children: [
      cell([para([run(w, { bold: true, color: MAROON, size: 18 })], { after: 0 })], { w: 1900 }),
      cell([para([run(s, { size: 18 })], { after: 0 })], { w: 7738 }),
    ],
  })),
], [1900, 7738]));

// the eight classes
kids.push(new Paragraph({ children: [new PageBreak()] }));
kids.push(h2('The eight classes'));
kids.push(para('Nothing in a week depends on a later one. That strictly forward chain is what makes the catch-up files work: a student who misses week five opens the week-five skeleton and walks into week six on level ground.', { after: 180 }));

for (const [band, title, idea, blocks, activity, project, homework] of WEEKS) {
  const rows = [
    new TableRow({
      cantSplit: true,
      children: [cell([para([run(band, { size: 15, bold: true, color: WHITE, caps: true, spacing: 60 })], { after: 0, keepNext: true })],
        { w: W, fill: MAROON, borders: NOBORDER })],
    }),
    new TableRow({
      cantSplit: true,
      children: [cell([
        para([run(title, { font: DISP, size: 24, bold: true, color: INK })], { after: 60, keepNext: true }),
        para([run(idea, { size: 18 })], { after: 0, keepNext: true }),
      ], { w: W, fill: CREAM, borders: NOBORDER })],
    }),
  ];
  const labelled = [['Blocks', blocks], ['Class activity', activity], ['Project', project], ['Homework', homework]];
  labelled.forEach(([label, text], i) => {
    const kn = i < labelled.length - 1;
    rows.push(new TableRow({
      cantSplit: true,
      children: [
        cell([para([run(label, { size: 16, bold: true, color: GOLDTX, caps: true })], { after: 0, keepNext: kn })], { w: 2000 }),
        cell([para([run(text, { size: 18, font: label === 'Blocks' ? 'Consolas' : TEXT })], { after: 0, keepNext: kn })], { w: W - 2000 }),
      ],
    }));
  });
  kids.push(new Table({ rows, columnWidths: [2000, W - 2000], width: { size: W, type: WidthType.DXA } }));
  kids.push(para('', { after: 140 }));
}

// non-negotiables
kids.push(new Paragraph({ children: [new PageBreak()] }));
kids.push(h2("Five things that aren't negotiable"));
for (const [head, text] of RULES) {
  kids.push(para([run(head, { font: DISP, size: 21, bold: true, color: MAROON })], { after: 40, keepNext: true }));
  kids.push(para(text, { after: 160 }));
}

// prep
kids.push(h2('Before week one — start six weeks out'));
kids.push(para([run('Scratch accounts, six weeks out', { font: DISP, size: 21, bold: true, color: INK })], { after: 40, keepNext: true }));
kids.push(para("Individual signups need a parent's email confirmed for each child. Fifteen families finding fifteen emails the night before does not work — don't try. Request a Scratch teacher account in the club's name instead: it creates student accounts in bulk and lets you reset forgotten passwords yourself. Approval is manual and takes days. Install Scratch Desktop on every machine anyway — community-hall wi-fi fails, and it will pick showcase night.", { after: 160 }));
kids.push(para([run('Skeleton files, three weeks out', { font: DISP, size: 21, bold: true, color: INK })], { after: 40, keepNext: true }));
kids.push(para('Build Sky Catcher yourself and save a copy at each week’s checkpoint. About two hours, once. When a child misses week five, their parent gets the week-five link and they walk into week six on level ground instead of two weeks behind and quietly humiliated. Falling behind is the main reason children drop out of coding clubs; this single artefact removes it, and nothing else in the prep comes close for value.', { after: 160 }));
kids.push(para([run('Small things that matter more than they look', { font: DISP, size: 21, bold: true, color: INK })], { after: 40, keepNext: true }));
kids.push(para('Spare USB mice — dragging blocks on a trackpad is the difference between building things and giving up. And lay the room out so you can walk behind every screen; rows facing the projector look tidy and hide everything.', { after: 180 }));

// money
kids.push(h2('What it costs, and what families pay'));
kids.push(para('The club charges $40 for the eight-week term — $5 a session — collected up front. A fee measurably improves attendance because people show up for what they have paid for, and at this level it turns nobody away.'));
kids.push(para([run('Agree with the committee, before the fee is published, that no child is turned away over it and who can waive it quietly. A waiver that needs a meeting is a waiver nobody asks for.', { size: 18, color: BODY, italics: true })],
  { after: 180, shading: { type: ShadingType.CLEAR, fill: CREAM, color: 'auto' }, indent: { left: 160, right: 160 }, before: 60 }));

// resources
kids.push(h2('Where the material comes from'));
kids.push(para('The lesson design is original, but it deliberately sits on free, tested project libraries. Use these for fast finishers, for catch-up, and as the backbone if a stand-in volunteer ever has to run a session cold.'));
kids.push(table([
  new TableRow({
    tableHeader: true,
    children: ['Resource', "What it's for", 'Maps to'].map((t, i) =>
      cell([para([run(t, { bold: true, color: INK, size: 18 })], { after: 0 })], { w: [3000, 4638, 2000][i], fill: CREAM2 })),
  }),
  ...RESOURCES.map(([a, b, c]) => new TableRow({
    children: [
      cell(a.split('\n').map((l, i) => para([run(l, { bold: i === 0, color: i === 0 ? INK : GREEN, size: i === 0 ? 18 : 16 })], { after: 0 })), { w: 3000 }),
      cell([para([run(b, { size: 18 })], { after: 0 })], { w: 4638 }),
      cell([para([run(c, { size: 18, bold: true, color: MAROON })], { after: 0 })], { w: 2000 }),
    ],
  })),
], [3000, 4638, 2000]));

kids.push(para([run('Measure the right thing.', { font: DISP, size: 21, bold: true, color: MAROON })], { before: 260, after: 40, keepNext: true }));
kids.push(para('Not test scores — there is no test. How many of the students who started week one demo at the showcase (aim above 75%), and how many are still opening Scratch a month after the course ended. That second number is the only one that really counts.'));

const doc = new Document({
  creator: 'Kerala Cultural Club',
  title: 'KCC Code Club: Game Makers',
  description: 'Programme summary — Scratch for ages 7–12',
  styles: { default: { document: { run: { font: TEXT, size: 20, color: BODY } } } },
  sections: [{
    properties: { page: { margin: { top: 1134, right: 1134, bottom: 1134, left: 1134 } } },
    children: kids,
  }],
});

Packer.toBuffer(doc).then(b => {
  fs.writeFileSync(process.argv[2] || 'KCC-Game-Makers.docx', b);
  console.log('wrote', process.argv[2]);
});
