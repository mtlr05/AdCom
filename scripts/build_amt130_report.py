"""Build data/amt130_report.pdf from data/amt130_report.md.

Run from anywhere. Reads the markdown next to the PDF it writes.
Supports headings, paragraphs, bold, code spans, bullets, tables, and images.
"""
import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image,
    ListFlowable, ListItem, CondPageBreak, HRFlowable,
)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MD = os.path.join(ROOT, "data", "amt130_report.md")
PDF = os.path.join(ROOT, "data", "amt130_report.pdf")


def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def rich(text):
    out = []
    i = 0
    while i < len(text):
        if text.startswith("**", i):
            j = text.find("**", i + 2)
            if j < 0:
                out.append(esc(text[i:]))
                break
            out.append("<b>" + esc(text[i + 2:j]) + "</b>")
            i = j + 2
        elif text[i] == "`":
            j = text.find("`", i + 1)
            if j < 0:
                out.append(esc(text[i:]))
                break
            out.append('<font face="Courier" size="8">' + esc(text[i + 1:j]) + "</font>")
            i = j + 1
        else:
            n = len(text)
            for m in ("**", "`"):
                k = text.find(m, i)
                if k >= 0:
                    n = min(n, k)
            out.append(esc(text[i:n]))
            i = n
    return "".join(out)


def styles():
    ss = getSampleStyleSheet()
    ss.add(ParagraphStyle(
        name="CoverTitle", fontName="Times-Bold", fontSize=18, leading=22,
        textColor=colors.HexColor("#1a1a1a"), spaceAfter=4, alignment=TA_LEFT))
    ss.add(ParagraphStyle(
        name="DateLine", fontName="Times-Italic", fontSize=11, leading=14,
        textColor=colors.HexColor("#333333"), spaceAfter=12))
    ss.add(ParagraphStyle(
        name="H2", fontName="Times-Bold", fontSize=14, leading=18,
        spaceBefore=16, spaceAfter=6, textColor=colors.HexColor("#1a1a1a")))
    ss.add(ParagraphStyle(
        name="H3", fontName="Times-Bold", fontSize=12, leading=15,
        spaceBefore=12, spaceAfter=4, textColor=colors.HexColor("#1a1a1a")))
    ss.add(ParagraphStyle(
        name="Body", fontName="Times-Roman", fontSize=11, leading=15,
        spaceAfter=8, alignment=TA_JUSTIFY))
    ss.add(ParagraphStyle(
        name="BulletBody", fontName="Times-Roman", fontSize=11, leading=15,
        alignment=TA_LEFT))
    ss.add(ParagraphStyle(
        name="Caption", fontName="Times-Italic", fontSize=9, leading=12,
        spaceBefore=3, spaceAfter=10, textColor=colors.HexColor("#222222")))
    ss.add(ParagraphStyle(
        name="Th", fontName="Times-Bold", fontSize=8, leading=10, textColor=colors.HexColor("#1a1a1a")))
    ss.add(ParagraphStyle(
        name="Td", fontName="Times-Roman", fontSize=8, leading=10))
    ss.add(ParagraphStyle(
        name="TdRight", fontName="Times-Roman", fontSize=8, leading=10, alignment=2))
    ss.add(ParagraphStyle(
        name="Footer", fontName="Times-Italic", fontSize=8, textColor=colors.HexColor("#444444")))
    return ss


def is_numericish(cell):
    s = cell.strip()
    if not s or s in ("---", "Off", "On", "Yes", "No", "None"):
        return s not in ("",)
    return bool(re.match(r"^[0-9].*|^Off$|^On$|^Yes$|^No$", s))


def make_table(rows, S):
    ncol = max(len(r) for r in rows)
    header, body = rows[0], rows[1:]
    # Drop a markdown separator if one slipped through.
    body = [r for r in body if not all(set(c.strip()) <= set("-: ") for c in r)]
    data = []
    aligns = []
    for j, h in enumerate(header):
        aligns.append("right" if j > 0 else "left")
    styled = [[Paragraph(rich(h), S["Th"]) for h in header]]
    for r in body:
        line = []
        for j in range(ncol):
            cell = r[j] if j < len(r) else ""
            st = S["TdRight"] if aligns[j] == "right" and is_numericish(cell) else S["Td"]
            line.append(Paragraph(rich(cell), st))
        styled.append(line)
    # Each column is at least as wide as its longest word, so a word does not
    # break mid-letter. Spare width goes to the column with the most text.
    from reportlab.pdfbase import pdfmetrics
    avail = 7.2 * inch
    mins = []
    bulk = []
    for j in range(ncol):
        texts = [header[j]] + [r[j] for r in body if j < len(r)]
        words = []
        chars = 0
        for t in texts:
            words.extend(w for w in re.split(r"\s+", t) if w)
            chars += len(t)
        widest = max((pdfmetrics.stringWidth(w, "Times-Bold", 8) for w in words), default=36)
        mins.append(widest + 10)
        bulk.append(chars)
    spare = avail - sum(mins)
    if spare < 0:
        scale = avail / sum(mins)
        widths = [m * scale for m in mins]
    else:
        widths = list(mins)
        widths[bulk.index(max(bulk))] += spare
    tbl = Table(styled, colWidths=widths, repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6e6e6")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#1a1a1a")),
        ("FONTNAME", (0, 0), (-1, 0), "Times-Bold"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#b0b0b0")),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f7f7f7")]),
    ]))
    return tbl


