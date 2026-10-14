import streamlit as st 
import pandas as pd 
import requests 

st.set_page_config(
 page_title="Displaying JSON Placeholder User Data", # Browser tab title
 page_icon="📊", # Browser tab icon
 layout="wide", # Use full browser width (default is "centered")
 initial_sidebar_state="expanded" # Sidebar starts open
)

# Fetching user data from JSON Placeholder and caching it
@st.cache_data
def load_users():
    response = requests.get("https://jsonplaceholder.typicode.com/users")
    response.raise_for_status()
    return response.json()

st.title(":blue[Displaying JSON Placeholder User Data]")

users = load_users()

# Extract the fields we need from each user
rows = []
for user in users:
    rows.append({
        "name": user["name"],
        "username": user["username"],
        "email": user["email"],
        "city": user["address"]["city"],
        "company": user["company"]["name"],
    })

df = pd.DataFrame(rows)

# Sidebar Name Filter
name_filter = st.sidebar.text_input("Filter by name")

filtered_df = df[df["name"].str.contains(name_filter, case=False)]

st.subheader("Users")
st.dataframe(filtered_df[["name", "username", "email", "city", "company"]])

# Metrics Row
col1, col2, col3 = st.columns(3)
col1.metric("Total Users", len(df))
col2.metric("Unique Cities", df["city"].nunique())
col3.metric("Unique Companies", df["company"].nunique())

# Bar Chart
st.subheader("Users per City")
city_counts = df["city"].value_counts().reset_index()
city_counts.columns = ["city","count"]
st.bar_chart(city_counts, x="city", y="count", color = "city")
