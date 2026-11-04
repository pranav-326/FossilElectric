"""Build an editable BISL504 final presentation from the project CSV."""

from __future__ import annotations

import csv
import statistics
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "ev_vs_petrol_dataset_cleaned.csv"
OUT = ROOT / "BISL504_Final_Project_Presentation.pptx"
EMU = 914400
W, H = 13.333333 * EMU, 7.5 * EMU
NAVY, INK, MUTED, PAPER = "102A43", "183B56", "526777", "F7F9FA"
BLUE, ORANGE, GREEN, LINE, WHITE = "0072B2", "E69F00", "009E73", "D8E1E8", "FFFFFF"


def read_data():
    with CSV_PATH.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def esc(text):
    return escape(str(text), {"\n": "&#10;"})


class Slide:
    def __init__(self, title=None, subtitle=None, dark=False):
        self.dark = dark
        self.shapes = []
        self.i = 2
        bg = NAVY if dark else PAPER
        self.rect(0, 0, 13.333, 7.5, bg, line=bg)
        if title:
            self.text(0.72, 0.42, 11.9, 0.56, title, 27, NAVY if dark else INK, bold=True)
            self.rect(0.72, 1.08, 0.58, 0.045, BLUE)
            if subtitle:
                self.text(0.72, 1.20, 11.9, 0.40, subtitle, 12.5, MUTED if not dark else "C9D7E2")

    def shape(self, x, y, w, h, geom="rect", fill=None, line=None, width=1):
        sid = self.i
        self.i += 1
        x, y, w, h = (round(v * EMU) for v in (x, y, w, h))
        fill_xml = f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>' if fill else "<a:noFill/>"
        line_xml = f'<a:ln w="{int(width*12700)}"><a:solidFill><a:srgbClr val="{line}"/></a:solidFill></a:ln>' if line else "<a:ln><a:noFill/></a:ln>"
        self.shapes.append(
            f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="Shape {sid}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>'
            f'<a:prstGeom prst="{geom}"><a:avLst/></a:prstGeom>{fill_xml}{line_xml}</p:spPr></p:sp>'
        )
        return sid

    def rect(self, x, y, w, h, fill, line=None):
        return self.shape(x, y, w, h, fill=fill, line=line)

    def line(self, x1, y1, x2, y2, color=LINE, width=1):
        # PowerPoint line preset; negative extents are avoided by normalising endpoints.
        x, y = min(x1, x2), min(y1, y2)
        w, h = max(abs(x2 - x1), 0.001), max(abs(y2 - y1), 0.001)
        sid = self.i
        self.i += 1
        flip = ' flipV="1"' if (x2 - x1) * (y2 - y1) < 0 else ""
        self.shapes.append(
            f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="Line {sid}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm{flip}><a:off x="{round(x*EMU)}" y="{round(y*EMU)}"/><a:ext cx="{round(w*EMU)}" cy="{round(h*EMU)}"/></a:xfrm>'
            f'<a:prstGeom prst="line"><a:avLst/></a:prstGeom><a:ln w="{int(width*12700)}"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill></a:ln>'
            f'</p:spPr></p:sp>'
        )

    def text(self, x, y, w, h, value, size=16, color=INK, bold=False, font="Aptos", valign="ctr", margin=0.02):
        sid = self.i
        self.i += 1
        paragraphs = []
        for part in str(value).split("\n"):
            paragraphs.append(f'<a:p><a:pPr/><a:r><a:rPr lang="en-US" sz="{int(size*100)}" b="{1 if bold else 0}"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill><a:latin typeface="{font}"/></a:rPr><a:t>{esc(part)}</a:t></a:r><a:endParaRPr lang="en-US" sz="{int(size*100)}"/></a:p>')
        x, y, w, h = (round(v * EMU) for v in (x, y, w, h))
        self.shapes.append(
            f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="Text {sid}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>'
            f'<p:txBody><a:bodyPr wrap="square" anchor="{valign}" lIns="{int(margin*EMU)}" rIns="{int(margin*EMU)}" tIns="{int(margin*EMU)}" bIns="{int(margin*EMU)}"/><a:lstStyle/>{"".join(paragraphs)}</p:txBody></p:sp>'
        )

    def xml(self):
        sp_tree = '<p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>' + ''.join(self.shapes) + '</p:spTree>'
        return f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:cSld>{sp_tree}</p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>'


