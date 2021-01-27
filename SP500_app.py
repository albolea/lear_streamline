import pandas as pd
import base64
import streamlit as st
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

st.title("S&P 500 Analysis")
st.markdown("""
This app performs a webscraping of S&P 500 Data
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [wikipedia.com](https://en.wikipedia.org/wiki/List_of_S&P_500_companies).
""")


# Webscraping
@st.cache
def scrap_data():
    url = "https://en.wikipedia.org/wiki/List_of_S&P_500_companies"
    html = pd.read_html(url, header=0)
    df = html[0]
    return df


sp500 = scrap_data()

# Sidebar: Sectors
unique_sectors = sorted(sp500["GICS Sector"].unique())
selected_sectors = st.sidebar.multiselect("Sectors", unique_sectors, unique_sectors)

# Filtering Data
sp500_filtered = sp500.loc[sp500["GICS Sector"].isin(selected_sectors), :]

# Main Page
st.header("Display S&P500 Companies in Selected Sectors")
st.write(str(sp500_filtered.shape[0]) + ' Companies')
st.dataframe(sp500_filtered)

# Download Data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="SP500_Companies.csv">Download CSV File</a>'
    return href


st.markdown(filedownload(sp500_filtered), unsafe_allow_html=True)

# Plot Close Price graphs
data = yf.download(
        tickers=list(sp500_filtered[0:10].Symbol),
        period="1y",
        interval="1d",
        group_by="ticker",
        auto_adjust=True,
        prepost=True,
        threads=True,
        proxy=None
)


def price_plot(symbol):
  df = pd.DataFrame(data[symbol].Close)
  df['Date'] = df.index
  fig, ax = plt.subplots()
  ax.fill_between(df.Date, df.Close, color='skyblue', alpha=0.3)
  ax.plot(df.Date, df.Close, color='skyblue', alpha=0.8)
  plt.title(symbol, fontweight='bold')
  plt.xlabel('Date', fontweight='bold')
  plt.ylabel('Closing Price', fontweight='bold')
  return st.pyplot(fig)


num_company = st.sidebar.slider('Number of Companies', 1, 5)

if st.button('Show Plots'):
    st.header('Stock Closing Price')
    for i in list(sp500_filtered.Symbol)[:num_company]:
        price_plot(i)