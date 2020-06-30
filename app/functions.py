import pandas as pd
import dash_table
import numpy as np
from plotly.subplots import make_subplots
from plotly import graph_objects as go

# Check graph orientation on phone
# Alias for table overflow
# Get link to open in new tab
# Add color change for closers


def generate_dow_graph(song):
    # distribution of phish shows for their full career
    dow_dist = [0.141,0.078,0.112,.120,.130,.208,.211]
    xticks = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']

    #import distribution of days of week for each song and change to list of values for graph
    dow_df = pd.read_csv('app/data/dow_dist_song')
    song_dow_df_only = dow_df[dow_df['title'] == song]
    song_dow_list = song_dow_df_only.values.tolist()
    song_dow_list = song_dow_list[0]
    song_dow_list.pop(0)

    #Create hover text to help explain graph better.
    hover_txt_song = []
    hover_txt_overall = []
    i = 0
    while i <= len(song_dow_list)-1:
        hover_txt_song.append(str(int(song_dow_list[i]*100)) + '% of the times ' + str(song) + ' was played it was on a ' + str(xticks[i]))
        hover_txt_overall.append(str(int(dow_dist[i]*100)) + '% of all Phish shows have been played on a ' + str(xticks[i]))
        i += 1

    #Create figure with two traces
    figure = go.Figure(
        data=go.Bar(x=xticks, y=song_dow_list, name='Song', marker_color='#F15A50', text=hover_txt_song, marker_line_color="#2C6E91",
                    marker_line_width=1.5, opacity=0.6))
    figure.add_trace(go.Scatter(x=xticks, y=dow_dist, mode='markers', text=hover_txt_overall, name='Overall',
                                marker=dict(color="#2C6E91", symbol='circle-open', opacity=0.8, line_width=3, size=8)))

    figure.update_layout(
            yaxis=dict(title='Percentage of Shows'),
            showlegend=True,
            legend=dict(x=0.43, y=1.25,
                        orientation='h',
                        bgcolor="white",
                        bordercolor="Black",
                        borderwidth=2))

    return figure

#Create box plot and scatter for individual songs
def generate_song_duration_box(song):
    track_length_combined = pd.read_csv('https://jroefive.github.io/track_length_combined')
    track_length_song = list(track_length_combined[track_length_combined['title']==song]['duration'].values)
    figure = go.Figure()
    figure.add_trace(go.Box(
        x=track_length_song,
        name=song,
        boxpoints='all',
        pointpos=0,
        boxmean='sd',
        jitter=1,
        orientation='h',
        marker=dict(color='#F15A50', symbol='circle-open', opacity=0.8, line_width=3),
        marker_size=8,
        line_color="#2C6E91"),
        )
    figure.update_layout(xaxis=dict(title='Song Duration in Minutes'))
    return figure

# Create box plot and scatter for set placement
def generate_set_placement_graph(song):
    tracks_graph = pd.read_csv('https://jroefive.github.io/set_placement_plot')
    track_placement = list(tracks_graph[tracks_graph['title']==song]['percentintoset'].values)
    figure = go.Figure()
    figure.add_trace(go.Box(
        x=track_placement,
        name=song,
        boxpoints='all',
        pointpos=0,
        boxmean='sd',
        jitter=1,
        orientation='h',
        marker=dict(color='#F15A50', symbol='circle-open', opacity=0.8, line_width=3),
        marker_size=8,
        line_color="#2C6E91"))

    figure.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=[1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5],
            ticktext=['Start Set 1', 'Mid Set 1', 'Start Set 2', 'Mid Set 2', 'Start Set 3', 'Mid Set 3',
                      'Start Encore', 'Mid Encore', 'End of Show']))
    figure.update_xaxes(range=[0.9, 5])

    return figure

