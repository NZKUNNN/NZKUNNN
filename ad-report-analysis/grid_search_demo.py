# -*- coding: utf-8 -*-
# GridSearchCV：自动搜索随机森林的最优超参数（树的数量 n_estimators / 树的深度 max_depth）
# 思路：机器对 param_grid 里所有组合跑 5 折交叉验证，挑出验证平均分最高的那一组
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV

# 1. 读数据 + 清洗
df = pd.read_csv(r"C:\Users\HP\NZKUNNN\ad-report-analysis\ad_data_100.csv")
df = df[df["Sales"] > 0]                # 去掉销售额为0的行，避免除零
df["ACoS"] = df["Spend"] / df["Sales"]  # 目标：ACoS = 花费 / 销售额

# 2. 特征：只用「干净特征」
#    不要用 Spend / Sales / Orders / Clicks（它们和 ACoS 直接或间接相关，会泄漏、虚高分数）
X = df[["Impressions", "CTR"]]
y = df["ACoS"]

# 3. GridSearchCV：自动搜索最优超参数组合
param_grid = {
    "n_estimators": [50, 100, 200],   # 树的数量：越多越稳（3 个候选）
    "max_depth": [None, 5, 10],       # 树的深度：None=不限制（3 个候选）
}
model = RandomForestRegressor()
gs = GridSearchCV(model, param_grid, cv=5)  # 3×3=9 种组合，全部交叉验证，挑最优
gs.fit(X, y)

print("最优参数:", gs.best_params_)
print("最优交叉验证平均分(R²):", round(gs.best_score_, 4))
