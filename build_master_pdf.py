"""Master schedule poster -- one landscape (tabloid) page per day."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from schedule_data import SLOTS, DAY_INFO, team_display, TOURNAMENT_NAME
from menu_rules_data import (FOOD_TRUCK_VENDOR, FOOD_TRUCK_TAGLINE, FOOD_TRUCK_ITEMS,
                              FOOD_TRUCK_NOTE, DRINKS_SNACKS, RULES_SECTIONS)
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph, Frame, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT

PAGE_W, PAGE_H = 17 * inch, 11 * inch

NAVY_DARK  = HexColor("#081849")   # hero/header bg (was field green)
CREAM      = HexColor("#ECDFD2")   # page/card bg + light text-on-dark (was chalk white)
LAPIS      = HexColor("#213885")   # Diamond 1 + Scorekeeping badge (was twilight navy)
PLUM       = HexColor("#5F3475")   # Diamond 2 (was clay brown)
MAGENTA    = HexColor("#893172")   # Beer tent badge fill (was scoreboard gold)
MUTED      = HexColor("#7A7482")   # secondary text (was muted gray)
LINE       = HexColor("#CCCACC")   # borders/dividers
INK        = HexColor("#081849")   # main text ink
DARK_MUTED = HexColor("#C7BFC9")   # muted light text on dark hero bg
TINT       = HexColor("#DFD5C8")   # buffer/lunch row bg (subtly distinct from CREAM)

F_DISPLAY = "Helvetica-Bold"
F_BODY    = "Helvetica"
F_BODYB   = "Helvetica-Bold"
F_MONO    = "Courier-Bold"

def diamond_marker(c, cx, cy, size, color):
    c.saveState()
    c.translate(cx, cy)
    c.rotate(45)
    c.setFillColor(color)
    c.rect(-size/2, -size/2, size, size, fill=1, stroke=0)
    c.restoreState()

def duty_badge(c, x, y, letter, label, bg, letter_color, label_color=None):
    if label_color is None:
        label_color = INK
    r = 9
    c.setFillColor(bg)
    c.circle(x, y, r, fill=1, stroke=0)
    c.setFillColor(letter_color)
    c.setFont(F_BODYB, 9)
    c.drawCentredString(x, y - 3.2, letter)
    c.setFillColor(label_color)
    c.setFont(F_BODY, 10.5)
    c.drawString(x + r + 6, y - 3.5, label)

def fit_text(c, text, font, max_width, max_size, min_size=11):
    size = max_size
    while size > min_size and c.stringWidth(text, font, size) > max_width:
        size -= 1
    return size

def draw_header(c, display_label, day_key):
    c.setFillColor(NAVY_DARK)
    c.rect(0, PAGE_H - 100, PAGE_W, 100, fill=1, stroke=0)
    c.setFillColor(CREAM)
    c.setFont(F_BODYB, 13)
    c.drawString(0.5*inch, PAGE_H - 34, f"{TOURNAMENT_NAME.upper()}  \u2014  MASTER SCHEDULE")
    c.setFillColor(CREAM)
    c.setFont(F_DISPLAY, 44 if len(display_label) > 10 else 52)
    c.drawString(0.5*inch, PAGE_H - 88, display_label.upper())
    c.setFont(F_BODY, 14)
    c.drawRightString(PAGE_W - 0.5*inch, PAGE_H - 50, DAY_INFO[day_key]["hours"])

def draw_legend(c, top_y):
    y = top_y
    c.setFillColor(CREAM)
    c.rect(0, y - 34, PAGE_W, 34, fill=1, stroke=0)
    x = 0.5*inch
    diamond_marker(c, x, y - 17, 12, LAPIS)
    c.setFillColor(INK); c.setFont(F_BODYB, 10.5)
    c.drawString(x + 14, y - 21, "DIAMOND 1")
    x += 1.5*inch
    diamond_marker(c, x, y - 17, 12, PLUM)
    c.drawString(x + 14, y - 21, "DIAMOND 2")
    x += 1.7*inch
    duty_badge(c, x, y - 17, "S", "Scorekeeping (2 players)", LAPIS, CREAM)
    x += 2.9*inch
    duty_badge(c, x, y - 17, "B", "Beer tent (2 players)", MAGENTA, CREAM)
    c.setStrokeColor(LINE); c.setLineWidth(1)
    c.line(0, y - 34, PAGE_W, y - 34)

def draw_game_half(c, x, w, top, h, diamond_color, diamond_label, teams, scorer, day):
    pad = 16
    diamond_marker(c, x + pad, top - 15, 10, diamond_color)
    c.setFillColor(MUTED); c.setFont(F_BODYB, 8.5)
    c.drawString(x + pad + 13, top - 18, diamond_label.upper())
    c.setFillColor(INK)
    t1, t2 = team_display(teams[0]), team_display(teams[1])
    text = f"{t1}  vs  {t2}"
    avail_w = w - pad - 14
    fsize = fit_text(c, text, F_DISPLAY, avail_w, 20 if h > 80 else 16, min_size=11)
    c.setFont(F_DISPLAY, fsize)
    c.drawString(x + pad, top - (42 if h > 80 else 36), text)
    if scorer and h > 55:
        badge_y = top - h + 12
        duty_badge(c, x + pad + 9, badge_y, "S", f"Scorekeeping (2 players): {team_display(scorer)}", LAPIS, CREAM)

def draw_special_row(c, top, h, label, beer_team, kind):
    c.setFillColor(TINT if kind in ("buffer","lunch") else NAVY_DARK)
    c.rect(0.5*inch, top - h, PAGE_W - 1*inch, h, fill=1, stroke=0)
    c.setFillColor(INK if kind in ("buffer","lunch") else CREAM)
    c.setFont("Helvetica-Oblique" if kind in ("buffer","lunch") else F_DISPLAY,
              14 if kind in ("buffer","lunch") else 22)
    c.drawCentredString(PAGE_W/2, top - h/2 - 5, label)
    if beer_team:
        duty_badge(c, PAGE_W/2 + 3.6*inch, top - h/2 - 5, "B",
                   f"Beer tent (2 players): {team_display(beer_team)}", MAGENTA, CREAM)

MAX_ROWS_PER_PAGE = 5

def chunk_even(lst, max_per_page):
    n = len(lst)
    num_pages = max(1, math.ceil(n / max_per_page))
    base, extra = divmod(n, num_pages)
    pages, i = [], 0
    for p in range(num_pages):
        size = base + (1 if p < extra else 0)
        pages.append(lst[i:i+size])
        i += size
    return pages

def draw_simple_header(c, title, subtitle=None):
    c.setFillColor(NAVY_DARK)
    c.rect(0, PAGE_H - 100, PAGE_W, 100, fill=1, stroke=0)
    c.setFillColor(CREAM)
    c.setFont(F_BODYB, 13)
    c.drawString(0.5*inch, PAGE_H - 34, TOURNAMENT_NAME.upper())
    c.setFillColor(CREAM)
    c.setFont(F_DISPLAY, 44 if len(title) > 18 else 52)
    c.drawString(0.5*inch, PAGE_H - 88, title.upper())
    if subtitle:
        c.setFont(F_BODY, 14)
        c.drawRightString(PAGE_W - 0.5*inch, PAGE_H - 50, subtitle)

def draw_price_row(c, x, y, name, price, col_width, name_font_size=11):
    c.setFillColor(INK)
    c.setFont(F_BODY, name_font_size)
    c.drawString(x, y, name)
    c.setFont(F_BODYB, name_font_size)
    price_w = c.stringWidth(price, F_BODYB, name_font_size)
    c.drawString(x + col_width - price_w, y, price)
    name_w = c.stringWidth(name, F_BODY, name_font_size)
    leader_start = x + name_w + 6
    leader_end = x + col_width - price_w - 6
    if leader_end > leader_start:
        c.saveState()
        c.setDash(1, 2)
        c.setStrokeColor(LINE)
        c.line(leader_start, y + name_font_size*0.32, leader_end, y + name_font_size*0.32)
        c.restoreState()

def build_menu_page(c):
    draw_simple_header(c, "Food & Concession", "Foodie LU  \u00b7  Drinks & Snacks")
    margin = 0.6*inch
    top = PAGE_H - 100 - 0.5*inch
    col_gap = 0.6*inch
    col_w = (PAGE_W - 2*margin - col_gap) / 2

    x = margin
    y = top
    c.setFillColor(LAPIS)
    c.setFont(F_DISPLAY, 24)
    c.drawString(x, y, "FOOD TRUCK  \u2014  " + FOOD_TRUCK_VENDOR)
    y -= 22
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Oblique", 12)
    c.drawString(x, y, FOOD_TRUCK_TAGLINE)
    y -= 18
    c.setStrokeColor(LINE)
    c.line(x, y, x + col_w, y)
    y -= 28
    for name, price in FOOD_TRUCK_ITEMS:
        draw_price_row(c, x, y, name, price, col_w, name_font_size=13)
        y -= 30
    y -= 8
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Oblique", 10.5)
    c.drawString(x, y, FOOD_TRUCK_NOTE)

    x2 = margin + col_w + col_gap
    y2 = top
    c.setFillColor(PLUM)
    c.setFont(F_DISPLAY, 24)
    c.drawString(x2, y2, "DRINKS & SNACKS")
    y2 -= 22
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Oblique", 12)
    c.drawString(x2, y2, "2026 Price List")
    y2 -= 18
    c.setStrokeColor(LINE)
    c.line(x2, y2, x2 + col_w, y2)
    y2 -= 30
    for section_name, items in DRINKS_SNACKS:
        c.setFillColor(NAVY_DARK)
        c.setFont(F_BODYB, 14)
        c.drawString(x2, y2, section_name.upper())
        y2 -= 22
        for name, price in items:
            draw_price_row(c, x2, y2, name, price, col_w, name_font_size=12)
            y2 -= 24
        y2 -= 14

    c.showPage()

def build_rules_pages(c):
    section_style = ParagraphStyle('Section', fontName=F_DISPLAY, fontSize=12.5,
                                    textColor=LAPIS, spaceBefore=8, spaceAfter=4, leading=15)
    body_style = ParagraphStyle('Body', fontName=F_BODY, fontSize=8.6,
                                 textColor=INK, leading=11.2, spaceAfter=6, alignment=TA_LEFT)

    flowables = []
    for title, paragraphs in RULES_SECTIONS:
        flowables.append(Paragraph(title, section_style))
        for p in paragraphs:
            flowables.append(Paragraph(p, body_style))

    margin = 0.5 * inch
    col_gap = 0.35 * inch
    n_cols = 3
    col_w = (PAGE_W - 2*margin - (n_cols-1)*col_gap) / n_cols
    header_h = 100
    top_pad = 20
    bottom_margin = 0.4 * inch
    frame_top = PAGE_H - header_h - top_pad
    col_height = frame_top - bottom_margin

    page_num = 1
    col_idx = 0
    y = frame_top
    title = "Tournament Rules"
    draw_simple_header(c, title, "2026 BLSA End of Year Tournament")

    for flowable in flowables:
        w, h = flowable.wrap(col_w, col_height)
        if h > col_height:
            h = col_height  # safety: never let one flowable exceed a column
        extra = 24 if flowable.style is section_style else 0  # keep section titles from being stranded alone
        if y - h - extra < bottom_margin:
            col_idx += 1
            y = frame_top
            if col_idx >= n_cols:
                c.showPage()
                page_num += 1
                col_idx = 0
                draw_simple_header(c, "Tournament Rules (cont'd)", "2026 BLSA End of Year Tournament")
        x = margin + col_idx * (col_w + col_gap)
        flowable.drawOn(c, x, y - h)
        y -= h

    c.showPage()

def build():
    c = canvas.Canvas(os.path.join(os.path.dirname(os.path.abspath(__file__)), "master_schedule.pdf"), pagesize=(PAGE_W, PAGE_H))
    for day in ["Friday", "Saturday", "Sunday"]:
        day_slots = [s for s in SLOTS if s["day"] == day]
        pages = chunk_even(day_slots, MAX_ROWS_PER_PAGE)
        for page_i, page_slots in enumerate(pages):
          label = day if len(pages) == 1 else f"{day} (Part {page_i+1}/{len(pages)})"
          draw_header(c, label, day)
          legend_top = PAGE_H - 100
          draw_legend(c, legend_top)
          body_top = legend_top - 34 - 10
          body_bottom = 0.4 * inch
          n = len(page_slots)
          gap = 10
          row_h = (body_top - body_bottom - gap * (n - 1)) / n
          row_h = min(row_h, 150)
          y = body_top
          margin = 0.5 * inch
          col_gap = 0.25 * inch
          half_w = (PAGE_W - 2*margin - col_gap) / 2
          for s in page_slots:
            top = y
            if s["kind"] in ("game", "playoff") and s.get("d1") and isinstance(s.get("d1"), tuple):
                c.setFillColor(CREAM)
                c.setStrokeColor(LINE)
                c.rect(margin, top - row_h, PAGE_W - 2*margin, row_h, fill=1, stroke=1)
                c.setFont(F_MONO, 15)
                c.setFillColor(LAPIS)
                c.drawString(margin + 10, top - 20, f"{s['start']} \u2013 {s['end']}")
                beer_strip_h = 26 if s.get("beer") else 0
                half_h = row_h - 22 - beer_strip_h
                lx = margin
                draw_game_half(c, lx, half_w, top - 22, half_h,
                                LAPIS, "Diamond 1", s["d1"], s.get("score1"), day)
                rx = margin + half_w + col_gap
                c.setStrokeColor(LINE)
                c.line(rx - col_gap/2, top - row_h, rx - col_gap/2, top)
                draw_game_half(c, rx, half_w, top - 22, half_h,
                                PLUM, "Diamond 2", s["d2"], s.get("score2"), day)
                if s.get("beer"):
                    c.setStrokeColor(LINE)
                    c.line(margin + 10, top - row_h + beer_strip_h, PAGE_W - margin - 10, top - row_h + beer_strip_h)
                    txt = f"Beer tent (2 players): {team_display(s['beer'])}"
                    tw = c.stringWidth(txt, F_BODY, 10.5) + 26
                    duty_badge(c, PAGE_W/2 - tw/2, top - row_h + 13, "B", txt, MAGENTA, CREAM)
            elif s["kind"] == "playoff":
                label = s["label"]
                c.setFillColor(NAVY_DARK)
                c.rect(margin, top - row_h, PAGE_W - 2*margin, row_h, fill=1, stroke=0)
                c.setFillColor(CREAM); c.setFont(F_MONO, 15)
                c.drawString(margin + 14, top - 24, f"{s['start']} \u2013 {s['end']}")
                c.setFillColor(CREAM); c.setFont(F_DISPLAY, 26)
                c.drawCentredString(PAGE_W/2, top - row_h/2 - 2, label)
                c.setFillColor(DARK_MUTED); c.setFont(F_BODY, 10.5)
                c.drawCentredString(PAGE_W/2, top - row_h + 22, "Scorekeeping: Tournament Execs")
                if s.get("beer"):
                    duty_badge(c, PAGE_W - margin - 4.3*inch, top - 24, "B",
                               f"Beer tent (2 players): {team_display(s['beer'])}", MAGENTA, CREAM, CREAM)
            else:
                draw_special_row(c, top, row_h, s.get("label",""), s.get("beer"), s["kind"])
            y -= row_h + gap
          c.showPage()
    build_menu_page(c)
    build_rules_pages(c)
    c.save()

if __name__ == "__main__":
    build()
    print("done")
