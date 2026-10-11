import pandas as pd

# 亚马逊广告报表分析脚本，用于运营广告指标复盘
if __name__ == "__main__":
    # 读取广告csv报表（亚马逊后台下载）
    df = pd.read_csv("sample_ad_data.csv")

    # 数据清洗：去除空值
    df = df.dropna(subset=["Impressions", "Clicks", "Spend", "Sales"])
    # 过滤曝光为0无效行
    df = df[df["Impressions"] > 0]

    # 计算核心广告指标
    df["CTR"] = df["Clicks"] / df["Impressions"]
    df["CVR"] = df["Orders"] / df["Clicks"]
    df["ACoS"] = df["Spend"] / df["Sales"]

    # 保留4位小数，百分比展示
    df["CTR"] = df["CTR"].round(4)
    df["CVR"] = df["CVR"].round(4)
    df["ACoS"] = df["ACoS"].round(4)

    print("====广告报表汇总结果====")
    print(df[["CampaignName", "Impressions", "Clicks", "Spend", "Sales", "CTR", "CVR", "ACoS"]])
    # 筛选ACoS大于0.3的低效广告组
    high_acos = df[df["ACoS"] > 0.3]
    print("\n====高ACoS待优化广告组====")
    print(high_acos[["CampaignName", "ACoS"]])
