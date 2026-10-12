# -*- coding: utf-8 -*-
# 回归：线性回归预测 ACoS（ACoS 是多少）
# 流程：读数据 -> 清洗 -> 算目标 -> 拆训练/测试 -> 训练 -> 预测 -> 评估 -> 系数解读
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error

df = pd.read_csv(r"C:\Users\HP\NZKUNNN\ad-report-analysis\ad_data_100.csv")
df = df[df["Sales"] > 0]                       # 清洗：去掉销售额为0的行（避免除零）
df["ACoS"] = df["Spend"] / df["Sales"]          # 目标：ACoS = 花费 / 销售额

# 特征（X）：用来预测的输入；目标（y）：要预测的答案
X = df[["Impressions", "Clicks", "Spend", "Orders", "CTR"]]
y = df["ACoS"]

# 拆成训练/测试：80%训练、20%测试，用模型没见过的数据验证真实能力
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)                     # 训练：自动算出最优系数

# 系数解读：每个特征变化1单位，ACoS平均变多少（共线性存在时系数会失真，需结合相关性矩阵看）
print("截距 b:", round(model.intercept_, 4))
for name, coef in zip(X.columns, model.coef_):
    print(name, "的系数:", round(coef, 4))

y_pred = model.predict(X_test)                  # 预测测试集
print("R2 :", round(r2_score(y_test, y_pred), 3))       # 解释了多少比例（越高越好）
print("MAE:", round(mean_absolute_error(y_test, y_pred), 3))  # 平均偏多少（越小越好）

# 相关性矩阵：诊断特征间多重共线性（越接近 ±1 越相关，系数越不可信）
print(df[["Impressions", "Clicks", "Spend", "Orders", "CTR", "ACoS"]].corr().round(2))
