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

# Download Data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode() # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerStats.csv">Download CSV File</a>'
    return href


st.markdown(filedownload(df_selected_players), unsafe_allow_html=True)

# Heatmap
if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')
    aux = df_selected_players.drop(['Player', 'Pos', 'Tm'], axis=1)
    aux = aux.astype(float)
    corr = aux.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot(f)