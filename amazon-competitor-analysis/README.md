# 亚马逊竞品Listing数据分析项目
> 亚马逊运营日常竞品调研工具，基于模拟竞品ASIN数据集，批量分析竞品价格、BSR排名、评分、评论数量，筛选优质对标竞品，辅助选品、定价与Listing策略制定。

## 项目功能
1. 读取竞品清单CSV数据集，做数据清洗，剔除异常、缺失数据
2. 统计：价格分布区间、商品评分分布、BSR类目排名分布
3. 筛选目标：高评分、BSR排名靠前的对标竞品
4. 输出汇总分析结果，快速识别竞品优势与市场机会

## 📊 字段说明
- asin：亚马逊商品ASIN编号
- title：商品标题
- price：售价（美元）
- star_rating：商品评分
- review_count：评论总数
- bsr_rank：类目BSR排名，数字越小销量越高
- category：所属类目

## 🛠️ 技术栈
Python, Pandas，CSV数据处理，纯本地离线分析，**无爬虫，全部使用模拟数据**

## 📋 运行输出示例
'''
======= 竞品数据汇总 =======
统计竞品总数：10
价格区间分布：
20-30 美元: 4 个
30-40 美元: 3 个
40-50 美元: 3 个

======= 筛选：高潜力对标竞品（评分≥4.2，BSR 排名 < 5000） =======
asin                                  title  price  star_rating  review_count  bsr_rank category
0  B0XXXX0001  Stainless Steel Water Bottle Insulated  24.99          4.5          1280      1250  Kitchen
1  B0XXXX0002  Portable Camping LED Light Waterproof  29.99          4.3           960      2100  Outdoor
2  B0XXXX0005  Silicone Food Storage Bags Reusable    32.99          4.6          1650      1800  Kitchen

'''
> 脚本自动筛选符合条件的对标竞品，帮助运营快速锁定需要重点研究的ASIN。
```
