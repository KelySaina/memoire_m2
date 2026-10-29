"""Build the M2 mémoire PDF from the content/*.md files.

Markup (one directive per line):
  @front TITLE             new page, centred title, in TOC (level 0)
  @part TITLE              part divider page
  @chapter TITLE           new page, chapter title
  ## / ### / ####          section, subsection, sub-subsection
  @mode roman|arabic|none [reset]   page numbering from the current page on
  @sommaire / @tdm / @lof / @lot    generated lists
  @img path | width_fraction | caption
  @code path [start-end]   listing from build/code/
  ``` ... ```              inline listing
  @tabcap caption          caption of the next pipe table
  @colw 1,2,3              relative column widths of the next pipe table
  @gantt / @pagebreak / @space N / @center text / @right text
  = text                   standalone non-indented line
  - item / "  - item"      bullets
"""
import glob
import os
import re
import sys

from reportlab.graphics.shapes import Drawing, Line, Rect, String
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Flowable, Frame, Image, KeepTogether,
                                NextPageTemplate, PageBreak, PageTemplate, Paragraph,
                                Preformatted, Spacer, Table, TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # scratchpad
LIB = "/usr/share/fonts/truetype/liberation/"
DJV = "/usr/share/fonts/truetype/dejavu/"

pdfmetrics.registerFont(TTFont("Serif", LIB + "LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Serif-B", LIB + "LiberationSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Serif-I", LIB + "LiberationSerif-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Serif-BI", LIB + "LiberationSerif-BoldItalic.ttf"))
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif-I", boldItalic="Serif-BI")
pdfmetrics.registerFont(TTFont("Mono", DJV + "DejaVuSansMono.ttf"))
pdfmetrics.registerFont(TTFont("Sym", DJV + "DejaVuSans.ttf"))

PAGE_W, PAGE_H = A4
ML, MR, MT, MB = 2.5 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm
FRAME_W, FRAME_H = PAGE_W - ML - MR, PAGE_H - MT - MB

# ---------------------------------------------------------------- styles
S = {}
S["body"] = ParagraphStyle("body", fontName="Serif", fontSize=12, leading=18, alignment=TA_JUSTIFY,
                           firstLineIndent=1.25 * cm, spaceAfter=6)
S["plain"] = ParagraphStyle("plain", parent=S["body"], firstLineIndent=0, spaceAfter=2)
S["plainkeep"] = ParagraphStyle("plainkeep", parent=S["plain"], keepWithNext=1, spaceAfter=6)
S["center"] = ParagraphStyle("center", parent=S["plain"], alignment=TA_CENTER)
S["right"] = ParagraphStyle("right", parent=S["plain"], alignment=TA_RIGHT)
S["bullet"] = ParagraphStyle("bullet", parent=S["body"], firstLineIndent=0, leftIndent=1.4 * cm,
                             bulletIndent=0.7 * cm, bulletFontName="Sym", bulletFontSize=10, spaceAfter=2)
S["bullet2"] = ParagraphStyle("bullet2", parent=S["bullet"], leftIndent=2.2 * cm, bulletIndent=1.6 * cm)
S["front"] = ParagraphStyle("front", fontName="Serif-B", fontSize=14, leading=18, alignment=TA_CENTER,
                            spaceAfter=24, keepWithNext=1)
S["part"] = ParagraphStyle("part", fontName="Serif-B", fontSize=16, leading=22, alignment=TA_CENTER)
S["chapter"] = ParagraphStyle("chapter", fontName="Serif-B", fontSize=16, leading=22, alignment=TA_CENTER,
                              spaceAfter=18, keepWithNext=1)
S["h1"] = ParagraphStyle("h1", fontName="Serif-B", fontSize=14, leading=18, leftIndent=0.6 * cm,
                         spaceBefore=12, spaceAfter=8, keepWithNext=1)
S["h2"] = ParagraphStyle("h2", fontName="Serif-BI", fontSize=12.5, leading=17, leftIndent=1.2 * cm,
                         spaceBefore=10, spaceAfter=6, keepWithNext=1)