# Generate tables for song clusters
def generate_song_cluster_tables(song):
    song_cluster_show_dict = np.load('app/data/song_cluster_show_dict.npy', allow_pickle = True).item()
    song_cluster_set_dict = np.load('app/data/song_cluster_set_dict.npy', allow_pickle = True).item()
    song_cluster_previous_dict = np.load('app/data/song_cluster_previous_dict.npy', allow_pickle = True).item()
    song_cluster_next_dict = np.load('app/data/song_cluster_next_dict.npy', allow_pickle = True).item()
    song_never_show_dict = np.load('app/data/song_never_show_dict.npy',allow_pickle = True).item()
    song_never_set_dict = np.load('app/data/song_never_set_dict.npy', allow_pickle = True).item()
    song_never_previous_dict = np.load('app/data/song_never_previous_dict.npy', allow_pickle = True).item()
    song_never_next_dict = np.load('app/data/song_never_next_dict.npy', allow_pickle = True).item()

    subplot_titles = ['Most Times Played - Same Show', 'Most Times Played - Same Set', 'Most Times Played - Previous Song', 'Most Times Played - Next Song', 'Never Played - Same Show', 'Never Played - Same Set', 'Never Played - Previous Song', 'Never Played - Next Song']
    figure = make_subplots(rows=2, cols=4, specs=[[{"type": "table"}, {"type": "table"}, {"type": "table"}, {"type": "table"}], [{"type": "table"}, {"type": "table"}, {"type": "table"}, {"type": "table"}]],
                           subplot_titles=subplot_titles, vertical_spacing=0.07, horizontal_spacing=0.02)
    figure.update_layout(paper_bgcolor="#2C6E91", plot_bgcolor="#2C6E91", scene_bgcolor="#2C6E91", margin=dict(l=10, r=10, t=10, b=10), height = 400)

    figure.add_trace(generate_song_cluster_table(song_cluster_show_dict[song]), row=1, col=1)
    figure.add_trace(generate_song_cluster_table(song_cluster_set_dict[song]), row=1, col=2)
    figure.add_trace(generate_song_cluster_table(song_cluster_previous_dict[song]), row=1, col=3)
    figure.add_trace(generate_song_cluster_table(song_cluster_next_dict[song]), row=1, col=4)
    figure.add_trace(generate_song_cluster_table(song_never_show_dict[song]), row=2, col=1)
    figure.add_trace(generate_song_cluster_table(song_never_set_dict[song]), row=2, col=2)
    figure.add_trace(generate_song_cluster_table(song_never_previous_dict[song]), row=2, col=3)
    figure.add_trace(generate_song_cluster_table(song_never_next_dict[song]), row=2, col=4)

    return figure

# Bar graph for song frequency changes over time
def generate_song_frequency_graph(song):
    # Get total times played for the song for every 100 shows
    song_freq_df = pd.read_csv('app/data/song frequency over time.csv')
    track_length_combined = pd.read_csv('https://jroefive.github.io/track_length_combined')
    debut_id = int(song_freq_df[song_freq_df['title']==song]['order_id'].values)
    song_freq_df_only = song_freq_df[song_freq_df['title'] == song]
    song_freq_list = song_freq_df_only.values.tolist()
    song_freq_list = song_freq_list[0]

    #drop off the leading values
    song_freq_list.pop(2)
    song_freq_list.pop(1)
    song_freq_list.pop(0)

    #Shorten list for songs that haven't been played for Phish's full career
    while song_freq_list[-1]==0:
        song_freq_list.pop(-1)

    #Create xtick marks based on the id of the debut show and add 100 each time
    intervals = len(song_freq_list)
    xticks = [debut_id]
    for i in range(1,intervals):
        xticks.append(debut_id + 100*i)

    #Create a list of dates based on the xticks above
    xdates_df = track_length_combined[track_length_combined['order_id'].isin(xticks)].copy()
    xdates = list(xdates_df['date'].unique())


    #Create hover text to explain bars better
    i = 0
    xranges=[]
    while i < len(xdates) - 1:
        xranges.append(str(song) + str(" was played ") + str(song_freq_list[i]) + str(' times in the 100 shows between ') + str(xdates[i])+ str(' and ') + str(xdates[i+1]))
        i += 1

    #Extrapolate to percentage of last group of shows since this is almost never 100 shows
    final_show_gap = 1628 - xticks[-1]
    last_bar_replace = int((song_freq_list[-1]/final_show_gap)*100)
    xranges.append(str(song) + str(" was played ") + str(song_freq_list[i]) + str(' times in the ') + str(final_show_gap) + str(' shows between ') + str(xdates[i]) + str(' and 2/23/20.  Bar shows ') + str(last_bar_replace) + str(', the percentage of times played in the last ') + str(final_show_gap) + str(' shows.'))
    song_freq_list[-1] = last_bar_replace

    #Draw figure
    figure = go.Figure(data=go.Bar(x=xticks,y=song_freq_list,text=xranges, marker_color='#F15A50', marker_line_color="#2C6E91",
                      marker_line_width=1.5, opacity=0.6))
    figure.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=xticks,
            ticktext=xdates),
        yaxis=dict(title='Percentage of Shows Played'))
    figure.update_xaxes(tickangle=90)

    return figure

