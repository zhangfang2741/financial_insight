import pandas as pd
import ta  # 技术指标库
import yfinance as yf
import os

# 设置 HTTP 和 HTTPS 代理（换成你自己的代理地址）
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'


def nine_turn_signal(df, close_col='Close'):
    periods = [3, 5, 8, 10, 12, 15, 30, 35, 40]

    ma_list = []
    for p in periods:
        ma = df[close_col].rolling(window=p, min_periods=1).mean()
        ma_list.append(ma)

    ma_df = pd.concat(ma_list, axis=1)
    ma_df.columns = [f'MA_{p}' for p in periods]

    # 比较收盘价与每条均线
    signals = (df[close_col].values.reshape(-1, 1) > ma_df.values).sum(axis=1)

    # signals的范围是0~9，调整成1~9区间
    signals = signals.clip(1, 9)

    return pd.Series(signals, index=df.index, name='NineTurnSignal')


def get_stock_basic_info(ticker="NVDA"):
    # 选择股票代码
    ticker = yf.Ticker(ticker)
    # 获取公司信息字典
    info = ticker.info
    # 打印常用字段
    return info


def get_stock_data_with_indicators(ticker='NVDA', start='2024-06-30', end='2025-06-30'):
    # 获取日线数据
    df = yf.download(ticker, start=start, end=end)
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
    df['percent'] = df['Close'].pct_change() * 100  # 百分比表示
    # 均线与趋势指标
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['EMA12'] = ta.trend.ema_indicator(df['Close'].squeeze(), window=12)
    df['EMA26'] = ta.trend.ema_indicator(df['Close'].squeeze(), window=26)
    df['MACD'] = df['EMA12'] - df['EMA26']

    # 动量与波动率
    df['RSI'] = ta.momentum.RSIIndicator(df['Close'].squeeze(), window=14).rsi()
    df['ATR'] = ta.volatility.AverageTrueRange(df['High'].squeeze(), df['Low'].squeeze(),
                                               df['Close'].squeeze()).average_true_range()

    # 布林带
    boll = ta.volatility.BollingerBands(df['Close'].squeeze())
    df['BOLL_UP'] = boll.bollinger_hband()
    df['BOLL_LOW'] = boll.bollinger_lband()

    # CCI（顺势指标）
    df['CCI'] = ta.trend.cci(high=df['High'].squeeze(), low=df['Low'].squeeze(), close=df['Close'].squeeze(), window=20)

    # 九转序列（TD Sequential）计算
    df['NineTurnSignal'] = nine_turn_signal(df)
    df = df.dropna()
    df = df.rename(columns={"index": "Date"}, inplace=True)
    return df
