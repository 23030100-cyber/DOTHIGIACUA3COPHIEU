import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Tiêu đề
st.set_page_config(page_title="Stock Chart App", layout="wide")

st.title("📈 Ứng dụng theo dõi giá 3 cổ phiếu")

st.write("Chọn tối đa 3 mã cổ phiếu để xem biểu đồ.")

# Danh sách cổ phiếu
stock_options = [
    "AAPL", "MSFT", "GOOGL",
    "AMZN", "META", "TSLA",
    "NVDA", "FPT.VN", "HPG.VN", "VCB.VN"
]

stocks = st.multiselect(
    "Chọn cổ phiếu",
    stock_options,
    default=["AAPL", "MSFT", "GOOGL"],
    max_selections=3
)

# Chọn thời gian
period = st.selectbox(
    "Khoảng thời gian",
    ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
    index=3
)

if st.button("📊 Xem biểu đồ"):

    if len(stocks) == 0:
        st.warning("Vui lòng chọn ít nhất 1 cổ phiếu.")
    else:

        data = yf.download(
            stocks,
            period=period,
            auto_adjust=True,
            progress=False
        )

        close = data["Close"]

        st.subheader("Dữ liệu")

        st.dataframe(close.tail())

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
            title="Biểu đồ giá cổ phiếu",
            xaxis_title="Ngày",
            yaxis_title="Giá đóng cửa",
            template="plotly_white",
            height=600
        )

        st.plotly_chart(fig, use_container_width=True)

        summary = pd.DataFrame()

        summary["Giá hiện tại"] = close.iloc[-1]
        summary["Giá cao nhất"] = close.max()
        summary["Giá thấp nhất"] = close.min()

        summary["% Thay đổi"] = (
            (close.iloc[-1] - close.iloc[0])
            / close.iloc[0] * 100
        ).round(2)

        st.subheader("Thống kê")

        st.dataframe(summary.style.format({
            "Giá hiện tại": "{:.2f}",
            "Giá cao nhất": "{:.2f}",
            "Giá thấp nhất": "{:.2f}",
            "% Thay đổi": "{:.2f}%"
        }))