#Function to pull values in for the duration and placement over time graphs
def get_values_for_graph(song, type, graph_choice):
    if graph_choice == 'Dur':
        if type == 'Avg':
            song_df = pd.read_csv('app/data/song_dur_avg_change')
        elif type == 'Max':
            song_df = pd.read_csv('app/data/song_dur_max_change')
        elif type == 'Min':
            song_df = pd.read_csv('app/data/song_dur_min_changes')
        elif type == 'Stdv':
            song_df = pd.read_csv('app/data/song_dur_stdv_change')
    elif graph_choice == 'Place':
        if type == 'Avg':
            song_df = pd.read_csv('app/data/setplace_avg_change')
        elif type == 'Max':
            song_df = pd.read_csv('app/data/setplace_max_change')
        elif type == 'Min':
            song_df = pd.read_csv('app/data/setplace_min_change')
        elif type == 'Stdv':
            song_df = pd.read_csv('app/data/setplace_std_change')
    song_df = song_df.fillna(0)
    song_df_only = song_df[song_df['title'] == song]
    song_val_list = song_df_only.values.tolist()
    song_val_list = song_val_list[0]
    song_val_list.pop(2)
    song_val_list.pop(1)
    song_val_list.pop(0)
    while song_val_list[-1] == 0:
        song_val_list.pop(-1)

    return song_val_list

# Get tickvalues and dates for all over time graphs
def xtick_lists(song_val_list, song):
    intervals = len(song_val_list)
    debut_id = get_debut_data(song)
    xticks = [debut_id]
    for i in range(1,intervals):
        xticks.append(debut_id + 100*i)
    track_length_combined = pd.read_csv('https://jroefive.github.io/track_length_combined')
    xdates_df = track_length_combined[track_length_combined['order_id'].isin(xticks)].copy()
    xdates = list(xdates_df['date'].unique())
    return xticks, xdates

# Pull out debut id for xticks
def get_debut_data(song):
    song_df = pd.read_csv('app/data/song_dur_avg_change')
    debut_id = int(song_df[song_df['title'] == song]['order_id'].values)
    return debut_id