def footer(s, n, dark=False):
    c = "B7C9D7" if dark else MUTED
    s.text(11.45, 7.11, 1.25, 0.18, f"BISL504  /  {n:02d}", 8.5, c, valign="ctr")


def bullet_list(s, x, y, w, items, size=16, gap=0.72, color=INK, marker=BLUE):
    for i, item in enumerate(items):
        yy = y + i * gap
        s.rect(x, yy + 0.13, 0.09, 0.09, marker)
        s.text(x + 0.22, yy, w - 0.22, gap - 0.06, item, size, color, valign="ctr")


def build_slides(rows):
    slides = []
    # 1. Cover
    s = Slide(dark=True)
    s.rect(0.78, 1.00, 0.07, 4.55, BLUE)
    s.text(1.15, 1.10, 10.9, 0.38, "BISL504   /   DATA VISUALIZATION LAB", 13, "A9C7DB", bold=True)
    s.text(1.12, 2.03, 10.8, 1.45, "Electric vehicle\nadoption across countries", 36, WHITE, bold=True, valign="ctr")
    s.text(1.15, 4.10, 9.7, 0.78, "Interactive exploration of market share, vehicle sales,\ncharging infrastructure and transport emissions", 17, "D6E3EC")
    s.text(1.15, 6.48, 8, 0.28, "FINAL PROJECT PRESENTATION   •   V SEMESTER   •   2026–27", 11, "A9C7DB", bold=True)
    footer(s, 1, True)
    slides.append(s)

    # 2. Question and dataset
    s = Slide("Decision question and dataset", "Explore adoption patterns across 25 country markets from 2010 to 2025.")
    s.text(0.82, 1.95, 5.7, 0.34, "GUIDING QUESTION", 11, BLUE, bold=True)
    s.text(0.82, 2.35, 5.45, 1.35, "How has EV adoption changed, and how does it vary across countries?", 25, INK, bold=True)
    s.line(6.65, 1.94, 6.65, 6.15, LINE, 1.2)
    s.text(7.05, 1.95, 5.4, 0.34, "ANALYSIS FRAME", 11, BLUE, bold=True)
    for j, (big, small) in enumerate([("400", "country-year rows"), ("25", "countries"), ("16 years", "2010–2025")]):
        y = 2.42 + j * 1.03
        s.text(7.05, y, 1.55, 0.50, big, 23, INK, bold=True)
        s.text(8.78, y + 0.07, 3.6, 0.42, small, 15, MUTED)
    s.text(0.82, 4.63, 5.45, 0.82, "Intended reader: an analyst comparing country adoption patterns and deciding where to investigate further.", 15, MUTED)
    s.rect(0.82, 5.72, 11.55, 0.72, "EAF2F7")
    s.text(1.02, 5.82, 11.1, 0.50, "Data provenance and licence are not recorded in the project files; confirm them before submission.", 13, INK, bold=True)
    footer(s, 2)
    slides.append(s)

    # 3. Preparation and honest scope
    s = Slide("Preparation and analytical scope", "A reproducible build turns the selected-column source into the country-year analysis table.")
    bullet_list(s, 0.9, 2.02, 5.5, [
        "1,200 source rows become 400 country-year rows across 25 countries.",
        "Each country-year has three source records; the file has no segment key explaining them.",
        "Vehicle sales are summed; shared metrics are kept once only where all three agree.",
        "Derived total sales, EV share and year-over-year growth are recalculated.",
    ], size=14, gap=0.82)
    s.line(6.7, 1.98, 6.7, 5.92, LINE, 1.2)
    s.text(7.08, 2.04, 5.25, 0.4, "DATA CHECKS", 11, BLUE, bold=True)
    s.text(7.08, 2.50, 5.15, 0.68, "0 exact duplicate rows; 0 missing country/year identifiers; 0 negative sales values.", 15, INK, bold=True)
    s.text(7.08, 3.43, 5.15, 0.78, "25 missing growth values are the first year for each country, where no prior year exists.", 14, MUTED)
    s.text(7.08, 4.48, 5.15, 0.96, "IQR flags 50 market-share, 39 station-count, 32 emissions and 46 EV-sales candidates; none are deleted without evidence.", 13, INK)
    s.rect(0.9, 5.92, 11.3, 0.58, "FFF3D8")
    s.text(1.08, 6.00, 10.95, 0.38, "Verify the meaning of the three source records per country-year before treating their sales sum as valid.", 12, INK, bold=True)
    footer(s, 3)
    slides.append(s)

    # 4. Dashboard interactions
    s = Slide("Dashboard structure and interaction", "A shared filter frame keeps the headline measures and charts in sync.")
    labels = [(0.95, "Country selection"), (4.05, "Shared filtered rows"), (8.05, "Year range + measure")]
    for x, label in labels:
        s.text(x, 2.18, 2.25, 0.55, label, 15, INK, bold=True)
    s.line(3.15, 2.47, 3.75, 2.47, BLUE, 2)
    s.line(7.15, 2.47, 7.75, 2.47, BLUE, 2)
    s.text(0.95, 3.45, 3.0, 1.85, "KPI strip\nMean share · EV sales · countries", 14, MUTED)
    s.text(4.65, 3.45, 3.45, 1.85, "Main views\nMarket-share trend · country ranking\nCharging stations vs share · emissions", 14, MUTED)
    s.text(9.0, 3.45, 3.0, 1.85, "Explore further\nSales-mix drill-down\nHover details · CSV download", 14, MUTED)
    s.line(0.95, 3.12, 12.0, 3.12, LINE, 1)
    s.text(0.95, 5.85, 10.9, 0.62, "Demo: change a country or year range, switch the trend measure, open a country detail, then export the filtered rows.", 15, BLUE, bold=True)
    footer(s, 4)
    slides.append(s)

    # 5. Mean time trend
    by_year = {}
    for r in rows:
        by_year.setdefault(int(r["year"]), []).append(float(r["ev_market_share"]))
    years = [2010, 2015, 2020, 2025]
    vals = [statistics.mean(by_year[y]) for y in years]
    s = Slide("EV market share rose across the country sample", "Unweighted mean of country-level market share; values are percentages.")
    x0, x1, y0, y1 = 1.65, 10.95, 5.75, 2.10
    s.line(x0, y0, x1, y0, MUTED, 1)
    for val in [0, 5, 10, 15, 20, 25]:
        y = y0 - (val / 25) * (y0 - y1)
        s.line(x0, y, x1, y, "E5EBF0", 0.55)
        s.text(0.93, y - 0.12, 0.55, 0.22, str(val), 10, MUTED)
    points = []
    for yr, val in zip(years, vals):
        x = x0 + ((yr - 2010) / 15) * (x1 - x0)
        y = y0 - (val / 25) * (y0 - y1)
        points.append((x, y))
        s.text(x - 0.30, y0 + 0.16, 0.75, 0.26, str(yr), 10.5, MUTED)
    for a, b in zip(points, points[1:]):
        s.line(a[0], a[1], b[0], b[1], BLUE, 2.2)
    for (x, y), val in zip(points, vals):
        s.shape(x - 0.065, y - 0.065, 0.13, 0.13, geom="ellipse", fill=BLUE)
        s.text(x - 0.42, y - 0.48, 0.95, 0.25, f"{val:.2f}%", 11, INK, bold=True)
    s.text(1.02, 6.38, 11, 0.34, "2010: 0.03%     →     2015: 1.25%     →     2020: 8.24%     →     2025: 21.67%", 13, INK, bold=True)
    footer(s, 5)
    slides.append(s)

    # 6. Country ranking
    latest = [r for r in rows if int(r["year"]) == 2025]
    top = sorted([(r["country"], float(r["ev_market_share"])) for r in latest], key=lambda z: -z[1])[:8]
    s = Slide("Country differences remain wide in 2025", "EV market share by country; a sorted bar makes the ranking easy to compare.")
    bx, bw, by, row_h = 2.3, 7.6, 2.05, 0.49
    for name, val in top:
        y = by + (top.index((name, val))) * row_h
        s.text(0.95, y - 0.03, 1.24, 0.32, name, 13, INK, bold=(name == "Norway"))
        s.rect(bx, y + 0.04, bw * val / 85, 0.24, BLUE if name == "Norway" else "7DAECC")
        s.text(bx + bw * val / 85 + 0.12, y - 0.04, 0.95, 0.34, f"{val:.2f}%", 12, INK, bold=True)
    s.text(10.25, 2.16, 2.2, 0.55, "79.96%", 22, BLUE, bold=True)
    s.text(10.25, 2.75, 2.15, 0.66, "Norway led the 2025 sample.", 13, MUTED)
    s.text(10.25, 4.20, 2.25, 0.50, "ρ = 0.88", 21, BLUE, bold=True)
    s.text(10.25, 4.78, 2.35, 1.10, "Spearman rank association for 375 country-years with positive station counts.", 12, MUTED)
    s.text(0.95, 6.45, 11.2, 0.32, "Country and time differences may confound the pooled association; it is not causal evidence.", 12, MUTED)
    footer(s, 6)
    slides.append(s)

    # 7. Refinement status
    s = Slide("Accessibility and iteration evidence", "The interface uses a colour-blind-safe palette; peer-test evidence still needs to be collected.")
    s.text(0.95, 2.02, 5.3, 0.4, "IN THE DASHBOARD", 11, BLUE, bold=True)
    bullet_list(s, 0.95, 2.48, 5.2, [
        "Blue, orange and green are distinct Okabe–Ito colours.",
        "Views use labels and tooltips; colour is not the only cue.",
        "Charts have plain titles, labelled units and restrained gridlines.",
    ], size=14, gap=0.82)
    s.line(6.65, 1.98, 6.65, 5.92, LINE, 1.2)
    s.text(7.02, 2.02, 5.3, 0.4, "BEFORE SUBMISSION", 11, ORANGE, bold=True)
    bullet_list(s, 7.02, 2.48, 5.25, [
        "Check contrast and colour-vision simulation on the projected display.",
        "Run the three-task peer test with the author silent.",
        "Record answer correctness and time; fix the two main hesitations.",
        "Add real before/after screenshots and the iteration log.",
        "Append the AI disclosure and one real, reasoned AI-suggestion rejection.",
    ], size=13.5, gap=0.68, marker=ORANGE)
    s.rect(0.95, 6.05, 11.4, 0.55, "FFF3D8")
    s.text(1.12, 6.12, 10.9, 0.34, "No usability findings or screenshot evidence are present in the current repository.", 12, INK, bold=True)
    footer(s, 7)
    slides.append(s)

    # 8. Limitations and close
    s = Slide("Limitations and next steps", "The dashboard supports exploration; the dataset sets the limits on what can be concluded.")
    bullet_list(s, 0.95, 2.00, 6.3, [
        "Confirm the source and reuse licence for the dataset.",
        "Country averages are unweighted; totals are not population-normalised.",
        "Association between stations and market share is not causal evidence.",
        "Transport emissions include more than passenger cars and EV adoption.",
    ], size=14.5, gap=0.78)
    s.line(7.5, 2.0, 7.5, 5.55, LINE, 1.2)
    s.text(7.9, 2.02, 4.6, 0.4, "NEXT", 11, BLUE, bold=True)
    s.text(7.9, 2.54, 4.5, 1.12, "Verify provenance, complete the usability iteration, and rehearse a live change to a filter or chart.", 21, INK, bold=True)
    s.text(7.9, 4.34, 4.4, 0.75, "Thank you\nQuestions", 17, BLUE, bold=True)
    s.text(0.95, 6.18, 11.1, 0.42, "The live presentation and viva are unaided; rehearse beforehand and make sure every member can explain their contribution.", 12, MUTED)
    footer(s, 8)
    slides.append(s)
    return slides


def write_pptx(slides):
    # Start from an eight-slide blank package created by PowerPoint itself, then
    # replace only slide contents. This keeps the deck compatible with Office.
    base = ROOT / "presentation_base.pptx"
    if not base.is_file():
        raise FileNotFoundError("presentation_base.pptx is required beside this script")
    with zipfile.ZipFile(base, "r") as source, zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as target:
        for name in source.namelist():
            if name.startswith("ppt/slides/slide") and name.endswith(".xml"):
                index = int(Path(name).stem.removeprefix("slide")) - 1
                target.writestr(name, slides[index].xml())
            else:
                target.writestr(name, source.read(name))
    return




if __name__ == "__main__":
    slides = build_slides(read_data())
    write_pptx(slides)
    print(f"Created {OUT} with {len(slides)} slides")
