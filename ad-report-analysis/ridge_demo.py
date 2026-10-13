# -*- coding: utf-8 -*-
# 五折交叉验证：用「干净特征」诚实评估 Ridge / Lasso 预测 ACoS 的水平
# 说明：只做评估，不做 train_test_split / fit / predict / 系数解读
import pandas as pd
from sklearn.linear_model import Ridge, Lasso
from sklearn.model_selection import cross_val_score

# 1. 读数据 + 清洗
df = pd.read_csv(r"C:\Users\HP\NZKUNNN\ad-report-analysis\ad_data_100.csv")
df = df[df["Sales"] > 0]                # 去掉销售额为0的行，避免除零
df["ACoS"] = df["Spend"] / df["Sales"]  # 目标：ACoS = 花费 / 销售额

# 2. 特征：只用「干净特征」
#    不要用 Spend / Sales / Orders / Clicks（它们和 ACoS 直接或间接相关，会泄漏、虚高分数）
X = df[["Impressions", "CTR"]]
y = df["ACoS"]

# 3. 遍历 alpha，对比 Ridge 和 Lasso 的交叉验证平均分
alpha_list = [0.001, 0.01, 0.1, 1, 10]

for name, Model in [("Ridge", Ridge), ("Lasso", Lasso)]:
    print(f"--- {name} ---")
    for alpha in alpha_list:
        model = Model(alpha=alpha)
        scores = cross_val_score(model, X, y, cv=5)
        print(f"alpha = {alpha:<5} 平均分 = {round(scores.mean(), 3)}")
