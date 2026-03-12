import pandas as pd
import plotly.express as px
import streamlit as st

# 1. Page Configuration
st.set_page_config(page_title="COVID-19 Global Dashboard", layout="wide")

st.title("🌍 COVID-19 Global Data Analysis")
st.markdown("This dashboard analyzes global COVID-19 trends using Plotly and Streamlit.")

# 2. Data Loading
@st.cache_data # Caches data so it doesn't reload on every click
def load_data():
    df = pd.read_csv('countries_covid.csv')
    # Cleaning
    cols_to_drop = ['todayCases', 'todayDeaths', 'todayRecovered', 'countryInfo._id', 
                    'countryInfo.iso2', 'countryInfo.iso3', 'countryInfo.lat', 'countryInfo.long']
    df.drop(columns=[c for c in cols_to_drop if c in df.columns], inplace=True)
    df.dropna(inplace=True)
    return df

df = load_data()

# 3. Sidebar Filters (Optional but nice for dashboards)
st.sidebar.header("Filter Options")
top_n = st.sidebar.slider("Select number of countries:", 5, 20, 10)

# --- VISUALIZATIONS ---

# Row 1: Cases and Deaths
col1, col2 = st.columns(2)

with col1:
    top10_cases = df.nlargest(top_n, 'cases')
    fig1 = px.bar(top10_cases, x='cases', y='country', orientation='h',
                 color='cases', color_continuous_scale='Spectral',
                 title=f'Top {top_n} Cases by Country', text_auto='.2s')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    top10_deaths = df.nlargest(top_n, 'deaths')
    fig2 = px.bar(top10_deaths, x='deaths', y='country', orientation='h',
                 color='deaths', color_continuous_scale='Spectral',
                 title=f'Top {top_n} Deaths by Country', text_auto='.2s')
    st.plotly_chart(fig2, use_container_width=True)

# Row 2: Recoveries and Active Percentage
col3, col4 = st.columns(2)

with col3:
    top10_rec = df.nlargest(top_n, 'recovered')
    fig3 = px.bar(top10_rec, y='recovered', x='country',
                 color='recovered', color_continuous_scale='Spectral',
                 title=f'Top {top_n} Recovery by Country', text_auto='.2s')
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    top10_active = df.nlargest(top_n, 'active')
    fig4 = px.pie(top10_active, values='active', names='country',
                 title=f'Active Cases Distribution (Top {top_n})',
                 color_discrete_sequence=px.colors.sequential.Oranges_r, hole=0.3)
    fig4.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig4, use_container_width=True)

# Row 3: Death Rate and Relationships
col5, col6 = st.columns(2)

with col5:
    df['death_rate'] = (df['deaths'] / df['cases']) * 100
    top10_rate = df.nlargest(top_n, 'death_rate')
    fig5 = px.bar(top10_rate, x='country', y='death_rate',
                 color='death_rate', color_continuous_scale='Reds',
                 title=f'Top {top_n} Countries by Death Rate (%)')
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    fig6 = px.scatter(df, x='cases', y='deaths', color='active',
                     color_continuous_scale='Spectral',
                     title='Relationship: Total Cases vs Deaths')
    st.plotly_chart(fig6, use_container_width=True)

# Display Raw Data if user wants
if st.checkbox("Show Raw Data"):
    st.dataframe(df)
