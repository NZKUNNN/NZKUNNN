# -*- coding: utf-8 -*-
"""
小红书图文第3篇：决策树 vs 随机森林（一行代码切换三个模型）
4 张 3:4 图（1080x1440），延续账号深色科技感风格。
数据全部来自今天的真实实验：线性回归0.429 / 决策树0.586 / 随机森林0.642（交叉验证R²）。
"""
import os
from PIL import Image, ImageDraw, ImageFont
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False

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

# ===== 真实数据 =====
MODELS = [
    ("线性回归", 0.429, 0.129, "只会画直线\n简单·稳·学不了非线性", "#64b5f6", "稳"),
    ("决策树", 0.586, 0.195, "切块学非线性\n但单棵飘·易过拟合", "#42a5f5", "飘"),
    ("随机森林", 0.642, 0.163, "一群树投票\n又准又稳·治过拟合", "#1e88e5", "稳"),
]

# ============ 图1 封面 ============
fig = plt.figure(figsize=(7.0, 3.4), dpi=110)
ax = fig.add_subplot(111)
names = ["线性回归", "决策树", "随机森林"]
vals = [0.429, 0.586, 0.642]
cols = ["#64b5f6", "#42a5f5", "#1e88e5"]
bars = ax.bar(names, vals, color=cols, width=0.55)
ax.set_ylim(0, 0.75)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.015, f"{v:.3f}", ha="center",
            fontsize=13, fontweight="bold", color="#263238")
ax.set_facecolor("#ffffff")
fig.patch.set_facecolor("#ffffff")
ax.tick_params(colors="#37474f", labelsize=12)
for s in ax.spines.values():
    s.set_color("#b0bec5")
ax.set_title("只改一行代码 → 分数从 0.43 涨到 0.64", color="#1a2b4a", fontsize=13, fontweight="bold")
ax.set_ylabel("交叉验证 R²", color="#37474f", fontsize=10)
fig.savefig(r"C:\Users\HP\NZKUNNN\xhs_images\_bar3_tmp.png", facecolor="#ffffff",
            bbox_inches="tight", pad_inches=0.15)
plt.close(fig)

bar = Image.open(r"C:\Users\HP\NZKUNNN\xhs_images\_bar3_tmp.png").convert("RGB")

cover = Image.new("RGB", (W, H), (15, 22, 34))
d = ImageDraw.Draw(cover)
center_text(d, 55, "转行 AI · 真实记录", font(32), (140, 180, 220))

