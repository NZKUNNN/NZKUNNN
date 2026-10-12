# -*- coding: utf-8 -*-
"""
小红书图文第2篇：模型评估与泛化（交叉验证 / R² / 特征泄漏 / 过拟合）
4 张 3:4 图（1080x1440），延续第一篇深色科技感风格。
素材全部来自今天的真实实验：4 次特征实验的 R²、cv_demo.py 真实代码、5 折交叉验证结果。
"""
import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False

CV_DEMO = r"C:\Users\HP\NZKUNNN\ad-report-analysis\cv_demo.py"
OUT = r"C:\Users\HP\NZKUNNN\xhs_images"
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1440

def font(size, bold=False):
    p = r"C:\Windows\Fonts\msyhbd.ttc" if bold else r"C:\Windows\Fonts\msyh.ttc"
    return ImageFont.truetype(p, size)

def font_mono(size):
    for p in [r"C:\Windows\Fonts\consola.ttf", r"C:\Windows\Fonts\cour.ttf"]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return font(size)

def center_text(draw, y, text, fnt, fill):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, y), text, font=fnt, fill=fill)

def round_box(draw, xy, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def wrap_line(d, line, fnt, max_w):
    if d.textlength(line, font=fnt) <= max_w:
        return [line]
    parts, cur = [], ""
    for ch in line:
        if cur and d.textlength(cur + ch, font=fnt) > max_w:
            parts.append(cur); cur = ch
        else:
            cur += ch
    if cur:
        parts.append(cur)
    return parts

# ===== 真实实验数据（今天亲手跑出） =====
cv_scores = [0.576, 0.403, 0.210, 0.418, 0.540]   # 干净特征 5 折

# ============ 图1 封面 ============
# 白色卡片放柱状图
bar_fig = plt.figure(figsize=(6.8, 3.6), dpi=110)
ax = bar_fig.add_subplot(111)
names = ["干净特征", "+ Clicks", "+ Spend/Sales", "+ 人工除法"]
vals = [0.429, 0.440, 0.522, 1.0]
cols = ["#43a047", "#fb8c00", "#e53935", "#1e88e5"]
bars = ax.bar(names, vals, color=cols, width=0.62)
ax.set_ylim(0, 1.16)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.03, f"{v:.3f}", ha="center",
            fontsize=12, fontweight="bold", color="#263238")
ax.set_facecolor("#ffffff")
bar_fig.patch.set_facecolor("#ffffff")
ax.tick_params(colors="#37474f", labelsize=11)
for s in ax.spines.values():
    s.set_color("#b0bec5")
ax.set_title("同一个模型 · 4 种特征 → 4 个分数（交叉验证 R²）", color="#1a2b4a",
             fontsize=13, fontweight="bold")
ax.annotate("假的！", xy=(3, 1.0), xytext=(2.15, 1.05), color="#e53935",
            fontsize=14, fontweight="bold")
bar_fig.savefig(r"C:\Users\HP\NZKUNNN\xhs_images\_bar_tmp.png", facecolor="#ffffff",
                bbox_inches="tight", pad_inches=0.15)
plt.close(bar_fig)

bar = Image.open(r"C:\Users\HP\NZKUNNN\xhs_images\_bar_tmp.png").convert("RGB")

cover = Image.new("RGB", (W, H), (15, 22, 34))
d = ImageDraw.Draw(cover)
center_text(d, 55, "转行 AI · 真实记录", font(32), (140, 180, 220))