# Generate hover text depending on the type of graph and trace
def get_hover_text(song, song_val_list, xdates, xticks, type, graph_choice):
    i = 0
    xranges=[]
    final_show_gap = 1628 - xticks[-1]

    if graph_choice == 'Dur':
        if type == 'Avg':
            while i < len(xdates) - 1:
                xranges.append(str(song) + str(" was an average of ") + str(song_val_list[i]) + str(' minutes long in the 100 shows between ') + str(xdates[i])+ str(' and ') + str(xdates[i+1]))
                i += 1
            xranges.append(str(song) + str(" was an average of ") + str(song_val_list[i]) + str(' minutes long in the ') + str(final_show_gap) + str(' shows between ') + str(xdates[i]) + str(' and 2/23/20.'))
        elif type == 'Max':
            while i < len(xdates) - 1:
                xranges.append(str('The longest ') + str(song) + str(" was ") + str(song_val_list[i]) + str(' minutes long in the 100 shows between ') + str(xdates[i])+ str(' and ') + str(xdates[i+1]))
                i += 1
            xranges.append(str('The longest ') + str(song) + str(" was ") + str(song_val_list[i]) + str(' minutes long in the ') + str(final_show_gap) + str(' shows between ') + str(xdates[i]) + str(' and 2/23/20.'))
        elif type == 'Min':
            while i < len(xdates) - 1:
                xranges.append(str('The shortest ') + str(song) + str(" was ") + str(song_val_list[i]) + str(' minutes long in the 100 shows between ') + str(xdates[i])+ str(' and ') + str(xdates[i+1]))
                i += 1
            xranges.append(str('The shortest ') + str(song) + str(" was ") + str(song_val_list[i]) + str(' minutes long in the ') + str(final_show_gap) + str(' shows between ') + str(xdates[i]) + str(' and 2/23/20.'))
        elif type == 'Std':
            while i < len(xdates) - 1:
                xranges.append(str('The standard deviation of the duration of ') + str(song) + str(" was ") + str(song_val_list[i]) + str(
                    ' during the 100 shows between ') + str(xdates[i]) + str(' and ') + str(xdates[i + 1]))
                i += 1
            #Sometimes the last stdv value is missing because the song was only played once in that gap, this checks to make sure there are the same number of values in the stddev list
            if len(xdates) == len(song_val_list):
                xranges.append(str('The standard deviation of the duration of ') + str(song) + str(" was ") + str(song_val_list[-1]) + str(' during in the ') + str(final_show_gap) + str(' shows between ') + str(xdates[-1]) + str(' and 2/23/20.'))
    if graph_choice == 'Place':
        if type == 'Avg':
            while i < len(xdates) - 1:
                xranges.append(str(song) + str(" was played at an average placement of ") + str(song_val_list[i]) + str(' during the 100 shows between ') + str(xdates[i])+ str(' and ') + str(xdates[i+1]))
                i += 1
            xranges.append(str(song) + str(" was played at an average placement of ") + str(song_val_list[i]) + str(' during the ') + str(final_show_gap) + str(' shows between ') + str(xdates[i]) + str(' and 2/23/20.'))
        elif type == 'Max':
            while i < len(xdates) - 1:
                xranges.append(str('The latest placement of ') + str(song) + str(" was ") + str(song_val_list[i]) + str(' during the 100 shows between ') + str(xdates[i])+ str(' and ') + str(xdates[i+1]))
                i += 1
            xranges.append(str('The latest placement of ') + str(song) + str(" was ") + str(song_val_list[i]) + str(' during the the ') + str(final_show_gap) + str(' shows between ') + str(xdates[i]) + str(' and 2/23/20.'))
        elif type == 'Min':
            while i < len(xdates) - 1:
                xranges.append(str('The earliest placement of ') + str(song) + str(" was ") + str(song_val_list[i]) + str(' during the 100 shows between ') + str(xdates[i])+ str(' and ') + str(xdates[i+1]))
                i += 1
            xranges.append(str('The earliest placement of ') + str(song) + str(" was ") + str(song_val_list[i]) + str(' during the ') + str(final_show_gap) + str(' shows between ') + str(xdates[i]) + str(' and 2/23/20.'))
        elif type == 'Std':
            while i < len(xdates) - 1:
                xranges.append(str('The standard deviation of the placement of ') + str(song) + str(" was ") + str(song_val_list[i]) + str(
                    ' during the 100 shows between ') + str(xdates[i]) + str(' and ') + str(xdates[i + 1]))
                i += 1
            if len(xdates) == len(song_val_list):
                xranges.append(str('The standard deviation of the placement of ') + str(song) + str(" was ") + str(song_val_list[-1]) + str(' during in the ') + str(final_show_gap) + str(' shows between ') + str(xdates[i]) + str(' and 2/23/20.'))
    return xranges

