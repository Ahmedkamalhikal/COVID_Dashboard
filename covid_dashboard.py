import pandas as pd
import plotly.express as px
import streamlit as st
import altair

st.set_page_config(page_title="COVID Dashboard", layout="wide")

st.title("📊 Global COVID-19 Analytics Dashboard")
st.markdown("---")

# 2. Data Loading & Cleaning
@st.cache_data
def get_data():
    # Load the CSV file
    df = pd.read_csv('countries_covid.csv')
    
    # Drop the specific columns you requested
    cols_to_drop = [
        'todayCases', 'todayDeaths', 'todayRecovered', 
        'countryInfo._id', 'countryInfo.iso2', 'countryInfo.iso3', 
        'countryInfo.lat', 'countryInfo.long'
    ]
    # Use errors='ignore' in case some columns are already missing
    df.drop(columns=cols_to_drop, inplace=True, errors='ignore')
    
    # Remove rows with missing values
    df.dropna(inplace=True)
    return df

countries_covid = get_data()

# 3. Create Visualizations
# --- Fig 1: Top 10 Cases ---
top10_cases = countries_covid.nlargest(10, 'cases')
fig1 = px.bar(top10_cases, x='cases', y='country', orientation='h',
             color='cases', color_continuous_scale='Spectral',
             title='Top 10 Cases by Country', labels={'cases': 'Total Cases'},
             text_auto='.2s')

# --- Fig 2: Top 10 Deaths ---
top10_deaths = countries_covid.nlargest(10, 'deaths')
fig2 = px.bar(top10_deaths, x='deaths', y='country', orientation='h',
             color='deaths', color_continuous_scale='Spectral',
             title='Top 10 Deaths by Country', labels={'deaths': 'Total Deaths'},
             text_auto='.2s')

# --- Fig 3: Top 10 Recoveries ---
top10_rec = countries_covid.nlargest(10, 'recovered')
fig3 = px.bar(top10_rec, y='recovered', x='country',
             color='recovered', color_continuous_scale='Spectral',
             title='Top 10 Recovery by Country', labels={'recovered': 'Total Recovered'},
             text_auto='.2s')

# --- Fig 4: Active Cases Pie ---
fig4 = px.pie(top10_rec, values='active', names='country',
             title='Top 10 Countries: Percentage of Active Cases',
             color_discrete_sequence=px.colors.sequential.Oranges_r, hole=0.3)
fig4.update_traces(textposition='inside', textinfo='percent+label')

# --- Fig 5: Death Rate ---
countries_covid['death_rate'] = (countries_covid['deaths'] / countries_covid['cases']) * 100
top10_rate = countries_covid.nlargest(10, 'death_rate')
fig5 = px.bar(top10_rate, x='country', y='death_rate',
             color='death_rate', color_continuous_scale='Reds',
             labels={'country': 'Country', 'death_rate': 'Death Rate (%)'},
             title='Top 10 Countries by COVID-19 Death Rate')

# --- Fig 6: Active vs Deaths Scatter ---
fig6 = px.scatter(countries_covid, x='cases', y='deaths', color='active',
                 color_continuous_scale='Spectral',
                 title='Relationship: Total Cases vs Deaths')

# 4. Displaying Charts in Streamlit Layout
# Use columns to make it look like a real dashboard
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig3, use_container_width=True)
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    st.plotly_chart(fig2, use_container_width=True)
    st.plotly_chart(fig4, use_container_width=True)
    st.plotly_chart(fig6, use_container_width=True)

# Optional: Show the dataframe
if st.checkbox("Show cleaned dataset"):
    st.write(countries_covid)
