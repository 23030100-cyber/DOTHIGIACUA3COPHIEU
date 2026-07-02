import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# =========================
# Cấu hình trang
# =========================
st.set_page_config(
    page_title="Stock Chart App",
    page_icon="📈",
    layout="wide"
)

st.title("📈 ỨNG DỤNG THEO DÕI GIÁ CỔ PHIẾU")
st.markdown("---")

# =========================
# Sidebar
# =========================
st.sidebar.header("Tùy chọn")

stock_options = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META",
    "TSLA", "NVDA",
    "FPT.VN", "HPG.VN", "VCB.VN"
]

stocks = st.sidebar.multiselect(
    "Chọn tối đa 3 cổ phiếu",
    stock_options,
    default=["AAPL", "MSFT", "GOOGL"],
    max_selections=3
)

period = st.sidebar.selectbox(
    "Khoảng thời gian",
    [
        "1mo",
        "3mo",
        "6mo",
        "1y",
        "2y",
        "5y"
    ]
)

# =========================
# Nút xem biểu đồ
# =========================
if st.sidebar.button("Xem biểu đồ"):

    if len(stocks) == 0:
        st.warning("Vui lòng chọn ít nhất 1 cổ phiếu.")
        st.stop()

    with st.spinner("Đang tải dữ liệu..."):

        data = yf.download(
            stocks,
            period=period,
            auto_adjust=True,
            progress=False
        )

    close = data["Close"]

    # =========================
    # Bảng dữ liệu
    # =========================
    st.subheader("📋 Dữ liệu giá đóng cửa")

    st.dataframe(close)

    # =========================
    # Biểu đồ
    # =========================
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

        yaxis_title="Giá",

        hovermode="x unified",

        template="plotly_white",

        height=600

    )

    st.plotly_chart(fig, use_container_width=True)

    # =========================
    # Thống kê
    # =========================
    summary = pd.DataFrame()

    summary["Giá hiện tại"] = close.iloc[-1]

    summary["Giá cao nhất"] = close.max()

    summary["Giá thấp nhất"] = close.min()

    summary["% Thay đổi"] = (
        (close.iloc[-1]-close.iloc[0])
        /close.iloc[0]*100
    ).round(2)

    st.subheader("📊 Thống kê")

    st.dataframe(summary)

    # =========================
    # Hiển thị Metric
    # =========================

    st.subheader("Thông tin nhanh")

    cols = st.columns(len(stocks))

    for i, stock in enumerate(stocks):

        with cols[i]:

            st.metric(

                label=stock,

                value=f"{summary.loc[stock,'Giá hiện tại']:.2f}",

                delta=f"{summary.loc[stock,'% Thay đổi']:.2f}%"

            )

else:

    st.info("👈 Hãy chọn cổ phiếu và nhấn 'Xem biểu đồ'.")
