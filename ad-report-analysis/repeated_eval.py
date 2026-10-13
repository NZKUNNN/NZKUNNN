# -*- coding: utf-8 -*-
"""
重复评估实验：数据不够时，多跑几次取平均，评估才稳
对比两个模型：
  - 随机森林（深度不限）= 复杂模型，容易过拟合
  - 决策树（max_depth=3）= 简单模型
每个模型都用 50 个不同的随机切点各评一次，收集分数，取平均 + 标准差
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
# ---------- 1. 读数据 + 清洗 + 特征（和之前完全一样） ----------
df = pd.read_csv(r"C:\Users\HP\NZKUNNN\ad-report-analysis\ad_data_100.csv")
df = df[df["Sales"] > 0]                # 去掉销售额为0的行
df["ACoS"] = df["Spend"] / df["Sales"]  # 目标：ACoS
X = df[["Impressions", "CTR"]]          # 干净特征，避免泄漏
y = df["ACoS"]

# ---------- 2. 定义两个模型 ----------
rf   = RandomForestRegressor()                    # 复杂：很多树、深度不限
tree = DecisionTreeRegressor(max_depth=3)         # 简单：限制深度 3
lin  = LinearRegression()
# ---------- 3. 写一个"重复评估"的函数 ----------
def evaluate(model, n=50):
    """换 n 个随机切点各评一次，返回 (平均分, 标准差)"""
    scores = []                                  # 空盒子，装每次的分数
    for seed in range(n):                        # seed 从 0 到 n-1，共 n 次
        X_tr, X_te, y_tr, y_te = train_test_split(
            X, y, test_size=0.2, random_state=seed)  # 每次用不同 seed 切
        model.fit(X_tr, y_tr)                    # 训练
        y_pred = model.predict(X_te)              # 预测测试集
        scores.append(r2_score(y_te, y_pred))     # 记下这次分数
    return np.mean(scores), np.std(scores)        # 返回平均 和 标准差

# ---------- 4. 两个模型都跑一遍，对比 ----------
m1, s1 = evaluate(rf)      # 随机森林
m2, s2 = evaluate(tree)    # 决策树
m3, s3 = evaluate(lin)

print(f"随机森林(复杂): 平均 R² = {m1:.3f}  标准差 = {s1:.3f}")
print(f"决策树(简单)  : 平均 R² = {m2:.3f}  标准差 = {s2:.3f}")
print(f"线性回归(最简)  : 平均 R² = {m3:.3f}  标准差 = {s3:.3f}")
