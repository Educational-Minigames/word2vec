import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
import json
from utils import *

PLOT_HEIGHT = 600

config = st.experimental_get_query_params()
ADD_WORDS = (config.get('add_words', 'false')) != 'false'
SHOW_RELATIONS = (config.get('show_relations', 'false')) != 'false'
SHOW_COLORS = (config.get('show_colors', 'false')) != 'false'

# Function to create and return the scatterplot figure with arrows for a selected relation
def create_scatterplot_with_arrows(data, relation_data=[]):
    if SHOW_COLORS:
        fig = px.scatter(data, x="x", y="y", text="word", color="cluster")
    else:
        fig = px.scatter(data, x="x", y="y", text="word")
    fig.update_traces(
        marker=dict(size=7),
        textfont=dict(family='Noto Sans Arabic', size=16),
        textposition='top center',
        hoverinfo='x+y+text'
    )

    # Add arrows for each word pair in the selected relation
    for pair in relation_data:
        word1, word2 = pair
        x1, y1 = data[data['word'] == word1]['x'].values[0], data[data['word'] == word1]['y'].values[0]
        x2, y2 = data[data['word'] == word2]['x'].values[0], data[data['word'] == word2]['y'].values[0]

        # Add an arrow annotation
        fig.add_annotation(
            text="",
            x=x1,
            y=y1,
            showarrow=True,
            ax=x2,
            axref='x',
            ay=y2,
            ayref='y',
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor='black'
        )

    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=PLOT_HEIGHT,
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
    )

    return fig

# Load the data from the CSV file
data = pd.read_csv("data.csv")

# Delete the 'Unnamed: 0' column
if 'Unnamed: 0' in data.columns:
    del data['Unnamed: 0']

# Load relationship data from the "groups.json" file
with open("groups.json", "r", encoding="utf-8") as json_file:
    relationship_data = json.load(json_file)

# Split the DataFrame into 'data' and 'hidden_data' based on NaN values in the 'cluster' column
hidden_data = data[data['cluster'].isna()]
data = data.dropna(subset=['cluster'])

# Configure Streamlit to be in wide mode and remove the title
st.set_page_config(layout="wide")

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# Create a Streamlit app
# st.title("2D Word Embeddings Visualization")  # Removed the title
placeholder = st.empty()

# Create the initial scatterplot using the function
fig = create_scatterplot_with_arrows(data)

placeholder.plotly_chart(fig, use_container_width=True)

# User input to add words
if ADD_WORDS:
    st.sidebar.header("Add Words")
    word_to_add = st.sidebar.text_input("Enter a word to add:")
    add_button = st.sidebar.button("Add Word")
    reset_button = st.sidebar.button("Reset")


# Initialize 'added_words' in session state or if reset button to clear 'added_words'
if 'added_words' not in st.session_state or reset_button:
    st.session_state.added_words = []

data = pd.concat([data, pd.DataFrame(st.session_state.added_words)], ignore_index=True)

# Randomly generate coordinates for the added word
if ADD_WORDS and add_button and word_to_add:
    if word_to_add in hidden_data['word'].values:
        x = hidden_data[hidden_data['word'] == word_to_add]['x'].values[0]
        y = hidden_data[hidden_data['word'] == word_to_add]['y'].values[0]
        st.session_state.added_words.append({'word': word_to_add, 'x': x, 'y': y, 'cluster': 'جدید'})
        
        # Update the scatterplot using the function
        data = pd.concat([data, pd.DataFrame([st.session_state.added_words[-1]])], ignore_index=True)
        fig = create_scatterplot_with_arrows(data)
        placeholder.plotly_chart(fig, use_container_width=True)
    else:
        st.sidebar.warning(f"The word '{word_to_add}' does not exist in the vocabulary.")


# Dropdown menu to select a relation
if SHOW_RELATIONS:
    st.sidebar.header("Select a Relation")
    selected_relation = st.sidebar.selectbox("Choose a Relation", ['هیچ کدام'] + list(relationship_data.keys()))

    # Process and display the selected relation with arrows if it exists
    if selected_relation:
        relation_data = relationship_data.get(selected_relation, [])
        st.sidebar.subheader(f"Selected Relation: {selected_relation}")
        if relation_data:
            # Process and display the relation data with arrows
            fig = create_scatterplot_with_arrows(data, relation_data)
            placeholder.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No data available for the selected relation.")

# You can add more interactivity or analysis here as needed
