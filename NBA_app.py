import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title("NBA Players Statistics Explorer")

st.markdown("""
This app performs a webscraping of NBA player stats data!
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [Basketball-reference.com](https://www.basketball-reference.com/).
""")

# Sidebar: Year Selection
st.sidebar.header("User Input Features")
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950,2020))))

# Webscraping
@st.cache
def scrap_data(year):
    url= "https://www.basketball-reference.com/leagues/NBA_" + str(year) +"_per_game.html"
    html = pd.read_html(url, header=0)
    df = html[0]
    raw = df.drop(df[df.Age == "Age"].index) # the table's header is repeated inside the table
    raw= raw.fillna(0)
    stats = raw.drop(['Rk'], axis=1)
    return stats


playerStats = scrap_data(selected_year)

# Sidebar: Team Selection
sorted_unique_teams = sorted(playerStats.Tm.unique())
selected_teams = st.sidebar.multiselect('Teams', sorted_unique_teams, sorted_unique_teams)

# Sidebar: Position Selection
sorted_unique_positions = sorted(playerStats.Pos.unique())
selected_positions = st.sidebar.multiselect('Positions', sorted_unique_positions, sorted_unique_positions)

# Filtering Data
df_selected_players = playerStats[(playerStats.Tm.isin(selected_teams)) &
                                  (playerStats.Pos.isin(selected_positions))]

# Show Results
st.header('Display Player Stats of Selected Team(s) and Position(s)')
st.write('Data Dimension: ' + str(df_selected_players.shape[0]) + ' rows and ' +
         str(df_selected_players.shape[1]) + ' columns.')
st.dataframe(df_selected_players)

