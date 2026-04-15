#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate arbest_foods_ad.pdf using ReportLab
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

# ── Font registration ──────────────────────────────────────────────────────────
GOTHIC_PATH  = "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf"
MINCHO_PATH  = "/usr/share/fonts/opentype/ipafont-mincho/ipam.ttf"
pdfmetrics.registerFont(TTFont("IPAGothic",  GOTHIC_PATH))
pdfmetrics.registerFont(TTFont("IPAMincho",  MINCHO_PATH))

# ── Colour helpers ─────────────────────────────────────────────────────────────
GOLD       = (0.77, 0.59, 0.23)
GOLD_LIGHT = (0.91, 0.79, 0.48)
BLACK_BG   = (0.05, 0.05, 0.05)
WHITE      = (0.98, 0.98, 0.97)
OFF_WHITE  = (0.95, 0.94, 0.91)
GRAY       = (0.54, 0.50, 0.44)

def rgb(t):
    return t

def fill(c, colour):
    c.setFillColorRGB(*colour)

def stroke(c, colour):
    c.setStrokeColorRGB(*colour)

def rect_filled(c, x, y, w, h, colour):
    fill(c, colour)
    c.rect(x, y, w, h, stroke=0, fill=1)

def rect_stroked(c, x, y, w, h, colour, line_width=1):
    c.setLineWidth(line_width)
    stroke(c, colour)
    c.rect(x, y, w, h, stroke=1, fill=0)

def hline(c, x, y, w, colour, lw=1):
    c.setLineWidth(lw)
    stroke(c, colour)
    c.line(x, y, x + w, y)

def text(c, x, y, s, font, size, colour):
    fill(c, colour)
    c.setFont(font, size)
    c.drawString(x, y, s)

def text_centered(c, cx, y, s, font, size, colour):
    fill(c, colour)
    c.setFont(font, size)
    c.drawCentredString(cx, y, s)

def text_right(c, rx, y, s, font, size, colour):
    fill(c, colour)
    c.setFont(font, size)
    c.drawRightString(rx, y, s)

# ── Page setup ─────────────────────────────────────────────────────────────────
OUTPUT = "/home/user/JIN-WORK/今日のワーク/arbest_foods_ad.pdf"
PAGE_W, PAGE_H = 595, 842
c = canvas.Canvas(OUTPUT, pagesize=(PAGE_W, PAGE_H))

L_MARGIN = 20
R_MARGIN = 575
CONTENT_W = R_MARGIN - L_MARGIN   # 555

# ══════════════════════════════════════════════════════════════════════════════
# 1. TOP SECTION  (y = 672 … 842, height ≈ 170)
# ══════════════════════════════════════════════════════════════════════════════
TOP_TOP    = PAGE_H          # 842
TOP_BOT    = PAGE_H - 170    # 672
TOP_H      = 170

rect_filled(c, 0, TOP_BOT, PAGE_W, TOP_H, BLACK_BG)

# gold top border line
hline(c, 0, TOP_TOP - 3, PAGE_W, GOLD, lw=3)

# small label
text(c, L_MARGIN, TOP_TOP - 14, "REQUE 2026 — ARBEST FOODS SPECIAL FEATURE",
     "IPAGothic", 7, GOLD)

# company name
text(c, L_MARGIN, TOP_TOP - 28, "アーベストフーズ株式会社", "IPAGothic", 11, WHITE)

# headline line 1
text(c, L_MARGIN, TOP_TOP - 48, "価格ではなく、品質価値で選ばれる設計",
     "IPAMincho", 11, GOLD)

# headline line 2 — split: first part white, "理由のある" in gold-light, rest white
HL2_Y = TOP_TOP - 76
c.setFont("IPAMincho", 26)
PART_A = "売場で差がつく、"
PART_B = "理由のある"
PART_C = "５品"
w_a = c.stringWidth(PART_A, "IPAMincho", 26)
w_b = c.stringWidth(PART_B, "IPAMincho", 26)
fill(c, WHITE);      c.drawString(L_MARGIN,         HL2_Y, PART_A)
fill(c, GOLD_LIGHT); c.drawString(L_MARGIN + w_a,   HL2_Y, PART_B)
fill(c, WHITE);      c.drawString(L_MARGIN + w_a + w_b, HL2_Y, PART_C)

