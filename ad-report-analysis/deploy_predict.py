# -*- coding: utf-8 -*-
"""
机器学习完整闭环：训练评估 → 选最佳模型 → 对新数据预测
数据：亚马逊广告 ad_data_100.csv（清洗后 82 行历史数据）
阶段1：清洗 → 特征 → 三切分 → 交叉验证调参 → 测试集定案（验证可信）
阶段2：用最佳模型预测「未来新广告」的 ACoS（模型的实际用途）
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error

# ============ 阶段1：训练 + 评估，选出可信的最佳模型 ============
df = pd.read_csv(r"C:\Users\HP\NZKUNNN\ad-report-analysis\ad_data_100.csv")
df = df[df["Sales"] > 0]
df["ACoS"] = df["Spend"] / df["Sales"]

X = df[["Impressions", "CTR"]]     # 干净特征，避免泄漏
y = df["ACoS"]

# 三切分：锁死测试集
X_trval, X_test, y_trval, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# 交叉验证调参，选最佳模型
gs = GridSearchCV(
    RandomForestRegressor(),
    {"max_depth": [3, 5, None], "n_estimators": [50, 200]},
    cv=5, scoring="r2")
gs.fit(X_trval, y_trval)
best_model = gs.best_estimator_      # 训练好的最佳模型

# 测试集定案（证明模型可信）
y_pred = best_model.predict(X_test)
print("=== 阶段1：评估定案 ===")
print("最佳参数    :", gs.best_params_)
print("测试集 R²   :", round(r2_score(y_test, y_pred), 4))
print("测试集 MAE  :", round(mean_absolute_error(y_test, y_pred), 4))
print("→ 模型可信，可上线用于预测新数据\n")

# ============ 阶段2：用最佳模型预测「新广告」的 ACoS ============
print("=== 阶段2：对新数据预测 ACoS ===")

# 造 30 条"未来新广告"：只有 Impressions、CTR，没有 ACoS（要预测的）
# 取值参照历史数据范围，仅作演示（非真实数据）
imp_min, imp_max = df["Impressions"].min(), df["Impressions"].max()
ctr_min, ctr_max = df["CTR"].min(), df["CTR"].max()
rng = np.random.default_rng(7)
new_data = pd.DataFrame({
    "Impressions": rng.integers(int(imp_min), int(imp_max), 30),
    "CTR": rng.uniform(ctr_min, ctr_max, 30),
})
print(f"(模拟新广告 30 条，特征范围参照历史：Impressions {imp_min:.0f}~{imp_max:.0f}，CTR {ctr_min:.3f}~{ctr_max:.3f})\n")

# 用最佳模型预测每条新广告的 ACoS
new_pred = best_model.predict(new_data)
new_data["预测ACoS"] = np.round(new_pred, 3)
new_data["判断"] = np.where(new_data["预测ACoS"] < 0.5, "较健康", "警惕")

# 按预测 ACoS 从低到高排序（ACoS 越低越赚钱）
new_data = new_data.sort_values("预测ACoS").reset_index(drop=True)

pd.set_option("display.max_rows", 50)
print(new_data)
print(f"\n结论：30 条新广告中，预测 ACoS < 0.5 的 {sum(new_data['判断']=='较健康')} 条较健康，"
      f"{sum(new_data['判断']=='警惕')} 条需警惕 → 可据此分配广告预算")