S["h3"] = ParagraphStyle("h3", fontName="Serif-BI", fontSize=12, leading=16, leftIndent=1.2 * cm,
                         spaceBefore=8, spaceAfter=4, keepWithNext=1)
S["figcap"] = ParagraphStyle("figcap", fontName="Serif-I", fontSize=11, leading=14, alignment=TA_CENTER,
                             spaceBefore=4, spaceAfter=12)
S["tabcap"] = ParagraphStyle("tabcap", parent=S["figcap"], spaceBefore=8, spaceAfter=6, keepWithNext=1)
S["cell"] = ParagraphStyle("cell", fontName="Serif", fontSize=11, leading=14, alignment=TA_LEFT)
S["cellh"] = ParagraphStyle("cellh", parent=S["cell"], fontName="Serif-B", alignment=TA_CENTER)
S["code"] = ParagraphStyle("code", fontName="Mono", fontSize=7.6, leading=9.8)

TOC_STYLES = [
    ParagraphStyle("toc0", fontName="Serif", fontSize=12, leading=17, leftIndent=0, firstLineIndent=0,
                   rightIndent=1.0 * cm, spaceBefore=3),
    ParagraphStyle("toc1", fontName="Serif", fontSize=12, leading=17, leftIndent=0.6 * cm, firstLineIndent=0,
                   rightIndent=1.0 * cm),
    ParagraphStyle("toc2", fontName="Serif", fontSize=11.5, leading=16, leftIndent=1.2 * cm, firstLineIndent=0,
                   rightIndent=1.0 * cm),
]
LIST_STYLE = [ParagraphStyle("lst", fontName="Serif", fontSize=12, leading=18, leftIndent=0, rightIndent=1.0 * cm)]

EMOJI = {"🚀": "[>>]", "❌": "[ERREUR]", "✅": "[OK]", "⚠️": "[ATTENTION]", "⚠": "[ATTENTION]", "🔹": "[*]",
         "🔄": "[ROLLBACK]", "🩺": "[CHECK]", "⏳": "[ATTENTE]", "️": ""}

# ------------------------------------------------------------ page numbers
PAGE_LABELS = {}  # physical page -> printed label, kept across multiBuild passes