# sub-copy
text(c, L_MARGIN, TOP_TOP - 96,
     "素材・製法・食感に妥協しない和惣菜・具材メーカーが、バイヤーの信頼に応える５アイテムをご提案。",
     "IPAGothic", 8, (0.75, 0.73, 0.70))

# border box tagline
BOX_TXT  = "OEM・PB・業務用 ─ 幅広い製造実績"
BOX_Y    = TOP_TOP - 128
BOX_H    = 16
c.setFont("IPAGothic", 8)
BOX_W    = c.stringWidth(BOX_TXT, "IPAGothic", 8) + 16
rect_stroked(c, L_MARGIN, BOX_Y, BOX_W, BOX_H, GOLD, line_width=0.8)
text(c, L_MARGIN + 8, BOX_Y + 4, BOX_TXT, "IPAGothic", 8, GOLD)

# ══════════════════════════════════════════════════════════════════════════════
# 2. GOLD THICK DIVIDER
# ══════════════════════════════════════════════════════════════════════════════
DIV_Y = TOP_BOT - 4
hline(c, 0, TOP_BOT, PAGE_W, GOLD, lw=4)

# ══════════════════════════════════════════════════════════════════════════════
# 3. DIFF STRIP  (height ≈ 52, just below top section)
# ══════════════════════════════════════════════════════════════════════════════
DIFF_TOP = TOP_BOT
DIFF_H   = 52
DIFF_BOT = DIFF_TOP - DIFF_H   # 620

rect_filled(c, 0, DIFF_BOT, PAGE_W, DIFF_H, OFF_WHITE)
hline(c, 0, DIFF_BOT, PAGE_W, GRAY, lw=1)

DIFF_COLS = [
    ("⚙",  "日本に3台のみ",       "7トン圧力釜を2台保有"),
    ("💧", "那須高原深層水使用",   "水の違いが旨味の違い"),
    ("🏭", "FSSC22000取得工場",    "国際食品安全規格取得"),
    ("🏆", "OEM・PB多数実績",      "業務用〜市販用まで対応"),
]
COL_W = CONTENT_W / 4
for i, (icon, title, desc) in enumerate(DIFF_COLS):
    cx = L_MARGIN + COL_W * i + COL_W / 2
    # circle icon (black bg)
    ICON_R = 10
    ICON_CY = DIFF_BOT + DIFF_H - 14
    fill(c, BLACK_BG)
    c.circle(cx, ICON_CY, ICON_R, stroke=0, fill=1)
    text_centered(c, cx, ICON_CY - 4, icon, "IPAGothic", 8, WHITE)
    # title
    text_centered(c, cx, DIFF_BOT + 22, title, "IPAGothic", 7.5, GOLD)
    # desc
    text_centered(c, cx, DIFF_BOT + 10, desc, "IPAGothic", 6.5, GRAY)

# ══════════════════════════════════════════════════════════════════════════════
# 4. MIDDLE SECTION  ─ 全商品がページ全体を余白なく埋める
# ══════════════════════════════════════════════════════════════════════════════
MID_TOP = DIFF_BOT        # 620
MID_BOT = 170             # KEY POINTS BAND上端（KP_BOT=100 + KP_H=70）
MID_H   = MID_TOP - MID_BOT  # 450

rect_filled(c, 0, MID_BOT, PAGE_W, MID_H, WHITE)

# ── セクションヘッダー ──────────────────────────────────────────────────────
HDR_TOP_PAD = 7
HDR_LABEL_H = 11
HDR_GAP     = 3
HDR_TITLE_H = 13
HDR_BOT_GAP = 5
HDR_TOTAL   = HDR_TOP_PAD + HDR_LABEL_H + HDR_GAP + HDR_TITLE_H + HDR_BOT_GAP  # 39

cur_y = MID_TOP - HDR_TOP_PAD
text_centered(c, PAGE_W/2, cur_y, "FEATURED LINEUP — 今月の注力５品",
              "IPAGothic", 7, GOLD)
cur_y -= (HDR_LABEL_H + HDR_GAP)
text_centered(c, PAGE_W/2, cur_y,
              "どの商品も、\u201c置いた理由\u201dが語れる",
              "IPAMincho", 12, BLACK_BG)
cur_y -= (HDR_TITLE_H + HDR_BOT_GAP)  # cur_y = MID_TOP - HDR_TOTAL

