import json

import numpy as np
from dash import Dash, html, dcc, callback, Output, Input, State
import pandas as pd
import plotly.figure_factory as ff
import plotly.express as px
from group import Group

WORD = 'word'
CLUSTER = 'cluster'
X = 'x'
Y = 'y'

app = Dash(__name__)


def read_df():
    data = pd.read_csv('data.csv')
    with_cluster = data.loc[data[CLUSTER].notna()]
    return data, with_cluster


all_df, df = read_df()

added_words = set()


def format_added_words():
    words = list(added_words)
    words.sort()
    return list(map(lambda w: html.P(w), words))


def create_cluster_fig():
    points_fig = px.scatter(df, x=df[X], y=df[Y], color=CLUSTER, text=df.loc[:, WORD],
                            color_discrete_sequence=px.colors.qualitative.Plotly)
    points_fig.update_traces(textposition='top center',
                             textfont=dict(family="Gulzar", size=15, ))
    return points_fig


# main plot displaying clusters
cluster_fig = create_cluster_fig()


def load_group_pairs():
    with open('groups.json', encoding='utf-8') as f:
        return json.load(f)


# groups of vectors
# the key in this dict is the group name which is displayed on radio items
# the value is a list of pairs:
# first item in pair is the vectors start word and the second is the vector's end word
group_pairs = load_group_pairs()

# map of group names to their group objects
# is populated in setup()
groups = dict()


def get_word(word):
    return np.array(df.loc[df[WORD] == word, [X, Y]]).reshape(2)


def create_vector_fig(group_name, pairs, index):
    starts = np.stack([get_word(pair[0]) for pair in pairs])
    ends = np.stack([get_word(pair[1]) - get_word(pair[0]) for pair in pairs])

    # create a unique selector for this figure
    # this will be used in update_traces to hide or display the figure's trace
    custom_data = (group_name + '_fig',)
    selector = {'customdata': custom_data}

    fig = ff.create_quiver(starts[:, 0], starts[:, 1], ends[:, 0], ends[:, 1],
                           scale=1,
                           arrow_scale=0.075,
                           name=group_name,
                           angle=np.pi / 6,
                           line_width=1.75,
                           customdata=custom_data)
    fig.update_traces(line_color=px.colors.qualitative.Antique[-index - 1])
    return fig, selector


def only_show_vec_fig(name_to_display=None):
    for name, group in groups.items():
        visible = 'legendonly'
        if name and name == name_to_display:
            visible = True
        cluster_fig.update_traces(
            patch={'visible': visible}, selector=group.selector)


def setup():
    pass
    # i = 0
    # for group_name, pairs in group_pairs.items():
    #     vector_fig, selector = create_vector_fig(group_name, pairs, i)
    #     groups[group_name] = Group(group_name, pairs, selector)
    #     cluster_fig.add_traces(data=vector_fig.data)
    #     i += 1


@callback(
    Output('graph-content', 'figure'),
    Input('radios', 'value'),
)
def radio_btn_cb(value):
    only_show_vec_fig(value)
    return cluster_fig


@callback(
    Output('graph-content', 'figure', allow_duplicate=True),
    Output('input-error', 'children'),
    Output('added-words', 'children'),
    Input('add-btn', 'n_clicks'),
    State('input-on-add', 'value'),
    prevent_initial_call=True,
)
def add_btn_cb(_, word):
    if word in df[WORD].unique() or word in added_words:
        return cluster_fig, "already added", format_added_words()

    word_row = all_df.loc[all_df[WORD] == word]
    if word_row.empty:
        return cluster_fig, "not exists in dictionary", format_added_words()

    added_words.add(word)

    points_fig = px.scatter(word_row, x=word_row[X], y=word_row[Y], text=word_row.loc[:, WORD],
                            color_discrete_sequence=['grey'])
    points_fig.update_traces(textposition='top center',
                             textfont=dict(family="Gulzar", size=15, ))
    cluster_fig.add_traces(data=points_fig.data)

    return cluster_fig, "word added successfully", format_added_words()


@callback(
    Output('graph-content', 'figure', allow_duplicate=True),
    Output('added-words', 'children', allow_duplicate=True),
    Input('reset-btn', 'n_clicks'),
    prevent_initial_call=True,
)
def reset_btn_cb(_):
    # remove the last len(added_words) items from cluster_fig.data
    # this only works if the added words are the last items in the cluster_fig.data
    # which is currently the case, unless changed.

    data = list(cluster_fig.data)
    cluster_fig.data = data[0:len(data) - len(added_words)]
    added_words.clear()

    return cluster_fig, format_added_words()


if __name__ == '__main__':
    setup()
    app.layout = html.Div([
        html.H1(children='Word 2 Vec', style={'textAlign': 'center'}),
        dcc.Graph(id='graph-content', figure=cluster_fig),
        html.Center(
            children=[
                html.Span(
                    children=[
                        dcc.Input(id='input-on-add', type='text',
                                  placeholder='کلمه جدید وارد کنید'),
                        html.Button('افزودن', id='add-btn', n_clicks=0),
                    ],
                ),
                html.Div(
                    id='input-error',
                    children='',
                ),
                html.Div(
                    id='added-words',
                    children=[],
                ),
                html.Button('حذف کلمات افزوده شده',
                            id='reset-btn', n_clicks=0),
            ]
        ),
    ])
    app.run(debug=True)
