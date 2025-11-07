#Import Libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set title and layout, tab-title
st.set_page_config(page_title="Premier League vs LaLiga", layout="wide")
st.title("Premier League vs LaLiga")

# Map the Datasets to corresponding year
PL_FILES = {2013: "out_pl.xlsx", 2014: "out_pl_2014.xlsx", 2015: "out_pl_2015.xlsx"}
ES_FILES = {2013: "out_es.xlsx", 2014: "out_es_2014.xlsx", 2015: "out_es_2015.xlsx"}

# Map the transferdatasets
TRANSFER_GB1 = "transfer_gb1.xlsx"
TRANSFER_ES1 = "transfer_es1.xlsx"

# This function loads an Excel file into a pandas DataFrame and standardizes the column names
@st.cache_data
def load_df(path):
    df = pd.read_excel(path)
    cols = {c.lower(): c for c in df.columns}
    rk = cols.get("rk", "Rk")
    sq = cols.get("squad", "Squad")
    df = df.rename(columns={rk: "Rk", sq: "Squad"})
    return df[["Rk", "Squad"]].dropna()

# Same as above for the transfer data
@st.cache_data
def load_transfer_df(path, league_label):
    df = pd.read_excel(path)
    df.columns = [c.lower() for c in df.columns]
    if "player_age" not in df.columns:
        raise ValueError(f"'player_age' column not found in {path}")
    if "season" not in df.columns:
        raise ValueError(f"'season' column not found in {path}")
    df = df.assign(League=league_label)
    return df

# Load data once to extract all seasons dynamically
transfer_gb1 = load_transfer_df(TRANSFER_GB1, "GB1")
transfer_es1 = load_transfer_df(TRANSFER_ES1, "ES1")

# Concatenate the datasets into one (we know age_df might not be the best name, but we'll stick with it for future use)
age_df = pd.concat([transfer_gb1, transfer_es1], ignore_index=True)

# For the dropdown menu, we get all unique seasons so we can use them for filtering
available_seasons = sorted(age_df["season"].unique())
season = st.selectbox("Season", available_seasons, index=0)

# Title in markdown
st.markdown("### Comparing the Leagues")

# Filter the dataframe to include only rows for the selected season
age_df_season = age_df[age_df["season"] == season]

# Check if there is any data available for that season
if age_df_season.empty:
    st.info(f"No player-age data available for season {season}.")
else:
# Create a box plot comparing player ages by league for the selected season
    fig = px.box(
        age_df_season,
        x="League",
        y="player_age",
        color="League",
        title=f"Player Age Comparison: GB1 vs ES1 ({season})",
    )
# Adjust the plot layout and set the axis titles
    fig.update_layout(
        template="plotly_white",
        xaxis_title="League",
        yaxis_title="Player Age",
    )
# Display the plot on streamlit
    st.plotly_chart(fig, use_container_width=True)

# Add a horizontal line
st.markdown("---")

# Get only the transfers with "in" as the direction and ignore those with written-out positions
filtered_df = age_df[
    (age_df['dir'] == 'in') &
    (~age_df['player_pos'].isin(['attack', 'midfield', 'defence']))
]

# Get unique leagues
leagues = filtered_df['league'].unique()

st.title("Player Position Distribution by League")

# Creating a pie chart for each league
for league in leagues:
    df_league = filtered_df[filtered_df['league'] == league]

    st.subheader(f"League: {league}")

    fig = px.pie(
    df_league,
    names='player_pos',
    title=f'Player Position Distribution in League: {league}',
    hole=0.3,
    color_discrete_sequence=px.colors.sequential.Blues
    )   

    # Display chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Set new title
st.markdown("### Total Transfer Fees per Season by League")

# Groupby the transfer amount and the league
fee_sum = age_df.groupby(['league', 'season'])['transfer_fee_amnt'].sum().reset_index()

# Creating a barchart
fig2 = px.bar(
    fee_sum,
    x='season',
    y='transfer_fee_amnt',
    color='league',
    barmode='group',
    title='Total Transfer Fees per Season by League',
    labels={
        'season': 'Season',
        'transfer_fee_amnt': 'Total Transfer Fee Amount',
        'league': 'League'
    }
)

# Barchart for the other league
fig2.update_layout(
    template="plotly_white",
    xaxis_title='Season',
    yaxis_title='Total Transfer Fee Amount',
    legend_title='League',
    width=900,
    height=600
)

# Display on streamlit
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

st.markdown("### Transfers per Window per League (2013–2015)")

# Filter dataframe for the specific seasons and the two leagues
filtered_df = age_df[
    (age_df['season'].isin([2013, 2014, 2015])) &
    (age_df['league'].isin(['GB1', 'ES1']))
]

# Groub by the number of transfers and also the the number of transfers in each window
transfer_counts = (
    filtered_df
    .groupby(['season', 'window', 'league'])
    .size()
    .reset_index(name='num_transfers')
)
# Create another barchart
fig3 = px.bar(
    transfer_counts,
    x='season',
    y='num_transfers',
    color='window',
    barmode='group',
    facet_col='league',
    title='Transfers per Window per League (2013–2015)',
    labels={
        'season': 'Season',
        'num_transfers': 'Number of Transfers',
        'window': 'Transfer Window'
    }
)

fig3.update_layout(
    template="plotly_white",
    xaxis_title='Season',
    yaxis_title='Number of Transfers',
    legend_title='Transfer Window'
)
# Display on streamlit
st.plotly_chart(fig3, use_container_width=True)

# End of Streamlit App