# ── カード高さを動的計算（余白なしでページを埋める） ────────────────────────
CARD_AREA_H  = cur_y - MID_BOT          # カード全体に使える高さ
GAP          = 5                         # カード間ギャップ
# featured 1枚 + grid 2行 = 3段、ギャップは2つ（featured→row1, row1→row2）
FEATURED_H   = int((CARD_AREA_H - 2 * GAP) * 0.44)
GRID_ROW_H   = (CARD_AREA_H - 2 * GAP - FEATURED_H) // 2
GRID_CARD_W  = (CONTENT_W - 6) / 2

# ── フィーチャードカード（極太メンマ、全幅） ────────────────────────────────
CARD_Y = cur_y - FEATURED_H
CARD_X = L_MARGIN
CARD_W = CONTENT_W

rect_filled(c, CARD_X, CARD_Y, CARD_W, FEATURED_H, (0.96, 0.96, 0.95))
rect_stroked(c, CARD_X, CARD_Y, CARD_W, FEATURED_H, (0.85, 0.82, 0.75), line_width=0.5)

F_LEFT_W = int(CARD_W * 0.38)
F_RIGHT_X = CARD_X + F_LEFT_W + 8

# 左ビジュアルエリア（黒）
rect_filled(c, CARD_X, CARD_Y, F_LEFT_W, FEATURED_H, BLACK_BG)
# タイトル・説明を縦中央に配置
VCY = CARD_Y + FEATURED_H / 2
text_centered(c, CARD_X + F_LEFT_W/2, VCY + 20,
              "極太メンマ", "IPAMincho", 18, GOLD)
text_centered(c, CARD_X + F_LEFT_W/2, VCY + 5,
              "300g", "IPAGothic", 9, GOLD_LIGHT)
text_centered(c, CARD_X + F_LEFT_W/2, VCY - 10,
              "─── GOKUFUTO MENMA ───", "IPAGothic", 6.5, (0.55, 0.45, 0.20))
# ゴールドのアクセントライン
hline(c, CARD_X + 14, VCY + 28, F_LEFT_W - 28, GOLD, lw=0.8)
# メイン商品バッジ
BADGE_H = 16
rect_filled(c, CARD_X, CARD_Y + FEATURED_H - BADGE_H, F_LEFT_W, BADGE_H, GOLD)
text_centered(c, CARD_X + F_LEFT_W/2, CARD_Y + FEATURED_H - BADGE_H + 4,
              "★ メイン商品", "IPAGothic", 8, BLACK_BG)

# 右情報エリア
INFO_X = F_RIGHT_X
IY = CARD_Y + FEATURED_H - 12
text(c, INFO_X, IY, "NO.01 — メイン商品", "IPAGothic", 7.5, GOLD)
IY -= 16
text(c, INFO_X, IY, "極太メンマ", "IPAMincho", 18, BLACK_BG)
IY -= 12
text(c, INFO_X, IY, "300g", "IPAGothic", 9, GRAY)
IY -= 14
rect_filled(c, INFO_X, IY - 1, 2, 10, GOLD)
text(c, INFO_X + 6, IY, "なぜこの食感は真似できないのか", "IPAMincho", 10, BLACK_BG)
IY -= 14
text(c, INFO_X, IY,
     "日本にわずか３台の７トン圧力釜を２台保有。芯まで均一に戻しながら", "IPAGothic", 8, (0.35,0.32,0.28))
IY -= 10
text(c, INFO_X, IY,
     "繊維を壊さず、しなやかさとリッチな噛み心地を実現しております。", "IPAGothic", 8, (0.35,0.32,0.28))
IY -= 12
TAGS_F = [("7トン圧力釜", True), ("設備差別化", True), ("たまり醤油", False), ("おつまみ・小鉢", False)]
TX = INFO_X
for tag_txt, bordered in TAGS_F:
    c.setFont("IPAGothic", 7)
    tw = c.stringWidth(tag_txt, "IPAGothic", 7) + 8
    TH = 12
    if bordered:
        rect_stroked(c, TX, IY - 1, tw, TH, GOLD, line_width=0.8)
        text(c, TX + 4, IY + 2, tag_txt, "IPAGothic", 7, GOLD)
    else:
        rect_filled(c, TX, IY - 1, tw, TH, (0.88, 0.86, 0.82))
        text(c, TX + 4, IY + 2, tag_txt, "IPAGothic", 7, GRAY)
    TX += tw + 5

cur_y = CARD_Y - GAP

# ── 2×2 グリッド（残り4商品、高さを均等に埋める） ──────────────────────────
GRID_CARD_H = GRID_ROW_H

