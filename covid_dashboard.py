import pandas as pd
import plotly.express as px
import streamlit as st

countries_covid =pd.DataFrame(pd.read_csv('countries_covid.csv'))

countries_covid.drop(columns=['todayCases', 'todayDeaths', 'todayRecovered','todayRecovered','countryInfo._id','countryInfo.iso2','countryInfo.iso3','countryInfo.lat','countryInfo.long'], inplace=True)
countries_covid.dropna(inplace=True)
countries_covid

# Which Top 10 countries have the highest total COVID-19 cases?

top10 = countries_covid.nlargest(10, 'cases')
fig1 = px.bar(top10,
             x='cases', y='country',
             orientation='h',
             color='cases',
             color_continuous_scale='Spectral',
             title='Top 10 Cases by Country',
             labels={'cases': 'Total Cases'},
             text_auto='.2s'
             )

# Which Top 10 countries recorded the highest number of deaths?
top10 = countries_covid.nlargest(10, 'deaths')
fig2 = px.bar(top10,
             x='deaths', y='country',
             orientation='h',
             color='deaths',
             color_continuous_scale='Spectral',
             title='Top 10 Deaths by Country',
             labels={'deaths': 'Total Deaths'},
             text_auto='.2s'
             )
fig2.show()

# Which countries have the highest recovery numbers?
top10 = countries_covid.nlargest(10, 'recovered')
fig3 = px.bar(top10,
             y='recovered', x='country',
             color='recovered',
             color_continuous_scale='Spectral',
             title='Top 10 Recovery by Country',
             labels={'recovered': 'Total Recovered'},
             text_auto='.2s'
             )

fig4 = px.pie(top10,
             values='active',
             names='country',
             title='Top 10 coutries per percentage of active cases',
             # FIX: Use color_discrete_sequence instead of color_continuous_scale
             color_discrete_sequence=px.colors.sequential.Oranges_r,
             hole=0.3)

# 3. Update traces for better visibility
fig4.update_traces(textposition='inside', textinfo='percent+label')

# Which top 10  countries have the highest death rate (deaths compared to total cases)?
countries_covid['death_rate'] = countries_covid['deaths'] / countries_covid['cases'] * 100
top10 = countries_covid.nlargest(10, 'death_rate')
fig5 = px.bar(top10,
              x= 'country',
              y= 'death_rate',
              color = 'death_rate',
              color_continuous_scale='Reds',
              labels={'country': 'Country', 'death_rate': 'Death Rate (%)'},
              title='Top 10 Countries by COVID-19 Death Rate'
)


# What is the relationship between active cases and critical cases across countries?
fig6 = px.scatter(countries_covid,
                  x='cases',
                  y='deaths',
                  color='active',
                   color_continuous_scale='Spectral',
                  title='Relationship between Active Cases and deaths across Countries',)


st.set_page_config(page_title="COVID-19 Dashboard", layout="wide")

st.title("🌍 COVID-19 Global Analysis Dashboard")

# Row 1: Total Cases & Deaths
col1, col2 = st.columns(2)
col1.plotly_chart(fig1, use_container_width=True)
col2.plotly_chart(fig2, use_container_width=True)

# Row 2: Recovered & Active %
col3, col4 = st.columns(2)
col3.plotly_chart(fig3, use_container_width=True)
col4.plotly_chart(fig4, use_container_width=True)

# Row 3: Death Rate & Active vs Critical
col5, col6 = st.columns(2)
col5.plotly_chart(fig5, use_container_width=True)
col6.plotly_chart(fig6, use_container_width=True)
