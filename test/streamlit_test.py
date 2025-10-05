import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import plotly.graph_objs as go

# --------------------------
# 页面配置
# --------------------------
st.set_page_config(page_title="📊 高级投资组合与图结构模拟", layout="wide")
st.title("📈 多资产投资组合动态与资产关系可视化")

# --------------------------
# 左侧控制栏
# --------------------------
st.sidebar.header("投资参数设置")
num_assets = st.sidebar.slider("投资资产数量", 2, 5, 3)
assets = [f"资产{i+1}" for i in range(num_assets)]
weights = []
for asset in assets:
    w = st.sidebar.slider(f"{asset} 权重 (%)", 0, 100, 100//num_assets)
    weights.append(w)
weights = np.array(weights)/100

initial_investment = st.sidebar.number_input("初始投资金额 ($)", 1000, 1000000, 10000, step=1000)
years = st.sidebar.slider("投资年数", 1, 30, 10)
strategy = st.sidebar.selectbox("投资策略", ["固定收益", "随机波动"])

st.sidebar.header("资产收益设置")
expected_returns = []
volatilities = []
for asset in assets:
    r = st.sidebar.slider(f"{asset} 预期年化收益率 (%)", 0.0, 20.0, 8.0, 0.5)
    v = st.sidebar.slider(f"{asset} 波动率 (%)", 0.0, 30.0, 10.0, 0.5)
    expected_returns.append(r/100)
    volatilities.append(v/100)

# --------------------------
# 模拟计算
# --------------------------
np.random.seed(42)
years_array = np.arange(1, years+1)
asset_values = []

for i in range(num_assets):
    values = [initial_investment * weights[i]]
    for y in range(1, years+1):
        if strategy == "固定收益":
            growth = values[-1] * (1 + expected_returns[i])
        else:
            growth = values[-1] * (1 + expected_returns[i] + np.random.normal(0, volatilities[i]))
        values.append(growth)
    asset_values.append(values[1:])  # 去掉初始值

portfolio_values = np.sum(asset_values, axis=0)

# --------------------------
# Plotly 时间序列图
# --------------------------
st.subheader("📊 投资组合时间序列（Plotly）")
fig = go.Figure()
for i in range(num_assets):
    fig.add_trace(go.Scatter(
        x=years_array,
        y=asset_values[i],
        mode='lines+markers',
        name=assets[i]
    ))
fig.add_trace(go.Scatter(
    x=years_array,
    y=portfolio_values,
    mode='lines+markers',
    name='组合总价值',
    line=dict(color='black', width=3)
))
fig.update_layout(
    xaxis_title='年份',
    yaxis_title='投资价值 ($)',
    hovermode='x unified'
)
st.plotly_chart(fig, use_container_width=True)

# --------------------------
# NetworkX 资产关系图
# --------------------------
st.subheader("🌐 资产关系图（NetworkX + Pyvis）")
# 构建简单图：用权重作为节点大小，随机连边表示相关性
G = nx.Graph()
for i, asset in enumerate(assets):
    G.add_node(asset, size=weights[i]*50+10)

# 随机连接节点
for i in range(num_assets):
    for j in range(i+1, num_assets):
        G.add_edge(assets[i], assets[j], weight=np.random.rand())

# 使用 Pyvis 可视化
net = Network(height='400px', width='100%', notebook=False)
net.from_nx(G)
# 生成 HTML 并嵌入 Streamlit
net.save_graph('graph.html')
HtmlFile = open('graph.html', 'r', encoding='utf-8')
components.html(HtmlFile.read(), height=450)

# --------------------------
# 数据表格
# --------------------------
df = pd.DataFrame({ "年份": years_array })
for i in range(num_assets):
    df[assets[i]] = asset_values[i]
df["组合总价值"] = portfolio_values
st.subheader("📋 模拟结果数据表")
st.dataframe(df)

# --------------------------
# CSV 导出
# --------------------------
st.download_button(
    label="⬇️ 下载 CSV 数据",
    data=df.to_csv(index=False).encode('utf-8-sig'),
    file_name="投资组合模拟.csv",
    mime="text/csv"
)