def roman(n):
    out = ""
    for v, s in ((1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"), (50, "L"),
                 (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")):
        while n >= v:
            out += s
            n -= v
    return out


class Mode(Flowable):
    """Zero-size marker switching the page numbering from the page it lands on."""

    def __init__(self, mode, reset):
        super().__init__()
        self.mode, self.reset = mode, reset

    def wrap(self, *a):
        return 0, 0

    def draw(self):
        pass


class Anchor(Flowable):
    """Zero-size marker registering a TOC / figure / table entry."""

    def __init__(self, kind, level, text, outline_level=None):
        super().__init__()
        self.kind, self.level, self.text, self.outline_level = kind, level, text, outline_level

    def wrap(self, *a):
        return 0, 0

    def draw(self):
        pass


class ListTOC(TableOfContents):
    def __init__(self, kind, max_level, styles):
        super().__init__(levelStyles=styles, dotsMinLevel=0, formatter=lambda p: PAGE_LABELS.get(p, str(p)))
        self._kind, self._max = kind, max_level

    def notify(self, kind, stuff):
        if kind == self._kind and stuff[0] <= self._max:
            self.addEntry(*stuff)


class Doc(BaseDocTemplate):
    def handle_documentBegin(self):
        self.num = {"mode": None, "roman": 0, "arabic": 0}
        self.key_n = 0
        super().handle_documentBegin()

    def afterFlowable(self, f):
        if isinstance(f, Mode):
            self.num["mode"] = f.mode
            if f.reset and f.mode:
                self.num[f.mode] = 0
        elif isinstance(f, Anchor):
            self.key_n += 1
            key = f"k{self.key_n}"
            self.canv.bookmarkPage(key)
            plain = re.sub(r"<[^>]+>", "", f.text).replace("&amp;", "&")
            if f.outline_level is not None:
                self.canv.addOutlineEntry(plain, key, f.outline_level, closed=f.outline_level > 0)
            self.notify(f.kind, (f.level, f.text, self.page, key))


def page_end(canv, doc):
    st = doc.num
    label = ""
    if st["mode"]:
        st[st["mode"]] += 1
        label = roman(st["roman"]) if st["mode"] == "roman" else str(st["arabic"])
        canv.setFont("Serif", 11)
        canv.drawRightString(PAGE_W - MR, 1.4 * cm, label)
    PAGE_LABELS[canv.getPageNumber()] = label


def cover_page(canv, doc):
    canv.saveState()
    canv.setDash(4, 3)
    canv.setLineWidth(0.8)
    canv.setStrokeColor(colors.HexColor("#555555"))
    canv.rect(1.4 * cm, 1.4 * cm, PAGE_W - 2.8 * cm, PAGE_H - 2.8 * cm)
    canv.restoreState()


# --------------------------------------------------------------- helpers
def inline(text):
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = text.replace("&lt;br&gt;", "<br/>")
    codes = []

    def keep(m):
        codes.append(m.group(1))
        return f"\x00{len(codes) - 1}\x00"

    text = re.sub(r"`([^`]+)`", keep, text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", text)
    text = re.sub(r"\x00(\d+)\x00", lambda m: f'<font name="Mono" size="10">{codes[int(m.group(1))]}</font>', text)
    return text


def img_path(p):
    return p if os.path.isabs(p) else os.path.join(ROOT, p)


def image_flow(path, frac, caption, counter):
    path = img_path(path)
    iw, ih = ImageReader(path).getSize()
    w = FRAME_W * frac
    h = w * ih / iw
    maxh = FRAME_H * 0.78
    if h > maxh:
        h, w = maxh, maxh * iw / ih
    counter["fig"] += 1
    cap = f"Figure {counter['fig']} : {caption}"
    return KeepTogether([Image(path, width=w, height=h), Anchor("FigEntry", 0, inline(cap)),
                         Paragraph(inline(cap), S["figcap"])])


def code_flow(text):
    for k, v in EMOJI.items():
        text = text.replace(k, v)
    text = text.expandtabs(4).rstrip("\n")
    width = 96
    lines = []
    for ln in text.split("\n"):
        indent = " " * (len(ln) - len(ln.lstrip()) + 4)
        while len(ln) > width:
            cut = ln.rfind(" ", len(indent) + 1, width)
            if cut <= width // 2:
                cut = width
            lines.append(ln[:cut])
            ln = indent + ln[cut:].lstrip()
        lines.append(ln)
    out = []
    for i in range(0, len(lines), 62):
        t = Table([[Preformatted("\n".join(lines[i:i + 62]), S["code"])]], colWidths=[FRAME_W])
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F4F4F4")),
                               ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#999999")),
                               ("LEFTPADDING", (0, 0), (-1, -1), 6), ("TOPPADDING", (0, 0), (-1, -1), 4),
                               ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
        out.append(t)
    out.append(Spacer(1, 8))
    return out


def table_flow(rows, colw, caption, counter):
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    cells = [r for r in cells if not all(re.fullmatch(r":?-{2,}:?", c) for c in r)]
    ncol = len(cells[0])
    if not colw:
        lens = [max(len(r[i]) if i < len(r) else 0 for r in cells) for i in range(ncol)]
        colw = [max(l, 8) ** 0.6 for l in lens]
    tot = sum(colw)
    widths = [FRAME_W * c / tot for c in colw]
    data = []
    for ri, r in enumerate(cells):
        r = r + [""] * (ncol - len(r))
        data.append([Paragraph(inline(c), S["cellh"] if ri == 0 else S["cell"]) for c in r])
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9D9D9")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    out = []
    if caption:
        counter["tab"] += 1
        cap = f"Tableau {counter['tab']} : {caption}"
        out += [Anchor("TabEntry", 0, inline(cap)), Paragraph(inline(cap), S["tabcap"])]
    out += [t, Spacer(1, 10)]
    return out


def gantt():
    phases = [("1. Mise en place de l'infrastructure", 1, 2),
              ("2. Étude et conception du pipeline CI/CD", 3, 5),
              ("3. Déploiement de la première version", 6, 7),
              ("4. Intégration de nouvelles fonctionnalités", 8, 10),
              ("5. Tests post-déploiement et validation", 11, 12)]
    lab_w, top, row_h = 6.2 * cm, 22, 26
    week_w = (FRAME_W - lab_w) / 12
    h = top + row_h * len(phases) + 6
    d = Drawing(FRAME_W, h)
    for w in range(12):
        x = lab_w + w * week_w
        d.add(String(x + week_w / 2, h - 14, f"S{w + 1}", fontName="Serif-B", fontSize=9, textAnchor="middle"))
        d.add(Line(x, 0, x, h - top + 4, strokeColor=colors.HexColor("#CCCCCC"), strokeWidth=0.5))
    d.add(Line(FRAME_W, 0, FRAME_W, h - top + 4, strokeColor=colors.HexColor("#CCCCCC"), strokeWidth=0.5))
    for i, (name, a, b) in enumerate(phases):
        y = h - top - (i + 1) * row_h
        d.add(String(0, y + 8, name, fontName="Serif", fontSize=9.5))
        d.add(Rect(lab_w + (a - 1) * week_w + 1, y + 4, (b - a + 1) * week_w - 2, row_h - 10,
                   fillColor=colors.HexColor("#ED7D31"), strokeColor=None))
    return d


# ------------------------------------------------------------ cover page
def cover():
    def P(t, size=12, bold=False, align=TA_CENTER, lead=None, after=0, color=colors.black):
        return Paragraph(t, ParagraphStyle("c", fontName="Serif-B" if bold else "Serif", fontSize=size,
                                           leading=lead or size * 1.35, alignment=align, spaceAfter=after,
                                           textColor=color))

    uf, eni = img_path("fig_m2/p001_n000.png"), img_path("fig_m2/p001_n001.png")
    tk = img_path("fig_bokyy/p001_n002.png")
    logos_l = Table([[Image(uf, width=1.75 * cm, height=2.2 * cm), Image(eni, width=2.15 * cm, height=2.15 * cm)]],
                    colWidths=[2.0 * cm, 2.4 * cm])
    logos = Table([[logos_l, "", Image(tk, width=4.6 * cm, height=4.6 * cm * 156 / 455)]],
                  colWidths=[4.6 * cm, FRAME_W - 9.4 * cm, 4.8 * cm])
    logos.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (2, 0), (2, 0), "RIGHT")]))
    title = Paragraph("ÉTUDE DE LA MISE EN PLACE D’UN PIPELINE CI/CD ET ORCHESTRATION POUR UNE APPLICATION "
                      "EN ARCHITECTURE MICROSERVICES",
                      ParagraphStyle("t", fontName="Serif-B", fontSize=16.5, leading=23, alignment=TA_CENTER,
                                     textColor=colors.HexColor("#1F4E79")))
    tbox = Table([[title]], colWidths=[FRAME_W])
    tbox.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 2, colors.HexColor("#5B9BD5")),
                              ("ROUNDEDCORNERS", [12, 12, 12, 12]),
                              ("TOPPADDING", (0, 0), (-1, -1), 12), ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
                              ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12)]))
    js = ParagraphStyle("j", fontName="Serif", fontSize=12, leading=17)
    jb = ParagraphStyle("jb", parent=js, fontName="Serif-B")
    jury = Table([
        [Paragraph("Président :", js), Paragraph("Monsieur RAFAMANTANANTSOA Fontaine, Professeur", js)],
        [Paragraph("Examinateur :", js),
         Paragraph("Monsieur RAZAFINDRAMONJA Clément Aubert, Assistant d’Enseignement Supérieur et de Recherche", js)],
        [Paragraph("Rapporteur :", js),
         Paragraph("Monsieur RANDRIANOMENJANAHARY Lala Ferdinand, Maître de Conférences", js)],
    ], colWidths=[3.0 * cm, FRAME_W - 3.0 * cm])
    jury.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                              ("TOPPADDING", (0, 0), (-1, -1), 1), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    return [
        logos, Spacer(1, 34),
        P("UNIVERSITÉ DE FIANARANTSOA", 16, True, after=4),
        P("ÉCOLE NATIONALE D’INFORMATIQUE", 16, True, after=40),
        P("MÉMOIRE DE FIN D’ÉTUDES POUR L’OBTENTION DU DIPLÔME", 13, True, after=2),
        P("DE MASTER PROFESSIONNEL", 13, True, after=26),
        P("<b>Mention :</b> Informatique", 12, after=4),
        P("<b>Parcours :</b> Informatique Générale", 12, after=4),
        P("<b>Intitulé :</b>", 12, after=12),
        tbox, Spacer(1, 44),
        P("<b>Présenté le</b> 26 novembre 2025", 12, align=TA_LEFT, after=2),
        P("<b>Par</b> Monsieur RAVELOMAHARAVO Rotsy Maminiaina Thierry Michaël", 12, align=TA_LEFT, after=30),
        Paragraph("<u>Membres du jury</u> :", jb), Spacer(1, 4), jury, Spacer(1, 56),
        P("Année Universitaire : 2024-2025", 12, align=TA_RIGHT),
        NextPageTemplate("normal"), PageBreak(),
    ]


