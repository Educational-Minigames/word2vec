import plotly.express as px
import streamlit as st
import pandas as pd
import json

PLOT_HEIGHT = 600

# Configure Streamlit to be in wide mode and remove the title
st.set_page_config(layout="wide")

config = st.experimental_get_query_params()
ADD_WORDS = (config.get('add_words', 'false')) != 'false'
SHOW_RELATIONS = (config.get('show_relations', 'false')) != 'false'
SHOW_COLORS = (config.get('show_colors', 'false')) != 'false'
config = {'modeBarButtonsToRemove':
          ['toImage',
           'lasso2d',
           'zoom2d',
           'select2d',
           'autoScale2d',
           ],
          'displaylogo': False,
          }


# Function to create and return the scatterplot figure with arrows for a selected relation
def create_scatterplot_with_arrows(data, relation_data=[]):
    if SHOW_COLORS:
        fig = px.scatter(data, x="x", y="y", text="word", color="cluster")
    else:
        fig = px.scatter(data, x="x", y="y", text="word")
    fig.update_traces(
        marker=dict(size=7),
        textfont=dict(size=16),
        textposition='top center',
        hoverinfo='x+y+text'
    )

    # Add arrows for each word pair in the selected relation
    for pair in relation_data:
        word1, word2 = pair
        x1, y1 = data[data['word'] ==
                      word1]['x'].values[0], data[data['word'] == word1]['y'].values[0]
        x2, y2 = data[data['word'] ==
                      word2]['x'].values[0], data[data['word'] == word2]['y'].values[0]

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
        margin={"r": 0, "t": 25, "l": 0, "b": 0},
        height=PLOT_HEIGHT,
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
    )

    return fig


# Load the data from the CSV file
raw_data = pd.read_csv("data.csv")

# Load relationship data from the "groups.json" file
with open("groups.json", "r", encoding="utf-8") as json_file:
    relationship_data = json.load(json_file)

# Split the DataFrame into 'data' and 'hidden_data' based on NaN values in the 'cluster' column
hidden_data = raw_data[raw_data['cluster'].isna()]
plot_data = raw_data.dropna(subset=['cluster'])
rtl_css = """
body, h1, h2, h3, p, label, span, div {
    direction: rtl;
}

@font-face{
    font-family: "Anjoman";
    src: url("https://db.onlinewebfonts.com/t/f6886c4078ba029be14b7d1053f961b5.eot");
    src: url("https://db.onlinewebfonts.com/t/f6886c4078ba029be14b7d1053f961b5.eot?#iefix")format("embedded-opentype"),
        url("https://db.onlinewebfonts.com/t/f6886c4078ba029be14b7d1053f961b5.woff")format("woff"),
        url("https://db.onlinewebfonts.com/t/f6886c4078ba029be14b7d1053f961b5.woff2")format("woff2"),
        url("https://db.onlinewebfonts.com/t/f6886c4078ba029be14b7d1053f961b5.ttf")format("truetype"),
        url("https://db.onlinewebfonts.com/t/f6886c4078ba029be14b7d1053f961b5.svg#Anjoman")format("svg");
    font-weight:normal;
    font-style:normal;
    font-display:swap;
}

* {
    font-family: Anjoman !important;
}

.legendtoggle {
    stroke: black !important;
    stroke-width: 1px !important;
    rx: 10px !important;
}

.legendtext {
    transform: translateX(-8px);
}

.layers {
    transform: scale(2) translateX(-14px);
}

.scrollbox {
    clip-path: none !important;
}

.scrollbox > :nth-child(3) {
    transform: translateY(6px) !important;
}

.scrollbox > :nth-child(4) {
    transform: translateY(12px) !important;
}

.scrollbox > :nth-child(5) {
    transform: translateY(18px) !important;
}

.scrollbox > :nth-child(6) {
    transform: translateY(24px) !important;
}

.scrollbox > :nth-child(7) {
    transform: translateY(30px) !important;
}

.scrollbox > :nth-child(8) {
    transform: translateY(36px) !important;
}

.scrollbox > :nth-child(9) {
    transform: translateY(42px) !important;
}

.scrollbox > :nth-child(10) {
    transform: translateY(48px) !important;
}

.scrollbox > :nth-child(11) {
    transform: translateY(54px) !important;
}

/* for hiding textfield helper text */
.st-emotion-cache-1li7dat {
    display: none !important;
}
"""

# Apply the custom CSS
st.markdown(f'<style>{rtl_css}</style>', unsafe_allow_html=True)

hide_streamlit_style = """
<style>
footer {visibility: hidden;}
header {visibility: hidden;}
</style>"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

hide_hint_css = """
<style>
.css-1umhob9-InputContainer .stTextInput {
    caret-color: transparent;
}
.css-1umhob9-InputContainer .stTextInput::placeholder {
    color: transparent;
}
</style>
"""

# Display the custom CSS
st.markdown(hide_hint_css, unsafe_allow_html=True)
# Create a Streamlit app
# st.title("2D Word Embeddings Visualization")  # Removed the title
placeholder = None

# Create the initial scatterplot using the function
# fig = create_scatterplot_with_arrows(data)

# placeholder.plotly_chart(fig, use_container_width=True)

# User input to add words

if ADD_WORDS:
    st.sidebar.header("کلمه جدید")
    with st.form("my-form"):
        word_to_add = st.sidebar.text_input("کلمه جدید وارد کنید:")
        add_button = st.sidebar.button("اضافه کردن کلمه")

    reset_button = st.sidebar.button("حذف کلمات جدید")

    # Initialize 'added_words' in session state or if reset button to clear 'added_words'
    if 'added_words' not in st.session_state or reset_button:
        st.session_state.added_words = []

    # Randomly generate coordinates for the added word
    if add_button and word_to_add:
        if word_to_add in plot_data['word'].values or word_to_add in [data_point['word'] for data_point in st.session_state.added_words]:
            st.sidebar.warning(f"کلمه '{word_to_add}' قبلا اضافه شده.")
        elif word_to_add in hidden_data['word'].values:
            x = hidden_data[hidden_data['word'] == word_to_add]['x'].values[0]
            y = hidden_data[hidden_data['word'] == word_to_add]['y'].values[0]
            st.session_state.added_words.append(
                {'word': word_to_add, 'x': x, 'y': y, 'cluster': 'جدید'})
        else:
            st.sidebar.warning(f"کلمه '{word_to_add}' در لغت‌نامه‌ نیست.")
    plot_data = pd.concat([plot_data, pd.DataFrame(
        st.session_state.added_words)], ignore_index=True)
else:
    plot_data = plot_data

# Dropdown menu to select a relation
if SHOW_RELATIONS:
    st.sidebar.header("انتخاب ارتباط")
    selected_relation = st.sidebar.selectbox(
        "یک ارتباط انتخاب کنید.", ['هیچ کدام'] + list(relationship_data.keys()))

    # Process and display the selected relation with arrows if it exists
    if selected_relation:
        relation_data = relationship_data.get(selected_relation, [])
        st.sidebar.subheader(f"ارتباط انتخابی شما: {selected_relation}")
else:
    relation_data = []

fig = create_scatterplot_with_arrows(plot_data, relation_data)
placeholder = st.empty()
placeholder.plotly_chart(fig, use_container_width=True, config=config)
# You can add more interactivity or analysis here as needed
