import pandas as pd
import src.integration.yfinance_client as yfinance_client
import src.integration.gdelt_client as gdelt_client

# 获取K线
stock = {
    "symbol": "NVDA",
    "name": "Nvidia"
}
start = '2025-01-01'
end = '2025-07-27'
df_kline = yfinance_client.get_stock_data_with_indicators(ticker=stock.get("symbol", ""), start=start, end=end)
df_news = gdelt_client.get_company_sentiment(company=stock.get("name", ""), start_date=start, end_date=end)

df_kline["Date"] = pd.to_datetime(df_kline["Date"])
df_news["Date"] = pd.to_datetime(df_news["date"])

# 按照日期合并，保留所有 K 线数据
df_merged = pd.merge(df_kline, df_news, left_on="Date", right_on="Date", how="left")

# 可选：去除重复列或无用字段
df_merged.drop(columns=["Date"], inplace=True)

# 显示结果
print(df_merged.head(10))