# ---------------------------------------------------------------- parser
def parse(text, counter):
    story = []
    lines = text.split("\n")
    i, para = 0, []
    pending_cap, pending_colw = None, None

    def flush():
        nonlocal para
        if para:
            story.append(Paragraph(inline(" ".join(para)), S["body"]))
            para = []

    while i < len(lines):
        ln = lines[i].rstrip()
        s = ln.strip()
        if s.startswith("```"):
            flush()
            j = i + 1
            while not lines[j].strip().startswith("```"):
                j += 1
            story += code_flow("\n".join(lines[i + 1:j]))
            i = j + 1
            continue
        if s.startswith("|"):
            flush()
            j = i
            while j < len(lines) and lines[j].strip().startswith("|"):
                j += 1
            story += table_flow(lines[i:j], pending_colw, pending_cap, counter)
            pending_cap = pending_colw = None
            i = j
            continue
        i += 1
        if not s:
            flush()
            continue
        if s.startswith("%"):  # comment
            continue
        if s.startswith("@"):
            flush()
            cmd, _, arg = s[1:].partition(" ")
            arg = arg.strip()
            if cmd in ("front", "part", "chapter") and story and not isinstance(story[-1], PageBreak):
                story.append(PageBreak())  # the cover already ends with a page break
            if cmd == "front":
                story += [Anchor("TOCEntry", 0, inline(arg), 0), Paragraph(inline(arg), S["front"])]
            elif cmd == "part":
                story += [Spacer(1, 9.5 * cm), Anchor("TOCEntry", 0, inline(arg), 0),
                          Paragraph(inline(arg), S["part"]), PageBreak()]
            elif cmd == "chapter":
                story += [Anchor("TOCEntry", 0, inline(arg), 1), Paragraph(inline(arg), S["chapter"])]
            elif cmd == "mode":
                parts = arg.split()
                story.append(Mode(None if parts[0] == "none" else parts[0], "reset" in parts))
            elif cmd == "sommaire":
                story.append(ListTOC("TOCEntry", 1, TOC_STYLES))
            elif cmd == "tdm":
                story.append(ListTOC("TOCEntry", 2, TOC_STYLES))
            elif cmd == "lof":
                story.append(ListTOC("FigEntry", 0, LIST_STYLE))
            elif cmd == "lot":
                story.append(ListTOC("TabEntry", 0, LIST_STYLE))
            elif cmd == "photo":
                # lines up to @endphoto on the left, the photo on the right
                p, wcm = [x.strip() for x in arg.split("|")]
                j = i
                while lines[j].strip() != "@endphoto":
                    j += 1
                left = parse("\n".join(lines[i:j]), counter)
                pw = float(wcm) * cm
                iw, ih = ImageReader(img_path(p)).getSize()
                photo = Image(img_path(p), width=pw, height=pw * ih / iw)
                t = Table([[left, photo]], colWidths=[FRAME_W - pw - 0.4 * cm, pw + 0.4 * cm])
                t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                                       ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                                       ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
                story.append(t)
                i = j + 1
            elif cmd == "img":
                p, frac, cap = [x.strip() for x in arg.split("|", 2)]
                story.append(image_flow(p, float(frac), cap, counter))
            elif cmd == "code":
                parts = arg.split()
                with open(os.path.join(HERE, "code", parts[0]), encoding="utf-8") as fh:
                    src = fh.read().split("\n")
                if len(parts) > 1:
                    a, b = parts[1].split("-")
                    src = src[int(a) - 1:(len(src) if b == "end" else int(b))]
                story += code_flow("\n".join(src))
            elif cmd == "tabcap":
                pending_cap = arg
            elif cmd == "colw":
                pending_colw = [float(x) for x in arg.split(",")]
            elif cmd == "gantt":
                counter["fig"] += 1
                cap = f"Figure {counter['fig']} : Diagramme de Gantt du projet"
                story.append(KeepTogether([gantt(), Anchor("FigEntry", 0, inline(cap)),
                                           Paragraph(inline(cap), S["figcap"])]))
            elif cmd == "pagebreak":
                story.append(PageBreak())
            elif cmd == "space":
                story.append(Spacer(1, float(arg)))
            elif cmd == "center":
                story.append(Paragraph(inline(arg), S["center"]))
            elif cmd == "right":
                story.append(Paragraph(inline(arg), S["right"]))
            else:
                raise ValueError(f"unknown directive @{cmd} (line {i})")
            continue
        if s.startswith("#### "):
            flush()
            story.append(Paragraph(inline(s[5:]), S["h3"]))
        elif s.startswith("### "):
            flush()
            story += [Anchor("TOCEntry", 2, inline(s[4:]), 3), Paragraph(inline(s[4:]), S["h2"])]
        elif s.startswith("## "):
            flush()
            story += [Anchor("TOCEntry", 1, inline(s[3:]), 2), Paragraph(inline(s[3:]), S["h1"])]
        elif s.startswith("= "):
            flush()
            heading = re.fullmatch(r"\*\*[^*]+\*\*", s[2:].strip())  # bold-only line: keep with what follows
            story.append(Paragraph(inline(s[2:]), S["plainkeep"] if heading else S["plain"]))
        elif ln.startswith("  - "):
            flush()
            story.append(Paragraph(inline(s[2:]), S["bullet2"], bulletText="–"))
        elif s.startswith("- "):
            flush()
            story.append(Paragraph(inline(s[2:]), S["bullet"], bulletText="➢"))
        else:
            para.append(s)
    flush()
    return story


