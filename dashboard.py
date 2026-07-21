import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Pandemic Pulse Dashboard",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv("covid_data.csv")
    return df

df = load_data()

st.markdown("<h1 style='text-align:center; color:#ff4b4b;'>🦠 Pandemic Pulse: COVID-19 Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

st.sidebar.header(" Filter Data")

region = st.sidebar.multiselect(
    "Select WHO Region",
    options=df["WHO Region"].unique(),
    default=df["WHO Region"].unique()
)

filtered_df = df[df["WHO Region"].isin(region)]

total_confirmed = int(filtered_df["Confirmed"].sum())
total_deaths = int(filtered_df["Deaths"].sum())
total_recovered = int(filtered_df["Recovered"].sum())
total_active = int(filtered_df["Active"].sum())

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Confirmed", f"{total_confirmed:,}")
col2.metric("Total Deaths", f"{total_deaths:,}")
col3.metric("Total Recovered", f"{total_recovered:,}")
col4.metric("Active Cases", f"{total_active:,}")

st.markdown("---")

st.subheader("Top 10 Countries by Confirmed Cases")

top10 = filtered_df.sort_values(by="Confirmed", ascending=False).head(10)

fig_bar = px.bar(
    top10,
    x="Country/Region",
    y="Confirmed",
    color="Confirmed",
    text="Confirmed",
    color_continuous_scale="Reds"
)

st.plotly_chart(fig_bar, use_container_width=True)

st.subheader("Case Distribution")

pie_df = pd.DataFrame({
    "Category": ["Confirmed", "Deaths", "Recovered", "Active"],
    "Values": [total_confirmed, total_deaths, total_recovered, total_active]
})

fig_pie = px.pie(
    pie_df,
    names="Category",
    values="Values",
    color_discrete_sequence=px.colors.sequential.RdBu
)

st.plotly_chart(fig_pie, use_container_width=True)

st.subheader(" WHO Region Analysis")

region_data = filtered_df.groupby("WHO Region")[["Confirmed", "Deaths", "Recovered"]].sum().reset_index()

fig_region = px.bar(
    region_data,
    x="WHO Region",
    y=["Confirmed", "Deaths", "Recovered"],
    barmode="group"
)

st.plotly_chart(fig_region, use_container_width=True)

st.subheader("Death Rate vs Recovery Rate")

fig_scatter = px.scatter(
    filtered_df,
    x="Deaths",
    y="Recovered",
    size="Confirmed",
    color="WHO Region",
    hover_name="Country/Region"
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.subheader(" Raw Data")

st.dataframe(filtered_df)
