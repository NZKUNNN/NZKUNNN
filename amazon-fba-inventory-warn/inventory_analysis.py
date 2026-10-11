import pandas as pd
import matplotlib.pyplot as plt

# 设置中文（解决图片中文乱码）
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# 读取FBA库存模拟报表
df = pd.read_csv("sample_inventory.csv")

# 计算库存周转天数：现有可售库存 / 日均销量
df["inventory_turn_days"] = df["available_stock"] / df["daily_sales"].replace(0, 0.001)

# 库存预警规则（亚马逊运营常用标准）
def get_warn_level(row):
    turn_days = row["inventory_turn_days"]
    if turn_days <= 15:
        return "🔴 紧急预警：库存不足，有断货风险"
    elif turn_days <=30:
        return "🟡 注意：库存偏低，建议安排补货"
    elif turn_days >90:
        return "🟠 积压预警：库存过多，产生长期仓储费"
    else:
        return "🟢 库存健康"

df["warn_status"] = df.apply(get_warn_level, axis=1)

# 筛选预警商品
warn_df = df[df["warn_status"].str.contains("预警")]

print("===== FBA库存健康分析报告 =====")
print(df[["sku","available_stock","daily_sales","inventory_turn_days","warn_status"]])
print("\n===== 需要重点关注的SKU预警清单 =====")
print(warn_df[["sku","available_stock","daily_sales","inventory_turn_days","warn_status"]])

# 导出结果到新csv
df.to_csv("inventory_result.csv", index=False, encoding="utf-8-sig")
print("\n✅ 分析完成，结果已保存至 inventory_result.csv")

# ============ 新增绘图部分 ============
plt.figure(figsize=(10,6))
colors = []
for days in df["inventory_turn_days"]:
    if days <=15:
        colors.append("#ff3333")
    elif days <=30:
        colors.append("#ffcc00")
    elif days>90:
        colors.append("#ff7722")
    else:
        colors.append("#33bb55")

plt.bar(df["sku"], df["inventory_turn_days"], color=colors)
plt.axhline(y=15, color='red', linestyle='--', label='断货预警线(15天)')
plt.axhline(y=30, color='gold', linestyle='--', label='补货提醒线(30天)')
plt.axhline(y=90, color='#ff7722', linestyle='--', label='积压预警线(90天)')
plt.title("FBA各SKU库存周转天数预警图")
plt.xlabel("SKU")
plt.ylabel("库存周转天数")
plt.legend()
plt.tight_layout()
plt.savefig("inventory_warn_chart.png", dpi=150)
plt.show()
print("✅ 库存预警图表已生成：inventory_warn_chart.png")