def main(out):
    counter = {"fig": 0, "tab": 0}
    text = "\n".join(open(p, encoding="utf-8").read() for p in sorted(glob.glob(os.path.join(HERE, "content", "*.md"))))
    story = cover() + parse(text, counter)
    if isinstance(story[-1], PageBreak):
        story.pop()
    doc = Doc(out, pagesize=A4, leftMargin=ML, rightMargin=MR, topMargin=MT, bottomMargin=MB,
              title="Étude de la mise en place d'un pipeline CI/CD et orchestration pour une application en "
                    "architecture microservices",
              author="RAVELOMAHARAVO Rotsy Maminiaina Thierry Michaël",
              subject="Mémoire de fin d'études - Master professionnel - ENI Fianarantsoa")
    frame = Frame(ML, MB, FRAME_W, FRAME_H, id="f", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    cframe = Frame(ML, MB - 0.6 * cm, FRAME_W, FRAME_H + 1.2 * cm, id="c", leftPadding=0, rightPadding=0,
                   topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate("cover", [cframe], onPage=cover_page, onPageEnd=page_end),
                          PageTemplate("normal", [frame], onPageEnd=page_end)])
    doc.multiBuild(story, maxPasses=12)
    print("figures:", counter["fig"], "tables:", counter["tab"])


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "memoire.pdf"))
