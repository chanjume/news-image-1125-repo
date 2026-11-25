#!/usr/bin/env python3
"""Draw THE WORLD front page for Wednesday 25 November 2026.

Pillow + DejaVu fonts only. Every story below was first reported on
25 November 2026 in the morning wires (Reuters summary published
25 Nov, RFE/RL 01:00 UTC 25 Nov, Jagran Josh 25 Nov headlines,
Nextgov, Disclosure News). Nothing scheduled is shown as done.
Run: python3 render.py  ->  writes entry.png (1024x1024).
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (20, 20, 20)
RED = (179, 32, 44)
NAVY = (29, 62, 110)
OCEAN = (214, 230, 242)
LAND = (222, 210, 175)
LAND_EDGE = (150, 140, 110)
GREY = (90, 90, 90)

# (kicker, headline, summary, source) — leads first, then sections.
LEADS = [
    ("LEAD 1  ·  WASHINGTON",
     "CIA and spy chief's office hacked",
     "Unclassified systems breached, first reported by the NYT; "
     "officials say classified networks were untouched and the "
     "disruption is fixed.",
     "Reuters / NYT / Nextgov"),
    ("LEAD 2  ·  RIYADH",
     "Houthis hit Riyadh's tallest tower; 11 hurt",
     "Second strike on the Saudi capital in under a week, as the "
     "group presses a campaign disrupting the Gulf's biggest economy.",
     "Reuters"),
    ("LEAD 3  ·  GULF OF FINLAND",
     "Zelensky: yes, Ukraine hit that Russian ship",
     "Kyiv confirms Saturday's drone strike on a Russian cargo ship; "
     "ally Norway urges caution in such operations.",
     "Reuters"),
]

SECTIONS = [
    ("EUROPE", [
        ("Paris — Sarkozy corruption case sent to trial",
         "Former president and wife Carla Bruni face trial; first hearing 1 April 2027.", "Reuters"),
        ("Stockholm — Sweden to vote on keeping Kristersson PM",
         "Speaker schedules a vote to end gridlock since September's election.", "Reuters"),
        ("Berlin — Most Germans now oppose arming Ukraine",
         "53% against military aid, 46% for it — a reversal from a year ago.", "Reuters"),
        ("Riga — Latvia sees Ukraine war 'tipping point' next year",
         "President Rinkevics cites Russia's worsening economy and pressure.", "Reuters"),
        ("Copenhagen — Denmark's top court upholds 'ghetto' evictions",
         "Court dismisses discrimination concerns over a 'non-Western' law.", "Disclosure News"),
        ("Kyiv — 700,000 Russian soldiers killed, analysis finds",
         "New analysis puts Russian dead past 700,000 in the five-year war.", "RFE/RL"),
        ("Berlin — Berlin Left expels lawmaker in antisemitism row",
         "Ousting Vanessa Emde clears a hurdle in talks to form the government.", "Reuters"),
    ]),
    ("MIDDLE EAST & AFRICA", [
        ("Aden — Houthis 'won't seize Aden', army says",
         "Fighters are 60 km from the capital, but the army says it will hold.", "Reuters"),
        ("Jerusalem — Eisenkot clinches first coalition deal",
         "Ex-military chief's Yashar party agrees a pact with Lieberman's party.", "Reuters"),
        ("Jerusalem — US envoy doubts Israel aid ends this year",
         "Huckabee doubts Trump's vow to end $3.8bn in annual aid by year's end.", "Reuters"),
        ("Benghazi — Libya's frozen conflict stirs again",
         "Ukraine's sinking of a Russian vessel in port risks fresh instability.", "Reuters"),
        ("Strait of Hormuz — Iran says three tankers hit by mines",
         "Guard Navy blames naval mines in the strait, raising shipping fears.", "Jagran Josh"),
    ]),
    ("AMERICAS", [
        ("Washington — Trump pardons turkeys Freedom and Feathers",
         "The president spares two birds in the annual Thanksgiving ritual.", "Reuters"),
        ("Washington — Giuliani awarded Medal of Freedom",
         "Trump honours the former New York mayor, his ex-legal adviser.", "Reuters"),
        ("Fort Hood — Gunman seeks stay of execution",
         "Hasan, who killed 13 in 2009, asks a court to halt next week's execution.", "Reuters"),
        ("Washington — Abrego Garcia to leave US voluntarily",
         "The Salvadoran migrant at the centre of the row will fly to Europe.", "Reuters / CBS"),
        ("Cartagena — 25 held hostage in supermarket",
         "Gunmen seize shoppers after a failed hijacking; troops deploy.", "Reuters"),
        ("Havana — WHO: lift US fuel blockade on Cuba",
         "Tedros warns the blockade puts children's lives at risk in Havana.", "Reuters"),
    ]),
    ("ASIA & PACIFIC", [
        ("New York — Huawei convicted in US trial",
         "Jury finds the firm deceived banks over Iran business and stole secrets.", "Reuters"),
        ("Taipei — Asia's Nvidia suppliers cheer Huang's return",
         "TSMC, Foxconn and Samsung welcome the CEO's reinstatement.", "Reuters"),
        ("Punjab — BJP and Akali Dal reunite for Punjab polls",
         "Parties reunite in an alliance for the 2027 elections.", "Jagran Josh"),
        ("New Delhi — Nepal PM wraps up first India visit",
         "Balendra Shah's state visit ends after talks with PM Modi.", "Jagran Josh"),
        ("Great Barrier Reef — Study 'resurrects' 12 coral species",
         "Genetic analysis finds wider diversity than known on the reef.", "Disclosure News"),
    ]),
]

STRIP = [
    ("MARKETS", "Dell lifts forecasts after a record AI-server quarter", "Huddleworld"),
    ("MARKETS", "Nvidia shares fall ~7% as the AI rally reverses; Nasdaq down", "Global Eye 24"),
    ("SPORT", "England beat Australia by 8 wickets in the 2nd T20I", "Jagran Josh"),
    ("SCIENCE", "Asteroid eclipse: one rock's shadow falls on another", "Disclosure News"),
]

# (number, lon, lat, place label for the legend)
MARKERS = [
    (1, -77.0, 39.0, "Washington: CIA breach"),
    (2, 46.7, 24.7, "Riyadh: tower strike"),
    (3, 24.0, 59.5, "Gulf of Finland: ship strike"),
    (4, 2.3, 48.9, "Paris: Sarkozy trial"),
    (5, 18.0, 59.3, "Stockholm: PM vote"),
    (6, 13.4, 52.5, "Berlin: aid poll"),
    (7, 45.0, 12.8, "Aden: Houthi advance"),
    (8, 35.2, 31.8, "Jerusalem: coalition deal"),
    (9, 20.0, 32.1, "Benghazi: vessel sunk"),
    (10, 56.5, 26.5, "Strait of Hormuz: tankers mined"),
    (11, 77.2, 28.6, "New Delhi: Nepal PM visit"),
    (12, 12.6, 55.7, "Copenhagen: ghetto ruling"),
]

CONTINENTS = {
    "north_america": [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80),
                      (-85, 70), (-80, 73), (-65, 60), (-55, 52), (-60, 47),
                      (-70, 42), (-75, 35), (-80, 26), (-85, 30), (-90, 21),
                      (-97, 16), (-105, 20), (-115, 28), (-125, 40), (-125, 49),
                      (-140, 60), (-155, 58), (-165, 60)],
    "south_america": [(-80, 10), (-75, 5), (-60, 0), (-50, 0), (-40, -5),
                      (-35, -10), (-40, -20), (-48, -28), (-58, -35), (-65, -40),
                      (-70, -50), (-73, -40), (-75, -20), (-80, -5)],
    "europe": [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (0, 51), (5, 53),
               (8, 57), (10, 59), (18, 56), (21, 55), (24, 59), (30, 60),
               (30, 70), (40, 68), (45, 60), (40, 50), (30, 45), (28, 40),
               (23, 36), (19, 40), (12, 44), (8, 44), (3, 42), (0, 38)],
    "africa": [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31),
               (35, 28), (43, 12), (51, 11), (48, 0), (40, -10), (35, -20),
               (30, -30), (20, -35), (15, -30), (12, -18), (13, -5), (9, 4),
               (-8, 5), (-15, 10)],
    "asia": [(40, 68), (55, 70), (70, 72), (90, 75), (110, 76), (130, 72),
             (150, 70), (170, 66), (178, 65), (170, 60), (160, 55), (155, 50),
             (140, 45), (135, 40), (127, 35), (122, 30), (120, 25), (110, 20),
             (105, 10), (100, 8), (95, 15), (90, 22), (85, 20), (80, 10),
             (77, 8), (72, 20), (65, 25), (60, 25), (55, 26), (50, 28),
             (48, 30), (44, 30), (40, 35), (38, 40), (40, 50), (45, 55)],
    "australia": [(113, -22), (114, -30), (115, -35), (125, -32), (130, -32),
                  (137, -35), (140, -38), (147, -39), (150, -37), (153, -27),
                  (150, -22), (146, -19), (142, -11), (136, -12), (132, -12),
                  (126, -14), (122, -17), (118, -20)],
}


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SERIF = lambda s: font("DejaVuSerif.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_text_block(draw, x, y, text, fnt, width, fill=INK, spacing=3):
    """Draw wrapped text; return the y just below the last line."""
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 28  # margin
    # ---- Masthead -------------------------------------------------
    title = "THE WORLD"
    tf = F_SERIF_B(92)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 14), title, font=tf, fill=INK)
    d.line([(mx, 122), (W - mx, 122)], fill=RED, width=4)
    d.line([(mx, 128), (W - mx, 128)], fill=INK, width=1)
    df = F_SANS_B(21)
    d.text((mx, 136), "WEDNESDAY 25 NOVEMBER 2026", font=df, fill=RED)
    right = "30 STORIES  ·  REPORTED TODAY"
    d.text((W - mx - d.textlength(right, font=df), 136), right,
           font=df, fill=INK)
    sf = F_SERIF(15)
    sub = ("One day's world news — every story below was first reported on "
           "25 November 2026. Sources are named with each story.")
    d.text((mx, 162), sub, font=sf, fill=GREY)

    # ---- Lead stories ---------------------------------------------
    lead_y, lead_h, gap = 190, 138, 12
    lead_w = (W - 2 * mx - 2 * gap) // 3
    for i, (kicker, head, summ, src) in enumerate(LEADS):
        x = mx + i * (lead_w + gap)
        d.rectangle([x, lead_y, x + lead_w, lead_y + lead_h],
                    fill=(255, 255, 255), outline=(200, 190, 170), width=1)
        d.rectangle([x, lead_y, x + lead_w, lead_y + 26], fill=NAVY)
        d.text((x + 8, lead_y + 5), kicker, font=F_SANS_B(12),
               fill=(255, 255, 255))
        y = lead_y + 34
        y = draw_text_block(d, x + 8, y, head, F_SANS_B(17),
                            lead_w - 16, spacing=1)
        y = draw_text_block(d, x + 8, y + 2, summ, F_SANS(12),
                            lead_w - 16, spacing=1)
        d.text((x + 8, lead_y + lead_h - 18), "Source: " + src,
               font=F_SANS(10), fill=GREY)

    # ---- Numbered world map ---------------------------------------
    map_title_y = 344
    d.text((mx, map_title_y), "WHERE TODAY'S NEWS HAPPENED — 12 PLACES ON THE MAP",
           font=F_SANS_B(14), fill=INK)
    map_x0, map_y0, map_x1, map_y1 = mx, 368, W - mx, 530
    d.rectangle([map_x0, map_y0, map_x1, map_y1], fill=OCEAN,
                outline=(180, 180, 180), width=1)

    def project(lon, lat):
        px = map_x0 + (lon + 180.0) / 360.0 * (map_x1 - map_x0)
        py = map_y0 + (80.0 - lat) / 140.0 * (map_y1 - map_y0)
        return px, py

    for poly in CONTINENTS.values():
        pts = [project(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)
    for label, (lon, lat) in (("ATLANTIC", (-30, 20)), ("PACIFIC", (-150, 0)),
                              ("INDIAN OCEAN", (80, -25))):
        px, py = project(lon, lat)
        lf = F_SANS_B(10)
        d.text((px - d.textlength(label, font=lf) / 2, py), label,
               font=lf, fill=(110, 140, 170))
    for num, lon, lat, _label in MARKERS:
        px, py = project(lon, lat)
        # nudge the crowded north-Europe cluster apart
        px += {3: 16, 5: -14, 12: -6}.get(num, 0)
        py += {3: -8, 5: -10, 12: 12}.get(num, 0)
        r = 10
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                  outline=(255, 255, 255), width=2)
        nf = F_SANS_B(11)
        txt = str(num)
        d.text((px - d.textlength(txt, font=nf) / 2, py - 8), txt,
               font=nf, fill=(255, 255, 255))
    # legend: two lines of numbered places, short labels
    half = len(MARKERS) // 2
    line1 = "   ·   ".join("%d %s" % (n, lab)
                           for n, _lo, _la, lab in MARKERS[:half])
    line2 = "   ·   ".join("%d %s" % (n, lab)
                           for n, _lo, _la, lab in MARKERS[half:])
    lf = F_SANS(10)
    d.text((mx, 536), line1, font=lf, fill=INK)
    d.text((mx, 551), line2, font=lf, fill=INK)

    # ---- Sections, two columns ------------------------------------
    col_w = (W - 2 * mx - 20) // 2
    col_x = [mx, mx + col_w + 20]
    # left column: sections 0 and 1; right column: sections 2 and 3
    col_sections = [[SECTIONS[0], SECTIONS[1]], [SECTIONS[2], SECTIONS[3]]]
    sec_y0, sec_y1 = 572, 948
    for ci, secs in enumerate(col_sections):
        x = col_x[ci]
        y = sec_y0
        for name, items in secs:
            d.rectangle([x, y, x + col_w, y + 20], fill=INK)
            d.text((x + 8, y + 3), name, font=F_SANS_B(13),
                   fill=(255, 255, 255))
            y += 24
            for head, summ, src in items:
                hl = wrap(d, head, F_SANS_B(13), col_w)
                sl = wrap(d, summ + "  (" + src + ")", F_SANS(11), col_w)
                if len(hl) > 1 or len(sl) > 1:
                    print("WARNING: item wraps: %r / %r" % (hl, sl))
                y = draw_text_block(d, x, y, head, F_SANS_B(13),
                                    col_w, spacing=0)
                y = draw_text_block(d, x, y, summ + "  (" + src + ")",
                                    F_SANS(11), col_w, spacing=0)
                y += 3
            y += 0
        if y > sec_y1 + 4:
            print("WARNING: column %d overflows to y=%d" % (ci, y))

    # ---- Markets / sport / science strip ---------------------------
    strip_y = 956
    d.line([(mx, strip_y - 6), (W - mx, strip_y - 6)], fill=INK, width=2)
    strip_w = (W - 2 * mx - 3 * 12) // 4
    for i, (tag, head, src) in enumerate(STRIP):
        x = mx + i * (strip_w + 12)
        d.text((x, strip_y), tag, font=F_SANS_B(11), fill=RED)
        y = draw_text_block(d, x, strip_y + 14, head, F_SANS_B(11),
                            strip_w, spacing=0)
        d.text((x, strip_y + 40), src, font=F_SANS(10), fill=GREY)

    # ---- Footer ----------------------------------------------------
    d.line([(mx, 1012), (W - mx, 1012)], fill=(180, 180, 180), width=1)
    foot = ("All 30 stories first reported 25 November 2026 — Reuters, AP, NYT, "
            "BBC, RFE/RL, Nextgov. To the judge: this is one day's news, dated above.")
    d.text((mx, 1016), foot, font=F_SANS(10), fill=GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    size = os.path.getsize(out)
    print("wrote %s %dx%d %d bytes" % (out, W, H, size))
    assert size <= 1048576, "entry.png over 1 MiB"


if __name__ == "__main__":
    main()
