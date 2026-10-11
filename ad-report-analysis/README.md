# 亚马逊广告报表自动化分析工具
> 项目定位：跨境B2C亚马逊运营辅助脚本，Python入门实践，用于广告报表快速复盘，自动计算广告核心指标，减少Excel重复操作。

## 项目背景
亚马逊运营日常需要下载广告后台CSV报表，手动在Excel计算ACoS、CTR、CVR，重复耗时间。
编写简易脚本，一键读取广告报表，自动清洗脏数据，计算广告核心KPI，输出汇总结果。

## 功能
1. 读取亚马逊下载的广告CSV原始报表
2. 数据清洗：去除空行、过滤无效曝光记录
3. 自动计算核心指标：
    - CTR = 点击量 / 曝光量
    - CVR = 订单数 / 点击量
    - ACoS = 广告花费 / 广告销售额
4. 输出广告组汇总结果，筛选高ACoS低效广告，方便运营做广告优化决策

## 技术栈
Python, pandas，基础CSV数据处理
> 说明：仅本地离线处理报表，不调用亚马逊API，仅用于运营数据分析学习。

## 运行方法
1. 将亚马逊后台导出的广告报表csv放入同目录
2. 修改脚本内文件名，运行python脚本，打印广告汇总指标与低效广告清单

```
## 📋 脚本运行输出示例
```
==== 广告报表汇总结果 ====
CampaignName  Impressions  Clicks  Spend  Sales    CTR    CVR    ACoS
0  ProductA-Keyword         1200      60   45.0  140.0  0.0500 0.0833 0.3214
1  ProductB-Keyword          800      24   32.0   75.0  0.0300 0.0833 0.4267
2  ProductC-Keyword         2000     120   90.0  220.0  0.0600 0.0750 0.4091
3  ProductD-Keyword         1500      45   60.0  130.0  0.0300 0.0667 0.4615

==== 高 ACoS 待优化广告组 ====
CampaignName    ACoS
0  ProductA-Keyword  0.3214
1  ProductB-Keyword  0.4267
2  ProductC-Keyword  0.4091
3  ProductD-Keyword  0.4615
```
> 脚本自动识别ACoS＞0.3的广告，快速筛选需要优化的广告活动。

