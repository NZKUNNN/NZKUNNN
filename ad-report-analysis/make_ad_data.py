import pandas as pd
import random

random.seed(42) #固定随机种子，让结果可复现

data = [ ]

for i in range(100):
     impressions = random.randint(500,3000)  # 曝光： 500~3000
     if i % 8 < 4:
         ctr = random.uniform(0.03,0.07) # Campaign-0~3:点击率偏高
         conv = random.uniform(0.15,0.25) # 转化率偏高
     else:
         ctr  = random.uniform(0.01,0.03) # Campaign-4~7:点击率偏低
         conv = random.uniform(0.02,0.05) # 转化率偏低
     clicks = int(impressions * ctr)  #点击 = 曝光 * 点击率（1%~8%）
     orders = int(clicks * conv)  #订单 = 点击 * 转化率（5%~15%）
     spend = round(clicks * random.uniform(0.5,1.2),2) #花费 = 点击 * 单次成本
     sales = round(orders * random.uniform(15,40),2)#销售额 = 订单 * 客单价
     data.append([f"Campaign-{i%8}",impressions,clicks,spend,sales,orders])

df = pd.DataFrame(data,columns=["Campaign","Impressions","Clicks","Spend","Sales","Orders"])

df["CTR"] = df["Clicks"]/df["Impressions"]

print("形状:",df.shape)
print(df.head())
print(df.describe())

df.to_csv(r"C:\Users\HP\NZKUNNN\ad-report-analysis\ad_data_100.csv",index=False)
print("已保存 ad_data_100.csv")