# -*- coding: utf-8 -*-
"""
三切分（训练 / 验证 / 测试）：拿到诚实的模型分数
=================================================
上一课：GridSearchCV 的 best_score_ 是"调参时见过验证数据"的分数，偏高（虚高）。
今天：先把测试集锁死，调参全程不碰它，最后只在测试集上评一次，才是真实水平。

流程：
  1. 数据清洗 + 构建特征
  2. 先把测试集锁死（test_size=0.2）——调参、训练都不能用它
  3. 在剩余数据上 GridSearchCV 调参（内部再分 训练 / 验证）
  4. 用调出的最优模型，在锁死的测试集上评一次 → 真实 R²
"""
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import r2_score

# ---------- 1. 读数据 + 清洗 ----------
df = pd.read_csv(r"C:\Users\HP\NZKUNNN\ad-report-analysis\ad_data_100.csv")
df = df[df["Sales"] > 0]                # 去掉销售额为0的行，避免除零
df["ACoS"] = df["Spend"] / df["Sales"]  # 目标：ACoS = 花费 / 销售额
print("清洗后样本数:", len(df))

# ---------- 2. 特征：只用「干净特征」 ----------
# 不要用 Spend / Sales / Orders / Clicks——它们和 ACoS 直接/间接相关，会泄漏、虚高分数
X = df[["Impressions", "CTR"]]
y = df["ACoS"]

# ---------- 3. 先锁死测试集（三切分第 1 刀） ----------
# 随机切 20% 当测试集，从此刻起调参、训练都不许碰它
X_trainval, X_test, y_trainval, y_test = train_test_split(
    X, y, test_size=0.2, random_state=45)  # random_state 换成别的数，切点就变、分数会跳——证明评估不稳定
print("训练+验证样本:", X_trainval.shape[0], "| 测试样本:", X_test.shape[0])

# ---------- 4. 在剩余数据上调参（内部再分 训练 / 验证） ----------
param_grid = {
    "n_estimators": [50, 100, 200],   # 树的数量：越多越稳
    "max_depth": [None, 5, 10],       # 树的深度：None = 不限制
}
gs = GridSearchCV(RandomForestRegressor(), param_grid, cv=5)  # 3×3=9 种组合，交叉验证挑最优
gs.fit(X_trainval, y_trainval)
print("调参分数 best_score_:", round(gs.best_score_, 4), "(虚高：见过验证数据)")
print("最优参数:", gs.best_params_)

# ---------- 5. 在锁死的测试集上评一次 → 真实水平 ----------
y_pred = gs.best_estimator_.predict(X_test)
print("真实测试 R2:", round(r2_score(y_test, y_pred), 4))
print("提示: 样本太少(约80行)时, 单次测试分数像抽奖——换 random_state 重跑分数会大变, 不代表真实水平")
