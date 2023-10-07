import streamlit as st
import pandas as pd
import plotly.express as px

# Load your DataFrame
# Assuming df contains 'name', 'x', 'y', and 'category' columns
df = pd.read_csv("your_data.csv")

# Create scatterplot with Streamlit
st.title("Word Embeddings Visualization")
category_filter = st.selectbox("Select Category:", df['category'].unique())
filtered_df = df[df['category'] == category_filter]

fig = px.scatter(filtered_df, x='x', y='y', text='name', color='category')
st.plotly_chart(fig)
