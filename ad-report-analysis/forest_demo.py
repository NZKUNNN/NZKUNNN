# -*- coding: utf-8 -*-
# 五折交叉验证：用「干净特征」诚实评估线性回归预测 ACoS 的水平
# 说明：只做评估，不做 train_test_split / fit / predict / 系数解读
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score

# 1. 读数据 + 清洗
df = pd.read_csv(r"C:\Users\HP\NZKUNNN\ad-report-analysis\ad_data_100.csv")
df = df[df["Sales"] > 0]                # 去掉销售额为0的行，避免除零
df["ACoS"] = df["Spend"] / df["Sales"]  # 目标：ACoS = 花费 / 销售额

# 2. 特征：只用「干净特征」
#    不要用 Spend / Sales / Orders / Clicks（它们和 ACoS 直接或间接相关，会泄漏、虚高分数）
X = df[["Impressions", "CTR"]]
y = df["ACoS"]

# 3. 五折交叉验证：自动把数据切成5份，每轮4份训练+1份测试，跑5次
scores = cross_val_score(RandomForestRegressor(), X, y, cv=5)

# 4. 结果
print("5 个分数:", [round(s, 3) for s in scores])
print("平均分  :", round(scores.mean(), 3))   # 模型真实水平（越接近1越好）
print("标准差  :", round(scores.std(), 3))    # 波动大小（越小越稳，越大越看运气）
