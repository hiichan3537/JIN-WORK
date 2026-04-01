"""
アーベストフーズ株式会社
イオントップバリュー向け アウトパック弁当 食材提案書 PDF生成スクリプト
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
import math

# フォント登録
pdfmetrics.registerFont(TTFont('IPA', '/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf'))
pdfmetrics.registerFont(TTFont('IPAP', '/usr/share/fonts/opentype/ipafont-gothic/ipagp.ttf'))

# カラーパレット
WHITE     = HexColor('#FFFFFF')
BLACK     = HexColor('#1A1A1A')
GOLD      = HexColor('#B8963E')
DARK_GOLD = HexColor('#8B6914')
DEEP_GREEN= HexColor('#1E4D2B')
LIGHT_GOLD= HexColor('#F5EDD6')
GRAY_LIGHT= HexColor('#F2F2F2')
GRAY_MID  = HexColor('#CCCCCC')
GRAY_DARK = HexColor('#666666')
ACCENT_BG = HexColor('#FAFAF7')

W, H = A4   # 595.27 x 841.89

OUTPUT_PATH = '/home/user/JIN-WORK/アーベストフーズ_トップバリュー提案書.pdf'


def draw_page1(c: canvas.Canvas):
    """1枚目: 会社特徴＋提案コンセプト＋商品一覧"""

    # ── 背景 ──────────────────────────────────
    c.setFillColor(WHITE)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # ── ヘッダーバー ──────────────────────────
    header_h = 68 * mm
    c.setFillColor(DEEP_GREEN)
    c.rect(0, H - header_h, W, header_h, fill=1, stroke=0)

    # ゴールドのアクセントライン
    c.setFillColor(GOLD)
    c.rect(0, H - header_h, W, 2.5, fill=1, stroke=0)
    c.rect(0, H - header_h + header_h - 2.5, W, 2.5, fill=1, stroke=0)

    # 左ゴールドバー
    c.setFillColor(GOLD)
    c.rect(0, H - header_h, 8, header_h, fill=1, stroke=0)

    # タイトルテキスト
    c.setFillColor(LIGHT_GOLD)
    c.setFont('IPA', 9)
    c.drawString(20*mm, H - 14*mm, 'イオントップバリュー株式会社 御中')

    c.setFillColor(WHITE)
    c.setFont('IPA', 22)
    c.drawString(20*mm, H - 27*mm, 'アウトパック弁当向け 食材提案')

    c.setFillColor(GOLD)
    c.setFont('IPA', 12)
    c.drawString(20*mm, H - 37*mm, '売場で差がつく"惣菜力強化"提案')

    # 右側: 会社名
    c.setFillColor(LIGHT_GOLD)
    c.setFont('IPA', 8)
    c.drawRightString(W - 15*mm, H - 20*mm, 'アーベストフーズ株式会社')
    c.setFont('IPA', 7)
    c.drawRightString(W - 15*mm, H - 27*mm, 'Arbest Foods Co., Ltd.')

    # ゴールドの区切り線（ヘッダー下）
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)

    # ── キャッチコピーセクション ──────────────
    catch_y = H - header_h - 22*mm
    c.setFillColor(LIGHT_GOLD)
    c.roundRect(12*mm, catch_y - 10*mm, W - 24*mm, 20*mm, 4, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.8)
    c.roundRect(12*mm, catch_y - 10*mm, W - 24*mm, 20*mm, 4, fill=0, stroke=1)

    c.setFillColor(DEEP_GREEN)
    c.setFont('IPA', 14)
    c.drawCentredString(W/2, catch_y + 3*mm, '"もう一品"で売上が変わる。　ご飯が進む、差別化惣菜。')
    c.setFont('IPA', 8)
    c.setFillColor(DARK_GOLD)
    c.drawCentredString(W/2, catch_y - 5*mm, '─── 開封即使用・安定供給・高付加価値 ───')

    # ── 2カラムセクション: 会社の強み & なぜこの提案か ──
    col_y = catch_y - 16*mm
    col_h = 52*mm
    col1_x = 12*mm
    col2_x = W/2 + 4*mm
    col_w = W/2 - 18*mm

    def draw_section_box(cx, cy, cw, ch, title, title_color=WHITE, bg=DEEP_GREEN):
        # ヘッダー
        c.setFillColor(bg)
        c.roundRect(cx, cy - ch, cw, ch, 4, fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.roundRect(cx, cy - 10*mm, cw, 10*mm, 4, fill=1, stroke=0)
        # 下側の角を消すため上部のみ丸く見せる
        c.setFillColor(GOLD)
        c.rect(cx, cy - 14*mm, cw, 6*mm, fill=1, stroke=0)
        c.setFillColor(title_color)
        c.setFont('IPA', 10)
        c.drawCentredString(cx + cw/2, cy - 7*mm, title)

    # 左: 会社の強み
    draw_section_box(col1_x, col_y, col_w, col_h, '■ アーベストフーズの強み')
    strengths = [
        ('国内製造', '栃木県の自社工場'),
        ('FSSC22000', '国際認証取得工場'),
        ('桃屋ブランド', '製造実績あり'),
        ('那須高原深層水', '3000年前の天然水使用'),
        ('高付加価値', '味・食感にこだわり'),
        ('安定供給', '業務用・カスタマイズ対応'),
    ]
    item_y = col_y - 16*mm
    for i, (bold, desc) in enumerate(strengths):
        iy = item_y - i * 5.8*mm
        c.setFillColor(GOLD)
        c.circle(col1_x + 6*mm, iy + 1.5*mm, 1.5, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont('IPA', 8)
        c.drawString(col1_x + 10*mm, iy, f'{bold}  ')
        c.setFillColor(GRAY_LIGHT)
        c.setFont('IPA', 7.5)
        c.drawString(col1_x + 10*mm + c.stringWidth(bold, 'IPA', 8) + 2*mm, iy, desc)

    # 右: なぜこの提案か
    draw_section_box(col2_x, col_y, col_w, col_h, '■ なぜこの提案か')
    reasons = [
        ('満足度UP', '弁当の"あと一品"で完成度向上'),
        ('原価最適化', '原価を抑えつつ価値を上げる'),
        ('差別化', '食感・味の強さで競合と差別化'),
        ('作業効率', '開封即使用・オペ簡略化'),
    ]
    item_y2 = col_y - 16*mm
    for i, (bold, desc) in enumerate(reasons):
        iy = item_y2 - i * 7.5*mm
        # アイコン風四角
        c.setFillColor(GOLD)
        c.roundRect(col2_x + 4*mm, iy - 0.5*mm, 14*mm, 5*mm, 2, fill=1, stroke=0)
        c.setFillColor(DEEP_GREEN)
        c.setFont('IPA', 7)
        c.drawCentredString(col2_x + 11*mm, iy + 0.8*mm, bold)
        c.setFillColor(WHITE)
        c.setFont('IPA', 8)
        c.drawString(col2_x + 22*mm, iy, desc)

    # ── 商品一覧セクション ──────────────────
    prod_section_y = col_y - col_h - 8*mm
    # セクションヘッダー
    c.setFillColor(DEEP_GREEN)
    c.rect(12*mm, prod_section_y - 8*mm, W - 24*mm, 8*mm, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(12*mm, prod_section_y - 8*mm, 3*mm, 8*mm, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('IPA', 10)
    c.drawString(20*mm, prod_section_y - 5.5*mm, '提案商品ラインナップ　─　全6品')

    # 商品カード (3列 x 2行)
    products = [
        ('①', '極太メンマ', 'たまり醤油', 'しなやかでリッチな\n噛み心地、ごちそう感'),
        ('②', '味付メンマ', '黒色', '真っ黒のインパクト\nクセになる旨さ'),
        ('③', 'フレッシュ\nグリーンザーサイ', '', '爽やかな食感\n箸休めの新定番'),
        ('④', '高菜油いため', '', 'ご飯が止まらない\n王道惣菜'),
        ('⑤', '味付ザーサイ', '細きり', '使いやすさ抜群\n万能食材'),
        ('⑥', 'メンマ\nダイスカット', '', '混ぜるだけで\n"売れる具材"'),
    ]

    card_w = (W - 24*mm - 8*mm) / 3
    card_h = 28*mm
    card_start_y = prod_section_y - 12*mm

    for idx, (num, name, sub, catch) in enumerate(products):
        row = idx // 3
        col = idx % 3
        cx = 12*mm + col * (card_w + 4*mm)
        cy = card_start_y - row * (card_h + 4*mm)

        # カード背景
        c.setFillColor(ACCENT_BG)
        c.roundRect(cx, cy - card_h, card_w, card_h, 3, fill=1, stroke=0)
        c.setStrokeColor(GOLD)
        c.setLineWidth(0.6)
        c.roundRect(cx, cy - card_h, card_w, card_h, 3, fill=0, stroke=1)

        # 番号バッジ
        c.setFillColor(DEEP_GREEN)
        c.circle(cx + 6*mm, cy - 5*mm, 4*mm, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont('IPA', 8)
        c.drawCentredString(cx + 6*mm, cy - 6.5*mm, num)

        # 商品名
        c.setFillColor(BLACK)
        c.setFont('IPA', 9)
        name_lines = name.split('\n')
        for li, ln in enumerate(name_lines):
            c.drawString(cx + 13*mm, cy - 5*mm - li*4.5*mm, ln)

        if sub:
            c.setFillColor(GOLD)
            c.setFont('IPA', 7)
            offset = len(name_lines) * 4.5*mm
            c.drawString(cx + 13*mm, cy - 5*mm - offset, f'（{sub}）')

        # 区切り線
        c.setStrokeColor(GOLD)
        c.setLineWidth(0.4)
        c.line(cx + 3*mm, cy - 14*mm, cx + card_w - 3*mm, cy - 14*mm)

        # キャッチコピー
        c.setFillColor(DARK_GOLD)
        c.setFont('IPA', 7.5)
        catch_lines = catch.split('\n')
        for li, ln in enumerate(catch_lines):
            c.drawCentredString(cx + card_w/2, cy - 17*mm - li*4*mm, ln)

    # ── フッター ──────────────────────────────
    footer_y = 8*mm
    c.setFillColor(DEEP_GREEN)
    c.rect(0, 0, W, footer_y + 2*mm, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, footer_y + 2*mm, W, 1, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('IPA', 7)
    c.drawString(12*mm, footer_y - 2*mm, 'アーベストフーズ株式会社　│　〒那須高原　│　FSSC22000認証取得')
    c.setFont('IPA', 7)
    c.drawRightString(W - 12*mm, footer_y - 2*mm, '1 / 2')


def draw_page2(c: canvas.Canvas):
    """2枚目: 各商品の詳細"""

    # 背景
    c.setFillColor(WHITE)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # ヘッダー（薄め）
    hdr_h = 22*mm
    c.setFillColor(DEEP_GREEN)
    c.rect(0, H - hdr_h, W, hdr_h, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, H - hdr_h, W, 2, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, H - hdr_h, 6, hdr_h, fill=1, stroke=0)

    c.setFillColor(WHITE)
    c.setFont('IPA', 14)
    c.drawString(16*mm, H - 10*mm, '商品詳細　─　各商品の特長・用途・強み')
    c.setFillColor(LIGHT_GOLD)
    c.setFont('IPA', 8)
    c.drawRightString(W - 12*mm, H - 10*mm, 'アーベストフーズ株式会社')
    c.setFillColor(GOLD)
    c.setFont('IPA', 8)
    c.drawRightString(W - 12*mm, H - 17*mm, 'Arbest Foods Co., Ltd.')

    # 商品詳細データ
    products_detail = [
        {
            'num': '①',
            'name': '極太メンマ（たまり醤油）',
            'catch': 'しなやかでリッチな噛み心地、ごちそう感',
            'uses': ['ラーメン', '弁当トッピング', '単品惣菜'],
            'merits': [
                '圧倒的な存在感と視覚的インパクト',
                '食感で競合商品と明確に差別化',
                '高単価弁当・プレミアムラインに最適',
            ],
            'color': HexColor('#3D6B45'),
        },
        {
            'num': '②',
            'name': '味付メンマ　黒色',
            'catch': '真っ黒のインパクト、クセになる旨さ',
            'uses': ['ラーメン', '焼きそば', '弁当'],
            'merits': [
                '見た目のインパクトで購買意欲を刺激',
                '濃厚な味付けで満足度・リピート率UP',
                'SNS映え・話題性で集客効果',
            ],
            'color': HexColor('#2C2C2C'),
        },
        {
            'num': '③',
            'name': 'フレッシュグリーンザーサイ',
            'catch': '爽やかな食感、箸休めの新定番',
            'uses': ['弁当', 'サラダ', '冷菜'],
            'merits': [
                '鮮やかな緑色で弁当の彩りUP',
                '油っぽさをリセットする爽快感',
                'ヘルシー・フレッシュなイメージ訴求',
            ],
            'color': HexColor('#2D7A4F'),
        },
        {
            'num': '④',
            'name': '高菜油いため',
            'catch': 'ご飯が止まらない王道惣菜',
            'uses': ['弁当', 'おにぎり', 'トッピング'],
            'merits': [
                '安定した幅広い世代への人気',
                '高回転率で売場効率UP',
                'ご飯との相性抜群・リピート率◎',
            ],
            'color': HexColor('#7B9E3C'),
        },
        {
            'num': '⑤',
            'name': '味付ザーサイ　細きり',
            'catch': '使いやすさ抜群、万能食材',
            'uses': ['混ぜご飯', '炒め物', '弁当'],
            'merits': [
                '細切りで作業性・計量性が格段にUP',
                'アレンジの幅が広く多用途に活用可能',
                '均一なカットで仕上がりが綺麗',
            ],
            'color': HexColor('#B8963E'),
        },
        {
            'num': '⑥',
            'name': 'メンマ　ダイスカット',
            'catch': '混ぜるだけで"売れる具材"',
            'uses': ['炒飯', '丼', '惣菜'],
            'merits': [
                '歩留まり向上・食材ロス削減',
                'ダイスカットで均一品質を実現',
                '炒飯・丼・惣菜まで幅広く対応',
            ],
            'color': HexColor('#8B6914'),
        },
    ]

    # カードレイアウト: 3行2列
    card_w = (W - 24*mm - 6*mm) / 2
    card_h = 48*mm
    start_y = H - hdr_h - 8*mm
    gap_x = 6*mm
    gap_y = 4*mm

    for idx, p in enumerate(products_detail):
        row = idx // 2
        col = idx % 2
        cx = 12*mm + col * (card_w + gap_x)
        cy = start_y - row * (card_h + gap_y)

        pc = p['color']

        # カード背景
        c.setFillColor(ACCENT_BG)
        c.roundRect(cx, cy - card_h, card_w, card_h, 4, fill=1, stroke=0)

        # 左カラーバー
        c.setFillColor(pc)
        c.roundRect(cx, cy - card_h, 5*mm, card_h, 4, fill=1, stroke=0)
        c.setFillColor(pc)
        c.rect(cx + 2.5*mm, cy - card_h, 2.5*mm, card_h, fill=1, stroke=0)

        # カード枠線
        c.setStrokeColor(GRAY_MID)
        c.setLineWidth(0.5)
        c.roundRect(cx, cy - card_h, card_w, card_h, 4, fill=0, stroke=1)

        # 番号バッジ
        c.setFillColor(pc)
        c.roundRect(cx + 7*mm, cy - 7*mm, 8*mm, 6*mm, 2, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont('IPA', 8)
        c.drawCentredString(cx + 11*mm, cy - 5.2*mm, p['num'])

        # 商品名
        c.setFillColor(BLACK)
        c.setFont('IPA', 10)
        c.drawString(cx + 18*mm, cy - 5.5*mm, p['name'])

        # キャッチコピー
        c.setFillColor(pc)
        c.setFont('IPA', 8)
        c.drawString(cx + 7*mm, cy - 12*mm, p['catch'])

        # 区切り線
        c.setStrokeColor(GRAY_MID)
        c.setLineWidth(0.4)
        c.line(cx + 7*mm, cy - 14*mm, cx + card_w - 4*mm, cy - 14*mm)

        # 用途ラベル
        c.setFillColor(DEEP_GREEN)
        c.setFont('IPA', 7)
        c.drawString(cx + 7*mm, cy - 18*mm, '用途:')
        tag_x = cx + 17*mm
        for use in p['uses']:
            tag_w = c.stringWidth(use, 'IPA', 7) + 4*mm
            c.setFillColor(LIGHT_GOLD)
            c.roundRect(tag_x, cy - 19.5*mm, tag_w, 4.5*mm, 1.5, fill=1, stroke=0)
            c.setStrokeColor(GOLD)
            c.setLineWidth(0.4)
            c.roundRect(tag_x, cy - 19.5*mm, tag_w, 4.5*mm, 1.5, fill=0, stroke=1)
            c.setFillColor(DARK_GOLD)
            c.setFont('IPA', 7)
            c.drawString(tag_x + 2*mm, cy - 18.5*mm, use)
            tag_x += tag_w + 2*mm

        # 強み
        c.setFillColor(DEEP_GREEN)
        c.setFont('IPA', 7)
        c.drawString(cx + 7*mm, cy - 25*mm, '強み:')
        for mi, merit in enumerate(p['merits']):
            my = cy - 29*mm - mi * 5.5*mm
            c.setFillColor(pc)
            c.circle(cx + 10*mm, my + 1.5*mm, 1.5, fill=1, stroke=0)
            c.setFillColor(BLACK)
            c.setFont('IPA', 7.5)
            c.drawString(cx + 13*mm, my, merit)

    # ── 導入メリットバナー ──────────────────
    banner_y = 28*mm
    banner_h = 18*mm
    c.setFillColor(DEEP_GREEN)
    c.roundRect(12*mm, banner_y - banner_h, W - 24*mm, banner_h, 4, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.roundRect(12*mm, banner_y - banner_h, W - 24*mm, banner_h, 4, fill=0, stroke=1)
    c.setLineWidth(1.2)

    # タイトル
    c.setFillColor(GOLD)
    c.setFont('IPA', 9)
    c.drawString(18*mm, banner_y - 6*mm, '導入によるメリット')

    benefits = [
        '売価UP可能',
        '明確な差別化',
        'オペレーション簡略化',
        'リピート率向上',
    ]
    bx = 55*mm
    for b in benefits:
        bw = c.stringWidth(b, 'IPA', 8) + 8*mm
        c.setFillColor(GOLD)
        c.roundRect(bx, banner_y - 8*mm, bw, 5*mm, 2, fill=1, stroke=0)
        c.setFillColor(DEEP_GREEN)
        c.setFont('IPA', 8)
        c.drawCentredString(bx + bw/2, banner_y - 6*mm, b)
        bx += bw + 3*mm

    c.setFillColor(WHITE)
    c.setFont('IPA', 8)
    c.drawString(18*mm, banner_y - 14*mm, 'ご相談・サンプル対応可能です。お気軽にお問い合わせください。')

    # フッター
    footer_y = 8*mm
    c.setFillColor(DEEP_GREEN)
    c.rect(0, 0, W, footer_y + 2*mm, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, footer_y + 2*mm, W, 1, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('IPA', 7)
    c.drawString(12*mm, footer_y - 2*mm, 'アーベストフーズ株式会社　│　〒那須高原　│　FSSC22000認証取得')
    c.drawRightString(W - 12*mm, footer_y - 2*mm, '2 / 2')


def main():
    c = canvas.Canvas(OUTPUT_PATH, pagesize=A4)
    c.setTitle('アーベストフーズ_トップバリュー提案書')
    c.setAuthor('アーベストフーズ株式会社')
    c.setSubject('アウトパック弁当向け食材提案書')

    # 1枚目
    draw_page1(c)
    c.showPage()

    # 2枚目
    draw_page2(c)
    c.showPage()

    c.save()
    print(f'PDF生成完了: {OUTPUT_PATH}')


if __name__ == '__main__':
    main()