card = (55, 120, 1025, 660)
round_box(d, card, 20, fill=(246, 248, 252), outline=(70, 100, 150), width=2)
ratio = (card[2] - card[0] - 40) / bar.width
bar_h = int(bar.height * ratio)
bar = bar.resize((card[2] - card[0] - 40, bar_h), Image.LANCZOS)
cover.paste(bar, (card[0] + 20, card[1] + (card[3] - card[1] - bar_h) // 2))
round_box(d, (55, 120, 1025, 128), 20, fill=(70, 100, 150))

center_text(d, 760, "模型分数", font(104, True), (255, 255, 255))
center_text(d, 880, "也会骗人！", font(104, True), (255, 150, 80))
center_text(d, 1040, "我把 R² 从 0.43 刷到 1.0，然后发现是假的", font(40), (190, 200, 215))
round_box(d, (160, 1250, 920, 1335), 34, fill=(35, 52, 78))
center_text(d, 1265, "数据驱动 · 动手实践 · 拒绝空谈", font(34), (200, 210, 228))
cover.save(os.path.join(OUT, "05_封面.png"))

# ============ 图2 四次实验详解 ============
fig = plt.figure(figsize=(10.8, 14.4), dpi=100)
gs = fig.add_gridspec(2, 1, height_ratios=[1.0, 1.6], hspace=0.42)
fig.patch.set_facecolor("#f5f7fa")

ax1 = fig.add_subplot(gs[0]); ax1.axis("off")
ax1.set_facecolor("#f5f7fa")
ax1.text(0.5, 0.90, "同一个模型，分数为什么天差地别？", ha="center", va="center",
         fontsize=28, fontweight="bold", color="#1f2933")
rows = [
    ("干净特征", "0.429", "诚实 · 真实水平", "#43a047"),
    ("+ Clicks", "0.440", "间接沾光 · 假", "#fb8c00"),
    ("+ Spend/Sales", "0.522", "直接泄密 · 但线性学不了除法", "#e53935"),
    ("+ 人工除法 Spend÷Sales", "1.0", "答案本体 · 满分但假", "#1e88e5"),
]
y0 = 0.05
for i, (name, score, note, c) in enumerate(rows):
    yy = y0 + i * 0.20
    from matplotlib.patches import FancyBboxPatch
    ax1.add_patch(FancyBboxPatch((0.05, yy), 0.90, 0.17, transform=ax1.transAxes,
                                 facecolor="#ffffff", edgecolor=c, lw=2,
                                 boxstyle="round,pad=0,rounding_size=0.02"))
    ax1.text(0.10, yy + 0.10, name, transform=ax1.transAxes, ha="left", va="center",
             fontsize=17, fontweight="bold", color="#1f2933")
    ax1.text(0.80, yy + 0.10, score, transform=ax1.transAxes, ha="center", va="center",
             fontsize=22, fontweight="bold", color=c)
    ax1.text(0.52, yy + 0.04, note, transform=ax1.transAxes, ha="center", va="center",
             fontsize=12, color="#52606d")

ax2 = fig.add_subplot(gs[1])
ax2.set_facecolor("#f5f7fa")
xpos = [0, 1, 2, 3]
heights = [0.429, 0.440, 0.522, 1.0]
colors = ["#43a047", "#fb8c00", "#e53935", "#1e88e5"]
labels = ["干净\n特征", "+Clicks", "+Spend\nSales", "+人工\n除法"]
b2 = ax2.bar(xpos, heights, color=colors, width=0.6)
ax2.set_ylim(0, 1.15)
for xx, h in zip(xpos, heights):
    ax2.text(xx, h + 0.02, f"{h:.3f}", ha="center", fontsize=17, fontweight="bold", color="#1f2933")
ax2.set_xticks(xpos)
ax2.set_xticklabels(labels, fontsize=14, color="#1f2933")
ax2.tick_params(labelsize=14, colors="#4b5563")
ax2.set_ylabel("交叉验证 R²", fontsize=16, color="#1f2933")
ax2.set_title("你喂的特征，决定了模型是学真规律还是背答案", fontsize=20,
              fontweight="bold", color="#1f2933")
ax2.spines[["top", "right"]].set_visible(False)
ax2.annotate("特征泄漏", xy=(3, 1.0), xytext=(2.4, 0.92), color="#e53935",
             fontsize=15, fontweight="bold")
fig.savefig(os.path.join(OUT, "06_四次实验.png"), facecolor="#f5f7fa")
plt.close(fig)

# ============ 图3 交叉验证真实代码 ============
with open(CV_DEMO, "r", encoding="utf-8") as f:
    raw_lines = [l.rstrip("\n") for l in f.readlines()]
pick_idx = [5, 6, 11, 12, 13, 16, 17, 20, 21, 22, 25, 26]
pick = [(i + 1, raw_lines[i]) for i in pick_idx if i < len(raw_lines)]

img = Image.new("RGB", (W, H), (18, 26, 38))
d = ImageDraw.Draw(img)
center_text(d, 42, "我的真实代码 · 五折交叉验证", font(44, True), (255, 255, 255))
center_text(d, 112, "cv_demo.py", font(26), (120, 150, 190))
y = 200
mono = font_mono(26)
code_fnt = font(28)
GREEN, WHITE, GRAY, BLUE, ORANGE = (106, 190, 135), (230, 235, 245), (100, 120, 145), (120, 170, 230), (240, 160, 90)
for lineno, line in pick:
    fill = WHITE
    s = line.strip()
    if s.startswith("#"):
        fill = GREEN
    elif s.startswith("import") or s.startswith("from"):
        fill = BLUE
    elif s.startswith("print"):
        fill = ORANGE
    d.text((55, y), f"{lineno:>2}", font=mono, fill=GRAY)
    segs = wrap_line(d, line, code_fnt, W - 200)
    for k, seg in enumerate(segs):
        d.text((130, y + k * 46), seg, font=code_fnt, fill=fill)
    y += len(segs) * 46

# 底部结果卡片
round_box(d, (60, y + 20, 1020, y + 210), 22, fill=(35, 52, 78))
d.text((90, y + 45), "真实运行结果：", font=font(30, True), fill=(255, 255, 255))
d.text((90, y + 95), f"5 个分数: {[round(s,3) for s in cv_scores]}", font=font(26), fill=(160, 200, 245))
d.text((90, y + 140), "平均分 0.429 · 标准差 0.129 → 评估更稳，但治不了泄漏", font=font(24), fill=(200, 210, 228))
img.save(os.path.join(OUT, "07_交叉验证代码.png"))

# ============ 图4 过拟合 vs 欠拟合 ============
img = Image.new("RGB", (W, H), (250, 251, 253))
d = ImageDraw.Draw(img)
center_text(d, 55, "过拟合 vs 欠拟合", font(48, True), (28, 34, 46))
center_text(d, 128, "模型分数高，不代表真的会", font(30), (90, 100, 115))

def draw_small(ox, oy, w, h, mode):
    d2 = ImageDraw.Draw(img)
    if mode == "under":
        for (cx, cy) in [(70, 180), (150, 150), (230, 175), (310, 135)]:
            d2.ellipse((ox+cx-5, oy+cy-5, ox+cx+5, oy+cy+5), fill="#37474f")
        d2.line((ox+40, oy+150, ox+w-30, oy+145), fill="#e65100", width=4)
    elif mode == "good":
        for (cx, cy) in [(70, 165), (150, 130), (230, 155), (310, 110)]:
            d2.ellipse((ox+cx-5, oy+cy-5, ox+cx+5, oy+cy+5), fill="#37474f")
        d2.line([(ox+40, oy+165), (ox+130, oy+125), (ox+210, oy+150), (ox+300, oy+105)],
                fill="#2e7d32", width=4)
    else:
        for (cx, cy) in [(70, 160), (120, 200), (170, 140), (220, 185), (270, 130), (320, 170)]:
            d2.ellipse((ox+cx-5, oy+cy-5, ox+cx+5, oy+cy+5), fill="#37474f")
        d2.line([(ox+60, 160+oy), (ox+90, 200+oy), (ox+120, 165+oy), (ox+150, 185+oy),
                 (ox+180, 160+oy), (ox+210, 175+oy), (ox+240, 150+oy), (ox+270, 170+oy),
                 (ox+300, 155+oy)], fill="#b71c1c", width=4)

cards = [("欠拟合", "模型太简单\n规律没学到\n训练·验证都差", "under", "#fff8e1", "#e65100"),
         ("正好", "复杂度刚好\n抓到真实规律\n泛化最好", "good", "#e8f5e9", "#2e7d32"),
         ("过拟合", "背了噪声\n训练高·验证低\n一上场就废", "over", "#ffebee", "#b71c1c")]
xw = 300
for i, (t, desc, mode, bg, tc) in enumerate(cards):
    x0 = 45 + i * (xw + 15)
    round_box(d, (x0, 200, x0 + xw, 950), 20, fill=bg)
    d.text((x0 + 20, 225), t, font=font(34, True), fill=tc)
    draw_small(x0 + 30, 300, 240, 300, mode)
    yy = 660
    for line in desc.split("\n"):
        d.text((x0 + 20, yy), line, font=font(26), fill=(70, 80, 95))
        yy += 44

round_box(d, (60, 1000, 1020, 1220), 22, fill=(28, 34, 46))
d.text((90, 1030), "一句话判断：", font=font(34, True), fill=(255, 255, 255))
d.text((90, 1090), "训练 R² 高、交叉验证低 → 过拟合（背题）", font=font(30), fill=(255, 200, 140))
d.text((90, 1150), "训练验证都低 → 欠拟合（没学到）", font=font(30), fill=(255, 200, 140))
img.save(os.path.join(OUT, "08_过拟合欠拟合.png"))

# 清理临时文件
os.remove(r"C:\Users\HP\NZKUNNN\xhs_images\_bar_tmp.png")
print("已生成 4 张图：", [f for f in sorted(os.listdir(OUT)) if f.startswith(("05","06","07","08"))])
