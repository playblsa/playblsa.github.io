"""Individual team schedule cards -- one portrait Letter page per team."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from schedule_data import TEAM_NAMES, team_display, team_pool, team_games, TOURNAMENT_NAME
from menu_rules_data import (FOOD_TRUCK_VENDOR, FOOD_TRUCK_TAGLINE, FOOD_TRUCK_ITEMS,
                              FOOD_TRUCK_NOTE, DRINKS_SNACKS, RULES_SECTIONS)
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT

PAGE_W, PAGE_H = letter

NAVY_DARK  = HexColor("#081849")
CREAM      = HexColor("#ECDFD2")
LAPIS      = HexColor("#213885")
PLUM       = HexColor("#5F3475")
MAGENTA    = HexColor("#893172")
MUTED      = HexColor("#7A7482")
LINE       = HexColor("#CCCACC")
INK        = HexColor("#081849")
DARK_MUTED = HexColor("#C7BFC9")

F_DISPLAY = "Helvetica-Bold"
F_BODY    = "Helvetica"
F_BODYB   = "Helvetica-Bold"
F_MONO    = "Courier-Bold"

DAY_ORDER = ["Friday", "Saturday", "Sunday"]

def diamond_marker(c, cx, cy, size, color, rotate=45):
    c.saveState()
    c.translate(cx, cy)
    c.rotate(rotate)
    c.setFillColor(color)
    c.rect(-size/2, -size/2, size, size, fill=1, stroke=0)
    c.restoreState()

def role_badge(c, x, y, letter, bg, fg, r=13):
    c.setFillColor(bg)
    c.circle(x, y, r, fill=1, stroke=0)
    c.setFillColor(fg)
    c.setFont(F_BODYB, 12)
    c.drawCentredString(x, y - 4.2, letter)

def fit_text(c, text, font, max_width, max_size, min_size=10):
    size = max_size
    while size > min_size and c.stringWidth(text, font, size) > max_width:
        size -= 1
    return size

HEADER_H = 132

def draw_header(c, team_code):
    pool = team_pool(team_code)
    accent = LAPIS if pool == "A" else PLUM
    c.setFillColor(NAVY_DARK)
    c.rect(0, PAGE_H - HEADER_H, PAGE_W, HEADER_H, fill=1, stroke=0)
    c.setFillColor(CREAM)
    c.setFont(F_BODYB, 11)
    c.drawString(0.55*inch, PAGE_H - 28, TOURNAMENT_NAME.upper())
    c.setFillColor(CREAM)
    c.setFont(F_BODY, 11)
    c.drawRightString(PAGE_W - 0.55*inch, PAGE_H - 28, "Personal Schedule Card")
    name = team_display(team_code)
    fsize = fit_text(c, name.upper(), F_DISPLAY, PAGE_W - 1.1*inch, 40, min_size=22)
    c.setFont(F_DISPLAY, fsize)
    c.drawString(0.55*inch, PAGE_H - 76, name.upper())
    chip_w = 88
    c.setFillColor(accent)
    c.roundRect(0.55*inch, PAGE_H - 108, chip_w, 22, 4, fill=1, stroke=0)
    c.setFillColor(CREAM)
    c.setFont(F_BODYB, 10.5)
    c.drawCentredString(0.55*inch + chip_w/2, PAGE_H - 100.5, f"POOL {pool}")
    c.setFillColor(DARK_MUTED)
    c.setFont(F_BODY, 10)
    c.drawString(0.55*inch + chip_w + 12, PAGE_H - 100.5,
                 "4 pool-play games  \u00b7  no back-to-back games")

def draw_legend(c, top_y):
    y = top_y
    c.setFillColor(CREAM)
    c.rect(0, y - 30, PAGE_W, 30, fill=1, stroke=0)
    x = 0.55*inch
    diamond_marker(c, x, y - 15, 11, LAPIS)
    c.setFillColor(INK); c.setFont(F_BODYB, 9.5)
    c.drawString(x + 12, y - 18.5, "DIAMOND 1")
    x += 1.35*inch
    diamond_marker(c, x, y - 15, 11, PLUM)
    c.drawString(x + 12, y - 18.5, "DIAMOND 2")
    x += 1.5*inch
    role_badge(c, x, y - 15, "S", LAPIS, CREAM, r=8)
    c.drawString(x + 12, y - 18.5, "SCOREKEEP")
    x += 1.35*inch
    role_badge(c, x, y - 15, "B", MAGENTA, CREAM, r=8)
    c.drawString(x + 12, y - 18.5, "BEER TENT")
    c.setStrokeColor(LINE); c.line(0, y - 30, PAGE_W, y - 30)

def draw_day_divider(c, top, day):
    h = 19
    c.setFillColor(NAVY_DARK)
    c.rect(0.55*inch, top - h, PAGE_W - 1.1*inch, h, fill=1, stroke=0)
    c.setFillColor(CREAM)
    c.setFont(F_BODYB, 11)
    c.drawString(0.55*inch + 10, top - h + 5.5, day.upper())
    return top - h

def draw_entry(c, top, h, game, team_code):
    s = game["slot"]
    role = game["role"]
    margin = 0.55*inch
    width = PAGE_W - 2*margin
    c.setFillColor(CREAM)
    c.setStrokeColor(LINE)
    c.rect(margin, top - h, width, h, fill=1, stroke=1)

    diamond_color = LAPIS if game.get("diamond") == "Diamond 1" else PLUM
    if s["kind"] == "playoff":
        diamond_color = MAGENTA

    c.setFont(F_MONO, 12)
    c.setFillColor(LAPIS)
    c.drawString(margin + 12, top - 19, f"{s['start']} \u2013 {s['end']}")
    c.setFillColor(MUTED); c.setFont(F_BODYB, 8)
    if game.get("diamond"):
        c.drawRightString(PAGE_W - margin - 12, top - 19, game["diamond"].upper())

    if role == "play":
        role_badge(c, margin + 26, top - 41, "P", diamond_color, CREAM, r=11)
        opp = team_display(game["opponent"])
        text = f"{team_display(team_code)}  vs  {opp}"
        avail_w = width - 46 - 14
        fsize = fit_text(c, text, F_DISPLAY, avail_w, 16.5, min_size=11)
        c.setFillColor(INK); c.setFont(F_DISPLAY, fsize)
        c.drawString(margin + 46, top - 45, text)
        c.setFillColor(MUTED); c.setFont(F_BODY, 8.7)
        c.drawString(margin + 46, top - 57,
                     "Playoff game" if s["kind"] == "playoff" else "Pool play game")
    elif role == "score":
        role_badge(c, margin + 26, top - 41, "S", LAPIS, CREAM, r=11)
        c.setFillColor(INK); c.setFont(F_BODYB, 13.5)
        c.drawString(margin + 46, top - 43, "Scorekeeping duty (2 players)")
        c.setFillColor(MUTED); c.setFont(F_BODY, 8.7)
        pair = s.get("d1") if game["diamond"] == "Diamond 1" else s.get("d2")
        if isinstance(pair, tuple):
            txt = f"{game['diamond']}: {team_display(pair[0])} vs {team_display(pair[1])}"
            avail_w = width - 46 - 14
            fsize2 = fit_text(c, txt, F_BODY, avail_w, 8.7, min_size=7)
            c.setFont(F_BODY, fsize2)
            c.drawString(margin + 46, top - 57, txt)
    elif role == "beer":
        role_badge(c, margin + 26, top - 41, "B", MAGENTA, CREAM, r=11)
        c.setFillColor(INK); c.setFont(F_BODYB, 13.5)
        c.drawString(margin + 46, top - 43, "Beer tent duty (2 players)")
        c.setFillColor(MUTED); c.setFont(F_BODY, 8.7)
        c.drawString(margin + 46, top - 57, "Send 2 players who aren't playing that slot")

def draw_ref_header(c, title, subtitle=None):
    c.setFillColor(NAVY_DARK)
    c.rect(0, PAGE_H - HEADER_H, PAGE_W, HEADER_H, fill=1, stroke=0)
    c.setFillColor(CREAM)
    c.setFont(F_BODYB, 11)
    c.drawString(0.55*inch, PAGE_H - 28, TOURNAMENT_NAME.upper())
    fsize = fit_text(c, title.upper(), F_DISPLAY, PAGE_W - 1.1*inch, 34, min_size=20)
    c.setFont(F_DISPLAY, fsize)
    c.drawString(0.55*inch, PAGE_H - 70, title.upper())
    if subtitle:
        c.setFillColor(DARK_MUTED)
        c.setFont(F_BODY, 10.5)
        c.drawString(0.55*inch, PAGE_H - 92, subtitle)

def draw_price_row(c, x, y, name, price, col_width, name_font_size=12):
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

def draw_food_truck_page(c):
    draw_ref_header(c, "Food Truck Menu", f"{FOOD_TRUCK_VENDOR} \u2014 {FOOD_TRUCK_TAGLINE}")
    margin = 0.55*inch
    col_w = PAGE_W - 2*margin
    y = PAGE_H - HEADER_H - 0.5*inch
    for name, price in FOOD_TRUCK_ITEMS:
        draw_price_row(c, margin, y, name, price, col_w, name_font_size=14)
        y -= 34
    y -= 12
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Oblique", 11)
    c.drawString(margin, y, FOOD_TRUCK_NOTE)
    c.showPage()

def draw_drinks_page(c):
    draw_ref_header(c, "Drinks & Snacks", "2026 Price List")
    margin = 0.55*inch
    col_w = PAGE_W - 2*margin
    y = PAGE_H - HEADER_H - 0.5*inch
    for section_name, items in DRINKS_SNACKS:
        c.setFillColor(LAPIS)
        c.setFont(F_BODYB, 15)
        c.drawString(margin, y, section_name.upper())
        y -= 24
        for name, price in items:
            draw_price_row(c, margin, y, name, price, col_w, name_font_size=12.5)
            y -= 27
        y -= 16
    c.showPage()

def draw_rules_pages(c):
    section_style = ParagraphStyle('Section2', fontName=F_DISPLAY, fontSize=11.5,
                                    textColor=LAPIS, spaceBefore=8, spaceAfter=4, leading=13.5)
    body_style = ParagraphStyle('Body2', fontName=F_BODY, fontSize=8.2,
                                 textColor=INK, leading=10.6, spaceAfter=6, alignment=TA_LEFT)

    flowables = []
    for title, paragraphs in RULES_SECTIONS:
        flowables.append(Paragraph(title, section_style))
        for p in paragraphs:
            flowables.append(Paragraph(p, body_style))

    margin = 0.55 * inch
    col_gap = 0.3 * inch
    n_cols = 2
    col_w = (PAGE_W - 2*margin - (n_cols-1)*col_gap) / n_cols
    top_pad = 20
    bottom_margin = 0.45 * inch
    frame_top = PAGE_H - HEADER_H - top_pad
    col_height = frame_top - bottom_margin

    col_idx = 0
    y = frame_top
    draw_ref_header(c, "Tournament Rules", "2026 BLSA End of Year Tournament")

    for flowable in flowables:
        w, h = flowable.wrap(col_w, col_height)
        if h > col_height:
            h = col_height
        extra = 20 if flowable.style is section_style else 0
        if y - h - extra < bottom_margin:
            col_idx += 1
            y = frame_top
            if col_idx >= n_cols:
                c.showPage()
                col_idx = 0
                draw_ref_header(c, "Tournament Rules (cont'd)", "2026 BLSA End of Year Tournament")
        x = margin + col_idx * (col_w + col_gap)
        flowable.drawOn(c, x, y - h)
        y -= h

    c.showPage()

def build():
    c = canvas.Canvas(os.path.join(os.path.dirname(os.path.abspath(__file__)), "team_cards.pdf"), pagesize=letter)
    for team_code in list(TEAM_NAMES.keys()):
        games = team_games(team_code)
        games_by_day = {d: [g for g in games if g["slot"]["day"] == d] for d in DAY_ORDER}

        draw_header(c, team_code)
        legend_top = PAGE_H - HEADER_H
        draw_legend(c, legend_top)
        y = legend_top - 30 - 10
        entry_h = 62
        gap = 7

        for day in DAY_ORDER:
            day_games = games_by_day[day]
            if not day_games:
                continue
            y = draw_day_divider(c, y, day) - 7
            for g in day_games:
                draw_entry(c, y, entry_h, g, team_code)
                y -= entry_h + gap
            y -= 4

        c.setFillColor(MUTED)
        c.setFont("Helvetica-Oblique", 8.5)
        names_finalized = any(TEAM_NAMES[t] != t for t in TEAM_NAMES)
        if names_finalized:
            c.drawCentredString(PAGE_W/2, 0.34*inch,
                               "Check the live digital schedule for any day-of changes.")
        else:
            c.drawCentredString(PAGE_W/2, 0.44*inch,
                         "Team names are placeholders until standings are finalized the Thursday before the tournament.")
            c.drawCentredString(PAGE_W/2, 0.30*inch,
                               "Check the live digital schedule for any day-of changes.")
        c.showPage()

    draw_food_truck_page(c)
    draw_drinks_page(c)
    draw_rules_pages(c)
    c.save()

if __name__ == "__main__":
    build()
    print("done")
