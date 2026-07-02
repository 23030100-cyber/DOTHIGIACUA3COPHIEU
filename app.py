import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Đồ thị giá 3 cổ phiếu", layout="wide")

st.title("📈 Ứng dụng vẽ đồ thị giá của 3 cổ phiếu theo thời gian- đề tài nhóm 8")

st.sidebar.header("Nhập thông tin")

stock1 = st.sidebar.text_input("Mã cổ phiếu thứ nhất", "VCB.VN")
stock2 = st.sidebar.text_input("Mã cổ phiếu thứ hai", "BID.VN")
stock3 = st.sidebar.text_input("Mã cổ phiếu thứ ba", "CTG.VN")

start = st.sidebar.date_input("Ngày bắt đầu", pd.to_datetime("2024-01-01"))
end = st.sidebar.date_input("Ngày kết thúc", pd.to_datetime("2025-01-01"))

if st.sidebar.button("Xem kết quả"):

    data = yf.download(
        [stock1, stock2, stock3],
        start=start,
        end=end,
        auto_adjust=True
    )["Close"]

    st.subheader("Dữ liệu giá đóng cửa")
    st.dataframe(data)

    st.subheader("Giá cao nhất")
    st.write(data.max())

    st.subheader("Giá thấp nhất")
    st.write(data.min())

    st.subheader("Giá trung bình")
    st.write(data.mean())

    # Mức thay đổi giá
    change = data.diff()

    st.subheader("Mức thay đổi giá")
    st.dataframe(change.tail())

    # Tỷ suất sinh lời
    returns = data.pct_change() * 100

    st.subheader("Tỷ suất sinh lời (%)")
    st.dataframe(returns.tail())

    # MA5
    ma5 = data.rolling(5).mean()

    # Độ biến động
    volatility = returns.std()

    st.subheader("Độ biến động")
    st.write(volatility)

    # Biểu đồ giá
    st.subheader("Biểu đồ giá cổ phiếu")

    fig, ax = plt.subplots(figsize=(12,6))

    for stock in data.columns:
        ax.plot(data.index, data[stock], label=stock)

    ax.set_title("Biểu đồ giá của 3 cổ phiếu")
    ax.set_xlabel("Ngày")
    ax.set_ylabel("Giá đóng cửa")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

    # Biểu đồ MA5
    st.subheader("Đường trung bình động MA5")

    fig2, ax2 = plt.subplots(figsize=(12,6))

    for stock in ma5.columns:
        ax2.plot(ma5.index, ma5[stock], label=f"MA5 - {stock}")

    ax2.set_title("Moving Average (MA5)")
    ax2.set_xlabel("Ngày")
    ax2.set_ylabel("Giá")
    ax2.legend()
    ax2.grid(True)

    st.pyplot(fig2)
