!pip install yfinance plotly --quiet

import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

stocks = ["AAPL","MSFT","GOOGL"]

data = yf.download(
    stocks,
    start="2024-01-01",
    end="2025-01-01",
    auto_adjust=True
)

close = data["Close"]

fig = go.Figure()

for stock in stocks:
    fig.add_trace(
        go.Scatter(
            x=close.index,
            y=close[stock],
            mode="lines",
            name=stock
        )
    )

fig.update_layout(
    title="Đồ thị giá 3 cổ phiếu",
    xaxis_title="Ngày",
    yaxis_title="Giá",
    template="plotly_white"
)

fig.show()

summary = pd.DataFrame()

summary["Giá hiện tại"] = close.iloc[-1]
summary["Giá cao nhất"] = close.max()
summary["Giá thấp nhất"] = close.min()
summary["% Thay đổi"] = (
    (close.iloc[-1]-close.iloc[0])/close.iloc[0]*100
).round(2)

print(summary)
