"""Create a Dash app within a Flask app."""
import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
from .layout import html_layout
from app.functions import generate_song_cluster_tables, generate_song_duration_box, generate_set_placement_graph, generate_song_frequency_graph, generate_over_time_graph, generate_table, get_date, generate_dow_graph
from dash.dependencies import Input, Output
import random
import dash_bootstrap_components as dbc

def create_dashboard(server):
    tracks = pd.read_csv('app/data/all_tracks_played')
    tracks = tracks[tracks.groupby('title').title.transform(len) > 25]

    #Create song and graph_type list
    songs = tracks['title'].unique()
    songs = sorted(songs)
    graph_types = ['Song Duration Scatter Plot', 'Song Duration Over Time', 'Set Placement Scatter Plot', 'Set Placement Over Time', 'Song Frequency Over Time', 'Song Clusters', 'Day of Week Distribution']



    #Initiate the dashboard
    dash_app = dash.Dash(server=server,
                         routes_pathname_prefix='/dashapp/',
                         external_stylesheets=[dbc.themes.BOOTSTRAP, 'static/style.css']
                         )

    #Pull in defaul html saved in layout.py
    dash_app.index_string = html_layout
    #Create overall layout
    dash_app.layout = html.Div([
            # Input window for dates and graph options.
            html.Div([dbc.Row([
                #Song Input
                dbc.Col(html.Div([
                    dcc.Dropdown(id='Song',
                        options=[{'label': i, 'value': i} for i in songs],
                        placeholder='The story of the...')],
                style={'width': '95%', 'display': 'inline-block', 'font-family': 'Arial'})),
                #Graph Choice
                dbc.Col(html.Button('Random', id='randomize', n_clicks=0, style={'width': '50%', 'display': 'inline-block', 'font-family': 'Arial', 'backgroundColor':'white', 'height':"40px"}),),
                dbc.Col(html.Div([
                    dcc.Dropdown(id='Graph-Type',
                                 options=[{'label': i, 'value': i} for i in graph_types],
                                 placeholder='Choose a graph...')],
                style={'width': '95%', 'display': 'inline-block', 'font-family': 'Arial'}))
                ,],
                    no_gutters=True)],
            style={'margin-left':'75px', 'margin-right':'75px','color': '#F15A50', 'text-align': 'center','backgroundColor':'#2C6E91',}),
            #Graph and helper text and table
            html.Div(children=[
                html.Div([dcc.Graph(id='graph')],
                         style={'width':'99%', 'display': 'inline-block', 'font-family': 'Arial'}),
                ],
            style={'width': '95%', 'display': 'inline-block', 'color': '#F15A50', 'text-align': 'center','backgroundColor':'#2C6E91'}),
            html.Div([html.P(id='hover-table')], style={'color': '#F15A50', 'text-align': 'center','backgroundColor':'#2C6E91', 'display': 'inline-block', 'min-height':'250px', 'verticalAlign':'center'})],
        style={'height':'100%','text-align': 'center','backgroundColor':'#2C6E91'})

    #Update tables and graphs every time a change is made
    @dash_app.callback(
        Output('graph', 'figure'),
        [Input('Song', 'value'),
        Input('Graph-Type', 'value')])
    def update_figure(song,graph_type):
        if graph_type == 'Song Clusters':
            figure = generate_song_cluster_tables(song)
        elif graph_type == 'Song Duration Scatter Plot':
            figure = generate_song_duration_box(song)
        elif graph_type == 'Set Placement Scatter Plot':
            figure = generate_set_placement_graph(song)
        elif graph_type == 'Song Frequency Over Time':
            figure = generate_song_frequency_graph(song)
        elif graph_type == 'Song Duration Over Time':
            figure = generate_over_time_graph(song, 'Dur')
        elif graph_type == 'Set Placement Over Time':
            figure = generate_over_time_graph(song, 'Place')
        elif graph_type == 'Day of Week Distribution':
            figure = generate_dow_graph(song)

        figure.update_layout(
            height=450,
            yaxis=dict(
                showgrid=True,
                gridwidth=1),
            margin=dict(l=40, r=40, t=40, b=40),
            paper_bgcolor="#2C6E91",
            font=dict(
                family="Arial, monospace",
                size=16,
                color='#F15A50'))
        if graph_type == 'Song Clusters':
            figure.update_layout(paper_bgcolor ='#e5ecf6')
        return figure


    #Update table every time a point is clicked or change to help test when the graph is changed
    @dash_app.callback(
        Output('hover-table', 'children'),
        [Input('graph', 'clickData'),
        Input('Song', 'value'),
        Input('Graph-Type', 'value')])
    def update_table(clickData, song, graph_type):
        if graph_type in ['Song Duration Scatter Plot', 'Song Duration Over Time', 'Set Placement Scatter Plot', 'Set Placement Over Time',]:
            print(clickData)
            if clickData != None:
                date_link_df = get_date(clickData, song, graph_type)
                return generate_table(date_link_df, graph_type)
            else:
                return 'Click on a point to see details and a link to listen.'
        elif graph_type in ['Song Frequency Over Time', 'Day of Week Distribution']:
            return "Hover over bars for more info"
        elif graph_type == 'Song Clusters':
            return "Never Played 'times' is times that song has been played without being played with the chosen song"

    #Randomly choose a song and graph combo
    @dash_app.callback(
        [Output('Song', 'value'),
        Output('Graph-Type','value')],
        [Input('randomize', 'n_clicks')])
    def randomize(n_clicks):
        if n_clicks > 0:
            random_song = random.choice(songs)
            random_choice = random.choice(graph_types)

        return random_song, random_choice

    return dash_app.server








