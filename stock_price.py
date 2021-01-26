import streamlit as st
import yfinance as yf
import pandas as pd

# Wite on the App in markdown stile
st.write("""
# Stock Price App

+ Google's closing price and trading volume graph.

""")

tickerSymbol = 'GOOGL'
tickerData = yf.Ticker(tickerSymbol)
tickerDf = tickerData.history(period='1d',
                              start='2005-01-01',
                              end='2021-01-26')

st.line_chart(tickerDf.Close)
st.line_chart(tickerDf.Volume)