card = (55, 120, 1025, 600)
round_box(d, card, 20, fill=(246, 248, 252), outline=(70, 100, 150), width=2)
ratio = (card[2] - card[0] - 40) / bar.width
bar_h = int(bar.height * ratio)
bar = bar.resize((card[2] - card[0] - 40, bar_h), Image.LANCZOS)
cover.paste(bar, (card[0] + 20, card[1] + (card[3] - card[1] - bar_h) // 2))
round_box(d, (55, 120, 1025, 128), 20, fill=(70, 100, 150))

center_text(d, 700, "只改一行代码", font(100, True), (255, 255, 255))
center_text(d, 820, "模型分数从 0.43 涨到 0.64", font(58, True), (255, 150, 80))
center_text(d, 960, "零基础学机器学习 · 决策树 vs 随机森林", font(38), (190, 200, 215))
round_box(d, (160, 1250, 920, 1335), 34, fill=(35, 52, 78))
center_text(d, 1265, "数据驱动 · 动手实践 · 拒绝空谈", font(34), (200, 210, 228))
cover.save(os.path.join(OUT, "09_封面.png"))

# ============ 图2 三模型详解 ============
img = Image.new("RGB", (W, H), (250, 251, 253))
d = ImageDraw.Draw(img)
center_text(d, 55, "三个模型，一页看懂", font(48, True), (28, 34, 46))
center_text(d, 128, "它们都靠 fit 训练、predict 预测，但原理完全不同", font(30), (90, 100, 115))

card_colors = ["#e3f2fd", "#fff3e0", "#e8f5e9"]
y = 200
for i, (name, score, std, desc, c, stab) in enumerate(MODELS):
    round_box(d, (60, y, 1020, y + 330), 20, fill=card_colors[i], outline=c, width=2)
    d.text((90, y + 25), name, font=font(40, True), fill=(28, 34, 46))
    d.text((90, y + 90), f"交叉验证 R² = {score:.3f}", font=font(36, True), fill="#1a2b4a")
    yy = y + 150
    for line in desc.split("\n"):
        d.text((90, yy), line, font=font(28), fill=(70, 80, 95))
        yy += 44
    d.text((90, yy), f"标准差 {std:.3f} · {stab}", font=font(26),
           fill=(47, 111, 178))
    y += 355

round_box(d, (60, 1280, 1020, 1380), 18, fill=(232, 240, 250))
d.text((90, 1300), "结论：随机森林 = 又能学非线性 + 又稳，成为主流默认", font=font(28, True), fill=(47, 111, 178))
img.save(os.path.join(OUT, "10_三模型详解.png"))

# ============ 图3 真实代码 ============
img = Image.new("RGB", (W, H), (18, 26, 38))
d = ImageDraw.Draw(img)
center_text(d, 42, "所谓「换模型」，其实只是换这一行", font(44, True), (255, 255, 255))
center_text(d, 112, "tree_demo.py / forest_demo.py", font(26), (120, 150, 190))

code_lines = [
    ("from sklearn.tree import DecisionTreeRegressor", "import"),
    ("from sklearn.ensemble import RandomForestRegressor", "import"),
    ("", ""),
    ("# 你只需要换这一行：", "comment"),
    ("model = LinearRegression()            # 一条直线", "code"),
    ("model = DecisionTreeRegressor()       # 一棵树：切块学非线性", "code"),
    ("model = RandomForestRegressor()       # 一群树：投票更稳", "code"),
    ("", ""),
    ("model.fit(X_train, y_train)", "code"),
    ("y_pred = model.predict(X_test)", "code"),
]
GREEN, WHITE, GRAY, BLUE, ORANGE = (106, 190, 135), (230, 235, 245), (100, 120, 145), (120, 170, 230), (240, 160, 90)
y = 200
code_fnt = font(28)
mono = font_mono(26)
for lineno, (line, kind) in enumerate(code_lines, start=1):
    if not line:
        y += 30
        continue
    fill = WHITE
    if kind == "import":
        fill = BLUE
    elif kind == "comment":
        fill = GREEN
    d.text((55, y), f"{lineno:>2}", font=mono, fill=GRAY)
    d.text((130, y), line, font=code_fnt, fill=fill)
    y += 52

# 结果卡片
round_box(d, (60, y + 10, 1020, y + 260), 22, fill=(35, 52, 78))
d.text((90, y + 40), "真实运行结果（交叉验证平均分）：", font=font(30, True), fill=(255, 255, 255))
d.text((90, y + 100), "线性回归 0.429  →  决策树 0.586  →  随机森林 0.642", font=font(32, True), fill=(160, 200, 245))
d.text((90, y + 160), "只改一行，分数涨了 0.21 —— 但原理完全不同", font=font(26), fill=(200, 210, 228))
img.save(os.path.join(OUT, "11_真实代码.png"))

# ============ 图4 为什么随机森林更强 ============
img = Image.new("RGB", (W, H), (250, 251, 253))
d = ImageDraw.Draw(img)
center_text(d, 55, "为什么随机森林更稳、更准？", font(46, True), (28, 34, 46))

# 卡片1：能学非线性
round_box(d, (60, 170, 1020, 470), 20, fill="#e8f5e9", outline="#2e7d32", width=2)
d.text((90, 200), "① 能学非线性（跟微积分一个思想）", font=font(32, True), fill="#2e7d32")
d.text((90, 265), "它把画面切成很多小块去逼近弯曲的关系", font=font(28), fill=(60, 70, 85))
d.text((90, 315), "（就像用无数小矩形逼近曲线）", font=font(26), fill=(90, 100, 115))
d.text((90, 380), "→ 线性回归只会画直线，所以学不了除法/曲线", font=font(28), fill=(60, 70, 85))

# 卡片2：多树投票
round_box(d, (60, 520, 1020, 820), 20, fill="#fff3e0", outline="#e65100", width=2)
d.text((90, 550), "② 一群树投票，治过拟合", font=font(32, True), fill="#e65100")
d.text((90, 615), "单棵树切太细、容易背噪声（飘：标准差0.195）", font=font(28), fill=(60, 70, 85))
d.text((90, 670), "随机森林：每棵看不同的数据+特征，各自犯错", font=font(28), fill=(60, 70, 85))
d.text((90, 725), "一投票平均，偏颇互相抵消 → 标准差降到 0.163", font=font(28), fill=(60, 70, 85))

# 卡片3：点菜vs后厨
round_box(d, (60, 870, 1020, 1170), 20, fill="#e3f2fd", outline="#1e88e5", width=2)
d.text((90, 900), "③ 但别只会「点菜」", font=font(32, True), fill="#1e88e5")
d.text((90, 965), "换一行 = 点菜；懂原理 = 懂后厨", font=font(28), fill=(60, 70, 85))
d.text((90, 1020), "真实项目卡你的是：数据、调参、诊断", font=font(28), fill=(60, 70, 85))
d.text((90, 1075), "这些才是一个 AI 从业者的核心能力", font=font(28), fill=(60, 70, 85))

round_box(d, (60, 1220, 1020, 1340), 18, fill=(28, 34, 46))
d.text((90, 1250), "总结：会换模型是起点，懂原理才能解决问题", font=font(30, True), fill=(255, 255, 255))
img.save(os.path.join(OUT, "12_为什么随机森林强.png"))

os.remove(r"C:\Users\HP\NZKUNNN\xhs_images\_bar3_tmp.png")
print("已生成 4 张图：", [f for f in sorted(os.listdir(OUT)) if f.startswith(("09","10","11","12"))])