#Create graphs by calling functions above
def generate_over_time_graph(song, graph_choice):
    song_avg_list = get_values_for_graph(song, 'Avg', graph_choice)
    xticks, xdates = xtick_lists(song_avg_list, song)
    song_max_list = get_values_for_graph(song, 'Max', graph_choice)
    song_min_list = get_values_for_graph(song, 'Min', graph_choice)
    song_stdv_list = get_values_for_graph(song, 'Stdv', graph_choice)

    # Add 0s on the end of the stdv list if the last values are 0.
    if len(xticks) != len(song_stdv_list):
        adj = len(xticks) - len(song_stdv_list)
        i = 1
        while i <= adj:
            song_stdv_list.append(0)
            i += 1

    hov_text_avg = get_hover_text(song, song_avg_list, xdates, xticks, "Avg", graph_choice)
    hov_text_max = get_hover_text(song, song_max_list, xdates, xticks, "Max", graph_choice)
    hov_text_min = get_hover_text(song, song_min_list, xdates, xticks, "Min", graph_choice)
    hov_text_std = get_hover_text(song, song_stdv_list, xdates, xticks, "Std", graph_choice)
    
    figure = go.Figure(data=go.Scatter(x=xticks,y=song_avg_list,text=hov_text_avg, name='Average Length', mode='lines+markers', marker=dict(color="#2C6E91", symbol='circle-open', opacity=0.8, line_width=3, size=8)))
    figure.add_trace(go.Scatter(x=xticks, y = song_max_list, text=hov_text_max,mode='markers', name='Max', marker=dict(color='#F15A50', symbol='circle-open', opacity=0.8, line_width=3, size=8)))
    figure.add_trace(go.Scatter(x=xticks, y=song_min_list, text=hov_text_min,mode='markers', name='Min', marker=dict(color='#F15A50', symbol='circle-open', opacity=0.8, line_width=3, size=8)))
    figure.add_trace(go.Bar(x=xticks, y=song_stdv_list, text=hov_text_std, name='Standard Deviation', marker_color='#F15A50', marker_line_color="#2C6E91",
                      marker_line_width=1.5, opacity=0.3))
    figure.update_xaxes(tickangle=90)
    figure.update_layout(
        showlegend=True,
        legend=dict(x=0.3, y=1.25,
                    bgcolor="white",
                    bordercolor="Black",
                    borderwidth=2),
        legend_orientation="h",
        xaxis=dict(
            tickmode='array',
            tickvals=xticks,
            ticktext=xdates))
    if graph_choice == 'Place':
        figure.update_layout(
            yaxis=dict(
                tickmode='array',
                tickvals=[1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5],
                ticktext=['Start Set 1', 'Mid Set 1', 'Start Set 2', 'Mid Set 2', 'Start Set 3', 'Mid Set 3',
                          'Start Encore', 'Mid Encore', 'End of Show']))
        figure.update_yaxes(range=[0, 5])

    if graph_choice == 'Dur':
        figure.update_layout(
            yaxis=dict(title='Average Song Duration in Minutes'))
    return figure

#Function to create tables for song cluster page
def generate_song_cluster_table(data):
    return go.Table(
            columnwidth=[3,1],
            header=dict(
                values=["Song", "Times"],
                font=dict(size=14, family="Arial, monospace"),
                line_color='#2C6E91',
                align="left",
                height=20
            ),
            cells=dict(
                values=[[i[0] for i in data], [i[1] for i in data]],
                align="left", font=dict(size=14, family="Arial, monospace"),
                line_color='#2C6E91',
                height=25)
        )