GRID_CARDS = [
    # (accent_col, num, name, weight, tagline, tags, has_kinpira_imgs, is_black_menma)
    (
        (0.36, 0.47, 0.18),
        "NO.02", "きんぴらごぼう チルド", "585g",
        "皮付きごぼう／シャキシャキ食感",
        [("那須高原深層水", True), ("高リピート", False)],
        True, False,
    ),
    (
        (0.18, 0.43, 0.29),
        "NO.03", "高菜油炒め", "300g",
        "油炒め製法／香ばしさが違う",
        [("香ばし系", True), ("チャーハン・おにぎり", False)],
        False, False,
    ),
    (
        (0.47, 0.31, 0.18),
        "NO.04", "穂先メンマ", "500g",
        "上品食感／高付加価値メンマ",
        [("桃屋製造実績", True), ("前菜・冷奴", False)],
        False, False,
    ),
    (
        (0.10, 0.10, 0.10),
        "NO.05", "味付けメンマ（黒）", "1200g",
        "見た瞬間に手が伸びる視覚訴求商品",
        [("インパクト", True), ("大容量", True), ("おつまみ", False)],
        False, True,
    ),
]

for idx, card_data in enumerate(GRID_CARDS):
    accent_col, num, name, weight, tagline, tags, has_kinpira, is_black = card_data
    col = idx % 2
    row = idx // 2
    gx = L_MARGIN + col * (GRID_CARD_W + 6)
    gy = cur_y - (row + 1) * (GRID_CARD_H + GAP) + GAP

    # カード背景
    rect_filled(c, gx, gy, GRID_CARD_W, GRID_CARD_H, (0.96, 0.96, 0.95))
    rect_stroked(c, gx, gy, GRID_CARD_W, GRID_CARD_H, (0.85, 0.82, 0.75), line_width=0.5)

    # アクセントバー（左端）
    ACCENT_W = 4
    rect_filled(c, gx, gy, ACCENT_W, GRID_CARD_H, accent_col)

    VIS_X = gx + ACCENT_W

    if has_kinpira:
        # きんぴらごぼう: 上段1枚 + 下段3枚
        VIS_W = int(GRID_CARD_W * 0.48)
        TOP_H = int(GRID_CARD_H * 0.60)
        BOT_H = GRID_CARD_H - TOP_H
        BOT_Y = gy
        TOP_Y = gy + BOT_H
        c.drawImage("/home/user/JIN-WORK/今日のワーク/きんぴら.png",
                    VIS_X, TOP_Y, VIS_W, TOP_H, preserveAspectRatio=False, mask='auto')
        c.setStrokeColorRGB(1, 1, 1); c.setLineWidth(0.7)
        c.line(VIS_X, TOP_Y, VIS_X + VIS_W, TOP_Y)
        for i, img_path in enumerate([
            "/home/user/JIN-WORK/今日のワーク/きんぴらキンパ2.png",
            "/home/user/JIN-WORK/今日のワーク/きんぴらのり弁.png",
            "/home/user/JIN-WORK/今日のワーク/きんぴら肉巻き.png",
        ]):
            sw = VIS_W / 3
            c.drawImage(img_path, VIS_X + i * sw, BOT_Y, sw, BOT_H,
                        preserveAspectRatio=False, mask='auto')
            if i > 0:
                c.setStrokeColorRGB(1,1,1); c.setLineWidth(0.5)
                c.line(VIS_X + i*sw, BOT_Y, VIS_X + i*sw, BOT_Y + BOT_H)
    elif is_black:
        # 黒メンマ: 黒背景 + ゴールドテキスト
        VIS_W = int(GRID_CARD_W * 0.35)
        rect_filled(c, VIS_X, gy, VIS_W, GRID_CARD_H, (0.05, 0.04, 0.04))
        text_centered(c, VIS_X + VIS_W/2, gy + GRID_CARD_H/2 + 4,
                      "味付けメンマ", "IPAMincho", 7.5, GOLD)
        text_centered(c, VIS_X + VIS_W/2, gy + GRID_CARD_H/2 - 5,
                      "（黒）", "IPAMincho", 7.5, GOLD)
        BADGE2_H = 12
        rect_filled(c, VIS_X, gy, VIS_W, BADGE2_H, GOLD)
        text_centered(c, VIS_X + VIS_W/2, gy + 3, "IMPACT", "IPAGothic", 7, BLACK_BG)
    else:
        VIS_W = int(GRID_CARD_W * 0.35)
        rect_filled(c, VIS_X, gy, VIS_W, GRID_CARD_H, (0.12, 0.11, 0.10))
        text_centered(c, VIS_X + VIS_W/2, gy + GRID_CARD_H/2 - 3,
                      name.replace(" チルド",""), "IPAGothic", 6.5, GOLD)

    # 情報エリア
    IX = VIS_X + VIS_W + 5
    IIY = gy + GRID_CARD_H - 10
    text(c, IX, IIY, num, "IPAGothic", 7, GOLD)
    IIY -= 13
    text(c, IX, IIY, name, "IPAMincho", 10, BLACK_BG)
    IIY -= 10
    text(c, IX, IIY, weight, "IPAGothic", 7.5, GRAY)
    IIY -= 11
    rect_filled(c, IX, IIY - 1, 2, 8, GOLD)
    text(c, IX + 5, IIY, tagline, "IPAGothic", 7.5, BLACK_BG)
    IIY -= 13
    TX2 = IX
    for tag_txt, bordered in tags:
        c.setFont("IPAGothic", 6.5)
        tw2 = c.stringWidth(tag_txt, "IPAGothic", 6.5) + 6
        TH2 = 10
        if bordered:
            rect_stroked(c, TX2, IIY - 1, tw2, TH2, GOLD, line_width=0.6)
            text(c, TX2 + 3, IIY + 1, tag_txt, "IPAGothic", 6.5, GOLD)
        else:
            rect_filled(c, TX2, IIY - 1, tw2, TH2, (0.88, 0.86, 0.82))
            text(c, TX2 + 3, IIY + 1, tag_txt, "IPAGothic", 6.5, GRAY)
        TX2 += tw2 + 4
        TX2 += tw2 + 3

