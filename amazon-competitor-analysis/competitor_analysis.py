import pandas as pd

# 读取模拟竞品csv数据
df = pd.read_csv("competitor_data.csv")

# 数据清洗：删除空值
df = df.dropna()

# 筛选条件：评分>=4.2，BSR排名小于5000
target_competitor = df[(df["star_rating"] >= 4.2) & (df["bsr_rank"] < 5000)]

print("======= 竞品数据汇总 =======")
print(f"统计竞品总数：{len(df)}")
# 价格区间统计
df["price_range"] = pd.cut(df["price"], bins=[20,30,40,50], labels=["20-30美元","30-40美元","40-50美元"])
print("价格区间分布：")
print(df["price_range"].value_counts())

print("\n======= 筛选：高潜力对标竞品（评分≥4.2，BSR排名<5000） =======")
print(target_competitor[["asin","title","price","star_rating","review_count","bsr_rank","category"]])
