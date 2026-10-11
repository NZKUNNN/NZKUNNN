import pandas as pd
import random

random.seed(42) #固定随机种子，让结果可复现

data = [ ]

for i in range(100):
     impressions = random.randint(500,3000)  # 曝光： 500~3000
     clicks = int(impressions * random.uniform(0.01,0.08))  #点击 = 曝光 * 点击率（1%~8%）
     orders = int(clicks * random.uniform(0.05,0.15))  #订单 = 点击 * 转化率（5%~15%）
     spend = round(clicks * random.uniform(0.5,1.2),2) #花费 = 点击 * 单次成本
     sales = round(orders * random.uniform(15,40),2)#销售额 = 订单 * 客单价
     data.append([f"Campaign-{i%8}",impressions,clicks,spend,sales,orders])

df = pd.DataFrame(data,columns=["Campaign","Impressions","Clicks","Spend","Sales","Orders"])

print("形状:",df.shape)
print(df.head())
print(df.describe())

df.to_csv(r"C:\Users\HP\NZKUNNN\ad-report-analysis\ad_data_100.csv",index=False)
print("已保存 ad_data_100.csv")