# ══════════════════════════════════════════════════════════════════════════════
# 5. KEY POINTS BAND  (height ≈ 75, above bottom section)
# ══════════════════════════════════════════════════════════════════════════════
KP_BOT = 100
KP_H   = 70
KP_TOP = KP_BOT + KP_H   # 170

rect_filled(c, 0, KP_BOT, PAGE_W, KP_H, BLACK_BG)
hline(c, 0, KP_TOP, PAGE_W, GOLD, lw=1)

text_centered(c, PAGE_W/2, KP_TOP - 10,
              "WHY ARBEST — 選ばれる４つの理由",
              "IPAGothic", 7, GOLD)

KP_DATA = [
    ("７トン圧力釜 / 日本に３台",  "2台保有の設備力が / 唯一無二の食感を生む"),
    ("那須高原 / 深層水使用",      "水の違いが味の違い / 後味のまとまりに直結"),
    ("FSSC22000 / 認証取得工場",  "国際食品安全規格 / 品質保証の信頼基盤"),
    ("OEM・PB / 多数実績",        "大手製品の製造実績 / 確かな技術と信頼"),
]
KP_COL_W = CONTENT_W / 4
for i, (title, desc) in enumerate(KP_DATA):
    bx = L_MARGIN + KP_COL_W * i + 2
    by = KP_BOT + 8
    bw = KP_COL_W - 4
    bh = KP_H - 22
    # box with slight gold tint
    fill(c, (0.13, 0.11, 0.06))
    c.rect(bx, by, bw, bh, stroke=0, fill=1)
    rect_stroked(c, bx, by, bw, bh, GOLD, line_width=0.6)
    cx2 = bx + bw/2
    # title lines
    title_parts = title.split(" / ")
    text_centered(c, cx2, by + bh - 11, title_parts[0], "IPAGothic", 7.5, WHITE)
    if len(title_parts) > 1:
        text_centered(c, cx2, by + bh - 21, title_parts[1], "IPAGothic", 7.5, GOLD)
    # desc lines
    desc_parts = desc.split(" / ")
    text_centered(c, cx2, by + 16, desc_parts[0], "IPAGothic", 6.5, GRAY)
    if len(desc_parts) > 1:
        text_centered(c, cx2, by + 7,  desc_parts[1], "IPAGothic", 6.5, GRAY)

# ══════════════════════════════════════════════════════════════════════════════
# 6. BOTTOM SECTION  (height ≈ 100, y = 0 … 100)
# ══════════════════════════════════════════════════════════════════════════════
BOT_BOT = 0
BOT_H   = 100
BOT_TOP = BOT_BOT + BOT_H   # 100