#Pulls out all shows that match the points that were clicked on
def get_date(clickData, song, graph_type):
    #Set some default values
    trace = 5
    val = 0
    df1 = pd.DataFrame()

    #Grab the clickdata differently based on the type of graph
    if graph_type == 'Song Duration Scatter Plot' or graph_type == 'Set Placement Scatter Plot':
        val = clickData['points'][0]['x']
        show_id = 0
    elif graph_type == 'Song Duration Over Time' or graph_type == 'Set Placement Over Time':
        val = clickData['points'][0]['y']
        show_id = clickData['points'][0]['x']
        trace = clickData['points'][0]['curveNumber']

    #Pull only rows from the df that fit criteria
    if graph_type == 'Song Duration Scatter Plot' or graph_type == 'Song Duration Over Time':
        all_tracks = pd.read_csv('https://jroefive.github.io/track_length_combined')
        df = all_tracks[(all_tracks['title'] == song) & (all_tracks['duration'] == val)]
        
        order_ids = list(df['order_id'].values)
        df['Part of Segue?'] = ""
        song_count = 1
        for i in order_ids:
            other_show_tracks = all_tracks[all_tracks['order_id']==i]
            song_count_df = other_show_tracks[other_show_tracks['title']==song]
            if song_count_df.shape[0] > 1:
                song_count = 2
                df.loc[df['order_id']==i, 'Part of Segue?'] = 'Yes'

        display_cols = ['title', 'date', 'set', 'position', 'duration', 'order_id', 'Part of Segue?']
        df1 = df[display_cols]

        df1['min'] = df1['duration'].astype(int)
        df1['minutes'] = df1['min'].astype(str)
        df1['part'] = df1['duration']%1
        df1['sec'] = df1['part']*60
        df1['secs'] = df1['sec'].astype(int)
        df1['seconds'] = df1['secs'].astype(str)

        for i in range(0,10):
            df1 = df1.replace({'seconds': str(i)}, '0' + str(i))
            
        df1['Song Duration'] = df1['minutes'] + ':' + df1['seconds']

    elif graph_type == 'Set Placement Scatter Plot' or graph_type == 'Set Placement Over Time':
        all_tracks = pd.read_csv('https://jroefive.github.io/set_placement_plot')
        df = all_tracks[(all_tracks['title']==song) & (all_tracks['percentintoset']==val)]
        df['Part of Segue?'] = ""
        order_ids = list(df['order_id'].values)
        song_count = 1
        for i in order_ids:
            other_show_tracks = all_tracks[all_tracks['order_id']==i]
            song_count_df = other_show_tracks[other_show_tracks['title']==song]
            if song_count_df.shape[0] > 1:
                song_count = 2
                df.loc[df['order_id']==i, 'Part of Segue?'] = 'Yes'

        display_cols = ['title', 'date', 'percentintoset', 'order_id', 'Part of Segue?']
        df1 = df[display_cols]

        #Adjust the percentintoset column to better explain what it means in the table
        df1['set'] = df['percentintoset'].astype(int)
        df1['percent'] = df['percentintoset']%1*100
        df1['percent'] = df1['percent'].astype(int)
        df1['percent'] = df1['percent'].astype(str)
        df1 = df1.replace({'set': 4}, 'enc')
        df1['Set Placement'] = df1['percent'] + '% into '
        df1 = df1.replace({'Set Placement': '0% into '}, 'Start of')

    #For the over time graphs, only display the shows in the 100 show range that was chosen
    if graph_type == 'Set Placement Over Time' or graph_type == 'Song Duration Over Time':
        if trace == 1 or trace == 2:
            df1 = df1[(df1['order_id'] >= show_id) & (df1['order_id'] < (show_id + 100))]
            df1 = df1.drop(['order_id'], axis=1)
    elif graph_type == 'Set Placement Scatter Plot' or graph_type == 'Song Duration Scatter Plot':
        df1 = df1.drop(['order_id'], axis=1)

    #Create a link column in markdown language so that it shows up as a link
    slugs_df = pd.read_csv('app/data/slugs')
    slug = slugs_df[slugs_df['title'] == song]['slug'].values
    df1['slug'] = slug[0]
    df1['Link'] = '[Link](https://phish.in/' + df1['date'] + '/' + df1['slug'] + ')'

    #Pull out only the columns for display
    if graph_type == 'Song Duration Scatter Plot' or graph_type == 'Song Duration Over Time':
        if song_count > 1:
            final_display_cols = ['date','set','position','Song Duration','Part of Segue?', 'Link']
        else:
            final_display_cols = ['date','set','position','Song Duration', 'Link']
    elif graph_type == 'Set Placement Scatter Plot' or graph_type == 'Set Placement Over Time':
        if song_count > 1:
            final_display_cols = ['date', 'Set Placement', 'set', 'Part of Segue?', 'Link']
        else:
            final_display_cols = ['date', 'Set Placement', 'set', 'Link']


    df1 = df1[final_display_cols]
    return df1

#Generate click table
def generate_table(df, graph_type):
    if graph_type == 'Song Clusters':
        df = pd.DataFrame()

    if df.empty:
        return 'Click on a point to see details and a link to listen.'

    return dash_table.DataTable(
        data=df.to_dict('records'),
        style_header={'color':"#2C6E91",'fontWeight': 'bold', 'fontSize':'26'},
        style_data={
        'whiteSpace': 'normal'},
        columns=[{'id': c, 'name': c, "presentation": "markdown"} for c in df.columns],
        style_cell={'textAlign':'center', 'width': '50px', 'padding':'25px', 'backgroundColor': '#e5ecf6'},
        style_data_conditional=[
            {
                'if': {
                    'column_id': 'Link',
                },
                'fontWeight': 'bold',
                'padding':'15px'
            },
            {
                'if': {
                    'column_id': 'date',
                },
                'fontWeight': 'bold',
                'width': '130px',
                'padding':'20px'
            },
        ],
        style_as_list_view=True,)