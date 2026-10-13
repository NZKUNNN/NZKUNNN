# -*- coding: utf-8 -*-
"""
机器学习完整评估流程 · 规范版
数据：亚马逊广告 ad_data_100.csv（清洗后 82 行）
流程：清洗 → 干净特征 → 三切分锁死测试集 → 交叉验证调参 → 测试集定案
原则：特征不泄漏 · 调参不碰测试集 · 最终用真实分数说话
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score, mean_absolute_error

# ============ 1. 数据清洗 ============
df = pd.read_csv(r"C:\Users\HP\NZKUNNN\ad-report-analysis\ad_data_100.csv")
df = df[df["Sales"] > 0]                    # 只保留有销量的
df["ACoS"] = df["Spend"] / df["Sales"]      # 目标：ACoS
print(f"清洗后样本：{len(df)} 行")

# ============ 2. 干净特征（避免泄漏） ============
# 只用和目标弱相关的真实可预测特征；不用 Clicks/Spend/Orders（泄漏）
X = df[["Impressions", "CTR"]]
y = df["ACoS"]

# ============ 3. 三切分：先锁死测试集 ============
# 固定 random_state=42 → 可复现
X_trval, X_test, y_trval, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
print(f"训练+验证集：{len(X_trval)} 行，测试集：{len(X_test)} 行\n")

# ============ 4. 交叉验证调参（不碰测试集） ============
# GridSearchCV 内部自动做交叉验证（cv=5），枚举超参数选最优
models = {
    "随机森林": (RandomForestRegressor(), {"max_depth": [3, 5, None], "n_estimators": [50, 200]}),
    "决策树":   (DecisionTreeRegressor(), {"max_depth": [3, 5, 8]}),
}

for name, (model, param_grid) in models.items():
    gs = GridSearchCV(model, param_grid, cv=5, scoring="r2")
    gs.fit(X_trval, y_trval)
    print(f"=== {name} ===")
    print("调参分数 best_score_ :", round(gs.best_score_, 4))
    print("最优参数             :", gs.best_params_)
    # ============ 5. 锁死的测试集上评一次 ============
    y_pred = gs.best_estimator_.predict(X_test)
    print("真实测试 R²          :", round(r2_score(y_test, y_pred), 4))
    print("真实测试 MAE         :", round(mean_absolute_error(y_test, y_pred), 4))
    print()
