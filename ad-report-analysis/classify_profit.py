# -*- coding: utf-8 -*-
# 分类：逻辑回归预测广告是否盈利（ACoS<0.5 记为盈利=1）
# 流程：读数据 -> 清洗 -> 算 ACoS -> 打盈利标签 -> 拆训练/测试 -> 训练 -> 预测 -> 用准确率评估
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

df = pd.read_csv(r"C:\Users\HP\NZKUNNN\ad-report-analysis\ad_data_100.csv")
df = df[df["Sales"] > 0]                            # 清洗：去掉销售额为0的行
df["ACoS"] = df["Spend"] / df["Sales"]              # ACoS = 花费 / 销售额
df["is_profit"] = (df["ACoS"] < 0.5).astype(int)    # 盈利标签：ACoS<0.5 → 1（盈利），否则 0

# 特征：只用预测时已知的投入信息（曝光、点击率）。
# 注意：不能用 Clicks / Spend / Orders——它们能推出 ACoS 再推出是否盈利，
#       会造成"特征泄漏"，让准确率虚高（本例 47% → 94%）
X = df[["Impressions", "CTR"]]
y = df["is_profit"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LogisticRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print("准确率:", round(accuracy_score(y_test, y_pred), 3))

# 基线：无脑猜多数类（盈利占比）的准确率。模型要明显高于基线才算真学到东西
print(df["is_profit"].value_counts())
