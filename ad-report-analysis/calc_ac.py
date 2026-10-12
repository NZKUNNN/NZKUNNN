import pandas as pd
df = pd.read_csv(r"C:\Users\HP\NZKUNNN\ad-report-analysis\ad_data_100.csv")
df = df[df["Sales"]>0]
df["ACOS"] = df["Spend"]/df["Sales"]
print(df.head())
print(df.describe())