def parse(md, S):
    lines = md.splitlines()
    story = []
    i = 0
    first_h1 = True
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("# "):
            text = line[2:].strip()
            if first_h1:
                story.append(Paragraph(rich(text), S["CoverTitle"]))
                story.append(HRFlowable(width="100%", thickness=0.6, color=colors.HexColor("#1a1a1a"), spaceAfter=8))
                first_h1 = False
            else:
                story.append(Paragraph(rich(text), S["H2"]))
            i += 1
            continue
        if line.startswith("## "):
            text = line[3:].strip()
            if text.lower().startswith("appendix"):
                story.append(CondPageBreak(4.5 * inch))
            story.append(Paragraph(rich(text), S["H2"]))
            i += 1
            continue
        if line.startswith("### "):
            story.append(Paragraph(rich(line[4:].strip()), S["H3"]))
            i += 1
            continue
        if line.startswith("!["):
            m = re.match(r"!\[(.*?)\]\((.*?)\)", line.strip())
            if m:
                cap, rel = m.group(1), m.group(2)
                path = os.path.normpath(os.path.join(os.path.dirname(MD), rel))
                iw, ih = ImageReader(path).getSize()
                w = 7.1 * inch
                img = Image(path, width=w, height=w * ih / iw)
                img.hAlign = "CENTER"
                story.append(Spacer(1, 4))
                story.append(img)
                story.append(Paragraph(rich(cap), S["Caption"]))
            i += 1
            continue
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                raw = lines[i].strip().strip("|")
                cells = [c.strip() for c in raw.split("|")]
                if not all(set(c) <= set("-: ") and c for c in cells):
                    rows.append(cells)
                i += 1
            story.append(Spacer(1, 4))
            story.append(make_table(rows, S))
            story.append(Spacer(1, 8))
            continue
        if line.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append(ListItem(Paragraph(rich(lines[i][2:].strip()), S["BulletBody"]), leftIndent=12))
                i += 1
            story.append(ListFlowable(items, bulletType="bullet", start="•", leftIndent=16, bulletFontName="Times-Roman", spaceBefore=2, spaceAfter=8))
            continue
        # Date line sits alone under the title in this file.
        if re.match(r"^\d{1,2} [A-Z][a-z]+ \d{4}$", line.strip()) and first_h1 is False and len(story) <= 3:
            story.append(Paragraph(rich(line.strip()), S["DateLine"]))
            i += 1
            continue
        buf = [line.strip()]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(("#", "|", "-", "!")):
            buf.append(lines[i].strip())
            i += 1
        story.append(Paragraph(rich(" ".join(buf)), S["Body"]))
    return story


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#cccccc"))
    canvas.setLineWidth(0.4)
    canvas.line(doc.leftMargin, 0.55 * inch, letter[0] - doc.rightMargin, 0.55 * inch)
    canvas.setFont("Times-Italic", 8)
    canvas.setFillColor(colors.HexColor("#444444"))
    canvas.drawString(doc.leftMargin, 0.38 * inch, "AMT-130: a historical prior from FDA advisory committee votes")
    canvas.drawRightString(letter[0] - doc.rightMargin, 0.38 * inch, str(doc.page))
    canvas.restoreState()


def main():
    S = styles()
    doc = SimpleDocTemplate(
        PDF, pagesize=letter,
        leftMargin=0.7 * inch, rightMargin=0.7 * inch,
        topMargin=0.7 * inch, bottomMargin=0.7 * inch,
        title="AMT-130: a historical prior from FDA advisory committee votes",
        author="AdCom dataset",
    )
    text = open(MD, encoding="utf-8").read()
    story = parse(text, S)
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print("wrote", PDF, "pages", doc.page)


if __name__ == "__main__":
    main()
