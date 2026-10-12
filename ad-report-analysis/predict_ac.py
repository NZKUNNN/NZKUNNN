import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
df = pd.read_csv(r"C:\Users\HP\NZKUNNN\ad-report-analysis\ad_data_100.csv")
df = df[df["Sales"]>0]
df["ACos"] = df["Spend"] / df["Sales"]
df["is_profit"] = (df["ACos"] < 0.5).astype(int)
X = df [["Impressions","CTR"]] # 特征：用来预测的输入
y = df["is_profit"] #目标：要来预测的东西
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42)
model = LogisticRegression()
model.fit(X_train,y_train)
y_pred = model.predict(X_test)
print("准确率：",round(accuracy_score(y_test,y_pred),3))
print(df[["Impressions","Clicks","Spend","Orders","CTR","ACos"]].corr().round(2))
print(df["is_profit"].value_counts())