rect_filled(c, 0, BOT_BOT, PAGE_W, BOT_H, OFF_WHITE)
hline(c, 0, BOT_TOP,        PAGE_W, BLACK_BG, lw=3)
hline(c, 0, BOT_BOT,        PAGE_W, GOLD,     lw=3)

LEFT_COL_W  = int(CONTENT_W * 0.55)
RIGHT_COL_X = L_MARGIN + LEFT_COL_W + 12
RIGHT_COL_W = CONTENT_W - LEFT_COL_W - 12

# ── LEFT COLUMN ────────────────────────────────────────────────────────────────
LOGO_X = L_MARGIN
LOGO_Y = BOT_TOP - 40
LOGO_SZ = 32

# logo square
rect_filled(c, LOGO_X, LOGO_Y, LOGO_SZ, LOGO_SZ, BLACK_BG)
text_centered(c, LOGO_X + LOGO_SZ/2, LOGO_Y + 10, "A", "IPAGothic", 16, GOLD)

TXT_X = LOGO_X + LOGO_SZ + 6
text(c, TXT_X, LOGO_Y + LOGO_SZ - 13, "アーベストフーズ株式会社",
     "IPAMincho", 12, BLACK_BG)
text(c, TXT_X, LOGO_Y + LOGO_SZ - 25, "ARBEST FOODS Co., Ltd.", "IPAGothic", 8, GRAY)

# company description with gold left bar
DESC_Y = LOGO_Y - 6
DESC_LINES = [
    "素材・製法・食感にこだわる和惣菜・具材メーカー。",
    "業務用・市販用・PB・OEMまで幅広い製造実績。",
    "『価格訴求』ではなく『満足感・品質価値』で選ばれる設計思想。",
]
rect_filled(c, LOGO_X, DESC_Y - len(DESC_LINES)*9 + 6, 2, len(DESC_LINES)*9, GOLD)
for line in DESC_LINES:
    text(c, LOGO_X + 5, DESC_Y, line, "IPAGothic", 7, GRAY)
    DESC_Y -= 9

# ── RIGHT COLUMN ───────────────────────────────────────────────────────────────
text(c, RIGHT_COL_X, BOT_TOP - 10, "QUALITY & CERTIFICATION", "IPAGothic", 7, GOLD)

CERT_DATA = [
    ("FSSC22000認証取得工場",      "国際食品安全マネジメントシステム"),
    ("国内製造・国産素材採用",     "那須高原深層水使用／自社工場"),
    ("OEM・PB対応可能",            "業務用〜市販用まで柔軟対応"),
]
CY = BOT_TOP - 22
for bold_txt, sub_txt in CERT_DATA:
    # white box
    CERT_W = RIGHT_COL_W
    CERT_H = 18
    rect_filled(c, RIGHT_COL_X, CY - CERT_H + 4, CERT_W, CERT_H, WHITE)
    # black icon square
    ICO_SZ = 12
    rect_filled(c, RIGHT_COL_X + 2, CY - CERT_H + 7, ICO_SZ, ICO_SZ, BLACK_BG)
    # bold text
    text(c, RIGHT_COL_X + ICO_SZ + 6, CY - 2, bold_txt, "IPAGothic", 7.5, BLACK_BG)
    # sub text
    text(c, RIGHT_COL_X + ICO_SZ + 6, CY - 11, sub_txt,  "IPAGothic", 6.5, GRAY)
    CY -= 21

# ── CTA BAR ────────────────────────────────────────────────────────────────────
CTA_H  = 18
CTA_Y  = BOT_BOT + 3
rect_filled(c, L_MARGIN, CTA_Y, CONTENT_W, CTA_H, BLACK_BG)

text(c, L_MARGIN + 6, CTA_Y + 5,
     "お仕入れ・サンプルのご相談はお気軽にお問い合わせください",
     "IPAMincho", 8.5, WHITE)

text_right(c, R_MARGIN - 4, CTA_Y + 11, "CONTACT", "IPAGothic", 7, GOLD)
text_right(c, R_MARGIN - 4, CTA_Y + 3,
           "アーベストフーズ株式会社 営業部", "IPAGothic", 7, WHITE)

# ── Save ───────────────────────────────────────────────────────────────────────
c.save()
print("PDF generated successfully")
print(f"Output: {OUTPUT}")
