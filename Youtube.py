from dash import Dash, dash_table, dcc, html, callback, clientside_callback
import dash_bootstrap_components as dbc
from dash.dependencies import State, Input, Output
import pandas as pd
import numpy as np

from googleapiclient import discovery

api_service_name= "youtube"
api_version= "v3"
client_secrets_file= "YOUR_CLIENT_SECRET_FILE.json"
key= '<your secret key>'
youtube = discovery.build(
        api_service_name, api_version, developerKey= key)

###

def Channel_get_gen_details(youtube, id):
    request= youtube.channels().list(
        part= 'snippet, contentDetails, statistics, topicDetails',
        id= id
    )
    response= request.execute()
    channel= {
        'title': response['items'][0]['snippet']['title'],
        'description': response['items'][0]['snippet']['description'],
        'customUrl': response['items'][0]['snippet']['customUrl'],
        'publishedAt': response['items'][0]['snippet']['publishedAt'],
        'thumbnails': response['items'][0]['snippet']['thumbnails']['default']['url'],
        # 'country': response['items'][0]['snippet']['country'],
        'viewCount': response['items'][0]['statistics']['viewCount'],
        'subscriberCount': response['items'][0]['statistics']['subscriberCount'],
        'videoCount': response['items'][0]['statistics']['videoCount'],
        'topicDetails': response['items'][0]['topicDetails']['topicCategories'],
    }
    return channel
def Channel_get_playlists(youtube, id):
    request = youtube.playlists().list(
        part= "snippet,contentDetails",
        channelId= id,
        maxResults=50
    )
    response= request.execute()
    playlist= []
    for i in range(len(response['items'])):
        list= {
            'title': response['items'][i]['snippet']['title'],
            # 'channelId': response['snippet']['channelId'],
            'id': response['items'][i]['id'],
            'description': response['items'][i]['snippet']['description']
            # 'thumbnails': response['items'][i]['snippet']['thumbnails']['default']['url'],
        }
        playlist.append(list)
    token= response.get('nextPageToken')

    while True:
        if token == None:
            break
        else:
            request = youtube.playlists().list(
                part= "snippet,contentDetails",
                channelId= id,
                maxResults=50,
                pageToken= token
            )
            response= request.execute()
            for i in range(len(response['items'])):
                list= {
                    'title': response['items'][i]['snippet']['title'],
                    # 'channelId': response['snippet']['channelId'],
                    'id': response['items'][i]['id'],
                    'description': response['items'][i]['snippet']['description']
                    # 'thumbnails': response['items'][i]['snippet']['thumbnails']['default']['url'],
                }
                playlist.append(list)
            token= response.get('nextPageToken')
    return playlist
def get_videos_from_playlist(youtube, id):
    request = youtube.playlistItems().list(
        part= "snippet,contentDetails",
        playlistId= id,
        maxResults= 50
    )
    response= request.execute()
    videos= []
    for i in range(len(response['items'])):
        det= {
            'idg': response['items'][i]['id'],
            'title': response['items'][i]['snippet']['title'],
            'description': response['items'][i]['snippet']['description'],
            # 'thumbnails': response['items'][i]['snippet']['thumbnails']['default']['url'],
            'videoId': response['items'][i]['contentDetails']['videoId']
            # 'videoPublishedAt': response['items'][i]['contentDetails']['videoPublishedAt']
        }
        videos.append(det)
    token= response.get('nextPageToken')
    while True:
        if token == None:
            break
        else:
            request = youtube.playlistItems().list(
                part= "snippet,contentDetails",
                playlistId= id,
                maxResults= 50,
                pageToken= token
            )
            response= request.execute()
            for i in range(len(response['items'])):
                det= {
                    'idg': response['items'][i]['id'],
                    'title': response['items'][i]['snippet']['title'],
                    'description': response['items'][i]['snippet']['description'],
                    # 'thumbnails': response['items'][i]['snippet']['thumbnails']['default']['url'],
                    'videoId': response['items'][i]['contentDetails']['videoId']
                    # 'videoPublishedAt': response['items'][i]['contentDetails']['videoPublishedAt']
                }
            token= response.get('nextPageToken')
    return videos
def video_gen_Details(youtube, id):
    request= youtube.videos().list(
        part= "snippet,contentDetails,statistics,topicDetails",
        id= id
    )
    response= request.execute()
    video= []

    for i in range(len(response['items'])):
        det= {
            'title': response['items'][i]['snippet']['title'],
            'tags': response['items'][i]['snippet']['tags'],
            'duration': response['items'][i]['contentDetails']['duration'],
            'regionRestriction': response['items'][i]['contentDetails']['regionRestriction']['allowed'],
            'viewCount': response['items'][i]['statistics']['viewCount'],
            'likeCount': response['items'][i]['statistics']['likeCount'],
            'favoriteCount': response['items'][i]['statistics']['favoriteCount'],
            'commentCount': response['items'][i]['statistics']['commentCount'],
            'topicDetails': response['items'][i]['topicDetails']['topicCategories']
        }
    video.append(det)
    return video
def video_get_comment_details(youtube, id):
    request= youtube.commentThreads().list(
        part= "snippet,replies",
        videoId= id,
        maxResults= 50
    )
    response= request.execute()
    items= response.get('items')
    video= []
    for i in range(len(response['items'])):
        try:
            det= {
                'id': response['items'][i]['snippet']['topLevelComment']['id'],
                'Original Text': response['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal'],
                'Author Name': response['items'][i]['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                'Author Profile Image URL': response['items'][i]['snippet']['topLevelComment']['snippet']['authorProfileImageUrl'],
                'Author Channel URL': response['items'][i]['snippet']['topLevelComment']['snippet']['authorChannelUrl'],
                'Author Channel ID': response['items'][i]['snippet']['topLevelComment']['snippet']['authorChannelUrl']['value'],
                'Published Date': response['items'][i]['snippet']['topLevelComment']['snippet']['publishedAt'],
                'Likes': response['items'][i]['snippet']['topLevelComment']['snippet']['likeCount']
            }
        except:
            det= {
                'id': response['items'][i]['snippet']['topLevelComment']['id'],
                'Original Text': response['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal'],
                'Author Name': response['items'][i]['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                'Author Profile Image URL': response['items'][i]['snippet']['topLevelComment']['snippet']['authorProfileImageUrl'],
                'Author Channel URL': response['items'][i]['snippet']['topLevelComment']['snippet']['authorChannelUrl'],
                'Author Channel ID': response['items'][i]['snippet']['topLevelComment']['snippet']['authorChannelUrl'],
                'Published Date': response['items'][i]['snippet']['topLevelComment']['snippet']['publishedAt'],
                'Likes': response['items'][i]['snippet']['topLevelComment']['snippet']['likeCount']
            }
        video.append(det)
    token= response.get('nextPageToken')
    while True:
        if token == None:
            break
        else:
            request= youtube.commentThreads().list(
                part= "snippet,replies",
                videoId= id,
                maxResults= 50,
                pageToken= token
            )
            response= request.execute()
            for i in range(len(response['items'])):
                try:
                    det= {
                        'id': response['items'][i]['snippet']['topLevelComment']['id'],
                        'Original Text': response['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal'],
                        'Author Name': response['items'][i]['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                        'Author Profile Image URL': response['items'][i]['snippet']['topLevelComment']['snippet']['authorProfileImageUrl'],
                        'Author Channel URL': response['items'][i]['snippet']['topLevelComment']['snippet']['authorChannelUrl'],
                        'Author Channel ID': response['items'][i]['snippet']['topLevelComment']['snippet']['authorChannelUrl']['value'],
                        'Published Date': response['items'][i]['snippet']['topLevelComment']['snippet']['publishedAt'],
                        'Likes': response['items'][i]['snippet']['topLevelComment']['snippet']['likeCount']
                    }
                except:
                    det= {
                        'id': response['items'][i]['snippet']['topLevelComment']['id'],
                        'Original Text': response['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal'],
                        'Author Name': response['items'][i]['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                        'Author Profile Image URL': response['items'][i]['snippet']['topLevelComment']['snippet']['authorProfileImageUrl'],
                        'Author Channel URL': response['items'][i]['snippet']['topLevelComment']['snippet']['authorChannelUrl'],
                        'Author Channel ID': response['items'][i]['snippet']['topLevelComment']['snippet']['authorChannelUrl'],
                        'Published Date': response['items'][i]['snippet']['topLevelComment']['snippet']['publishedAt'],
                        'Likes': response['items'][i]['snippet']['topLevelComment']['snippet']['likeCount']
                    }
                video.append(det)
            token= response.get('nextPageToken')
    return video
def initial_df(No= 16, value= 'Product name', title= 'Product Name'):
    cols = ([title])
    data = np.repeat(value, No)
    df = pd.DataFrame(data= data, columns= cols).reset_index().rename(columns= {'index': 'id'})
    df = df.reset_index().rename(columns= {'index': 'ID'})
    df['ID'] += 1
    return df

###      

ESPN_Channel_id= 'UCFmMw7yTuLTCuMhpZD5dVsg'
ESPN_Channel_gen_details = Channel_get_gen_details(youtube, ESPN_Channel_id)
ESPN_Channel_playlists= Channel_get_playlists(youtube, ESPN_Channel_id)
Channel_playlists_pd= pd.DataFrame(ESPN_Channel_playlists)
ESPN_Playlist_videos= get_videos_from_playlist(youtube, 'PLTRckBbIqcx1TF37DDsNbapSVg3zgL6SL')
Playlists_videos_pd= pd.DataFrame(ESPN_Playlist_videos)
ESPN_comments= video_get_comment_details(youtube, 'TDtz7RdrMAA')

###

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME], suppress_callback_exceptions=True)

inputrow= dbc.Row(
    dbc.Col([
        html.H6("Input a channel id: ", className= 'pt-2 pe-2'),
        dcc.Input(id= 'input_submit', type= 'text', placeholder= "Submit a tag", className= 'my-1'),
        html.Button('Submit', id='submit-val', n_clicks=0, className= 'my-1'),
    ], style= dict(display='flex', justifyContent='center', backgroundColor= 'white')), class_name= 'mx-3 pt-2',
)
first_row= dbc.Row([
    dbc.Col([], id= 'row-1 col-1',
            align= 'center', style={"width": "49.68%", "margin-right": "8px", 'backgroundColor': 'white', 'height': '30vh', 'overflowY': 'auto'}, width= 6),
    # dbc.Col([], id= 'row-1 col-2',
    #         align= 'center', class_name= 'mx-2', style= dict(justifyContent='center', backgroundColor= 'white')),
    dbc.Col([], id= 'row-1 col-2',
            align= 'center', style={"width": "49.68%", "margin-right": "0",'backgroundColor': 'white', 'height': '30vh', 'overflowY': 'auto'}, width= 6)
], class_name= 'my-1 mx-3', style= {'display': 'flex'})
second_row = dbc.Row([
    dbc.Col([
        dbc.Row(html.H6('Choose a playlist', style= {'display': 'flex', 'justifyContent': 'center'})),
        dbc.Row(dcc.Dropdown([], id= 'dropdown_playlist')),
        dbc.Row(html.Div(dash_table.DataTable(
            data= [],
            id= 'datatable_videos'
        )))
    ], id= 'row-3 col-1', 
    style={"width": "32.4%", "margin-right": "8px", "max-width": "100%", 'backgroundColor': 'white', 'flex-grow': 0, 'height': '60vh'}),
    dbc.Col([
        dbc.Row(html.H6('The comments and its details can be found in the following table')),
        dbc.Row(html.Div(dash_table.DataTable(
            data= [],
            id= 'datatable_comments'
        )))
    ], id= 'row-3 col-2',
    # style={"flex-basis": "66.4%", "margin-right": "0", 'backgroundColor': 'white', 'flex-grow': 0}),
    style={"width": "66.925%", "margin-right": "0", 'backgroundColor': 'white', 'flex-grow': 0, 'height': '60vh'}),
], class_name= 'mt-1 mx-3 pb-2')

app.layout= dbc.Container([
    dbc.Col([  
            # title,
            inputrow,
            first_row,
            second_row, 
            # third_row
        ])    
], style= dict(backgroundColor= 'rgb(240,240,240)'), fluid= True)

@callback(
    Output('row-1 col-1', 'children'), Output('row-1 col-2', 'children'), Output('dropdown_playlist', 'options'), 
    Input('submit-val', 'n_clicks'),
    State('input_submit', 'value')
)
def Update_gen_values(n_clicks, value):
    if n_clicks > 0:
        Channel_gen_details= Channel_get_gen_details(youtube, value)
        a= []
        for b in Channel_gen_details['topicDetails']:
            det= {
                'element': b.split('/')[-1],
                'url': b
            } 
            a.append(det)
        rows= []
        for i in a:
            row= dbc.Row(html.A(i['element'], href= i['url'], style={"margin-bottom": "-1px", 'justifyContent': 'center', 'display': 'flex'}))
            rows.append(row)
        one_first_child= dbc.Row([
            dbc.Col([
                dbc.Row(f'Topic details:', style= dict(display= 'flex', justifyContent= 'start'), class_name= 'ps-3'),
                dbc.Row(rows),
                dbc.Row(f'Creation date: {Channel_gen_details['publishedAt']}', style= dict(display= 'flex', justifyContent= 'center'), class_name= 'pt-3'),
                dbc.Row(f'Subscribers Count: {Channel_gen_details['subscriberCount']}', style= dict(display= 'flex', justifyContent= 'center')),
                dbc.Row(f'Video Count: {Channel_gen_details['videoCount']}', style= dict(display= 'flex', justifyContent= 'center')),
                dbc.Row(f'View Count: {Channel_gen_details['viewCount']}', style= dict(display= 'flex', justifyContent= 'center')),
            ], width= 7),
            dbc.Col([
                # dbc.Row(f'Country: {Channel_gen_details['country']}', style= dict(display= 'flex', justifyContent= 'center'), class_name= 'pt-3'),
                dbc.Row(html.Img(src= Channel_gen_details['thumbnails'], style= dict(height= '75%', width= '75%', justifyContent= 'center')), style={"display": "flex", "align-items": "center", "justify-content": "center"})
                ], width= 5)
        ])
        one_second_child= [
            dbc.Row(html.H5(f'{Channel_gen_details['title']}({Channel_gen_details['customUrl']})', style= dict(display= 'flex', justifyContent= 'center')), class_name= 'pt-2'),
            dbc.Row(html.P(Channel_gen_details['description']))
        ]
        playlists= []
        global Channel_playlists
        Channel_playlists= Channel_get_playlists(youtube, value)
        for i in Channel_playlists:
            playlists.append(i['title'])
        dropdown_playlist_options= playlists
    else:
        a= []
        for b in ESPN_Channel_gen_details['topicDetails']:
            det= {
                'element': b.split('/')[-1],
                'url': b
            } 
            a.append(det) 
        rows= []
        for i in a:
            row= dbc.Row(html.A(i['element'], href= i['url'], style={"margin-bottom": "5px", 'justifyContent': 'center', 'display': 'flex'}))
            rows.append(row)
        one_first_child= dbc.Row([
            dbc.Col([
                dbc.Row(f'Topic details:', style= dict(display= 'flex', justifyContent= 'start'), class_name= 'ps-3'),
                dbc.Row(rows),
                dbc.Row(f'Creation date: {ESPN_Channel_gen_details['publishedAt']}', style= dict(display= 'flex', justifyContent= 'center'), class_name= 'pt-3'),
                dbc.Row(f'Subscribers Count: {ESPN_Channel_gen_details['subscriberCount']}', style= dict(display= 'flex', justifyContent= 'center')),
                dbc.Row(f'Video Count: {ESPN_Channel_gen_details['videoCount']}', style= dict(display= 'flex', justifyContent= 'center')),
                dbc.Row(f'View Count: {ESPN_Channel_gen_details['viewCount']}', style= dict(display= 'flex', justifyContent= 'center')),
            ], width= 7),
            dbc.Col([
                # dbc.Row(f'Country: {ESPN_Channel_gen_details['country']}', style= dict(display= 'flex', justifyContent= 'center'), class_name= 'pt-3'),
                dbc.Row(html.Img(src= ESPN_Channel_gen_details['thumbnails'], style= dict(height= '75%', width= '75%')), style={"display": "flex", "align-items": "center", "justify-content": "center"})
            ], width= 5)
        ])
        one_second_child= [
            dbc.Row(html.H5(f'{ESPN_Channel_gen_details['title']}({ESPN_Channel_gen_details['customUrl']})', style= dict(display= 'flex', justifyContent= 'center')), class_name= 'pt-2'),
            dbc.Row(html.P(ESPN_Channel_gen_details['description']))
        ]
        playlists= []
        for i in ESPN_Channel_playlists:
            playlists.append(i['title'])
        dropdown_playlist_options= playlists
    return one_first_child, one_second_child, dropdown_playlist_options

@callback(
    Output('datatable_videos', 'columns'), Output('datatable_videos', 'data'), Output('datatable_videos', 'style_data_conditional'), Output('datatable_videos', 'style_header_conditional'), Output('datatable_videos', 'style_table'), Output('datatable_videos', 'page_size'), Output('datatable_videos', 'selected_cells'),
    Input('dropdown_playlist', 'value')
)
def Update_videos_datatable(value):
    if value != None:
        global Channel_playlists
        Channel_playlists_pd= pd.DataFrame(Channel_playlists)
        playlist_id= Channel_playlists_pd.loc[Channel_playlists_pd['title']== value]['id'].iloc[0]
        global Playlists_videos_pd
        Playlists_videos_pd= pd.DataFrame(get_videos_from_playlist(youtube, playlist_id))
        Playlists_videos_pd= Playlists_videos_pd.reset_index().rename(columns= {'index': 'id'})
        columns= [
            {'name': i, 'id': i} for i in Playlists_videos_pd.columns if i == 'title'
        ]
        data= Playlists_videos_pd.to_dict('records')
        first_four_colors = ['rgb(255, 0, 0)', 'rgb(0, 255, 0)', 'rgb(0, 0, 255)', 'rgb(255, 255, 0)']
        style_data_conditional= [
            {
                'if': {
                    'row_index': i
                },
                'color': first_four_colors[i % 4],
                'textOverflow': 'ellipsis',
                'overflow': 'hidden',
                'text-align': 'start'
            } for i in Playlists_videos_pd.index
        ]
        style_header_conditional= [
            {
                'if': {
                    'column_id' : 'title'
                },
                'display': 'none'
            }
        ]
       
    else:
        global ESPN_Playlist_videos_pd
        ESPN_Playlist_videos_pd= pd.DataFrame(ESPN_Playlist_videos)
        ESPN_Playlist_videos_pd= ESPN_Playlist_videos_pd.reset_index().rename(columns= {'index': 'id'})
        columns= [
            {'name': i, 'id': i} for i in ESPN_Playlist_videos_pd.columns if i == 'title'
        ]
        data= ESPN_Playlist_videos_pd.to_dict('records')
        first_colors = ['rgb(204, 0, 0)', 'rgb(204, 102, 0)', 'rgb(204, 204, 0)', 'rgb(102, 204, 0)', 'rgb(0, 204, 204)', 'rgb(0, 102, 204)', 'rgb(0, 0, 204)', 'rgb(102, 0, 204)']
        style_data_conditional= [
            {
                'if': {
                    'row_index': i
                },
                'color': first_colors[i % 8],
                'textOverflow': 'ellipsis',
                'overflow': 'hidden',
                'text-align': 'start'
            } for i in ESPN_Playlist_videos_pd.index
        ]
        style_header_conditional= [
            {
                'if': {
                    'column_id' : 'title'
                },
                'display': 'none'
            }
        ]
    style_table= {"overflowX": "auto"}
    page_size= 8
    selected_cells= []
    return columns, data, style_data_conditional, style_header_conditional, style_table, page_size, selected_cells

@callback(
    Output('datatable_comments', 'columns'), Output('datatable_comments', 'data'), Output('datatable_comments', 'style_data_conditional'), Output('datatable_comments', 'style_header_conditional'),Output('datatable_comments', 'style_table'),Output('datatable_comments', 'page_size'),
    Input('datatable_videos', 'active_cell')
)
def Update_comments_table(active_cell):
    if active_cell:
        row= int(active_cell['row_id'])
        videoId= Playlists_videos_pd['videoId'][row]
        global commens_table
        try:
            commens_table= pd.DataFrame(video_get_comment_details(youtube, videoId))
            columns= [
                {'name':i, 'id': i} for i in commens_table.columns if i != 'id'
            ]
            data= commens_table.to_dict('records')
            style_data_conditional= [
                {
                    'if': {
                        'column_id': col
                    },
                    'text-align': 'left',
                } for col in commens_table.columns
            ]
            style_header_conditional= [
                {
                    'if': {
                        'column_id' : col
                    },
                    'text-align': 'center',
                } for col in commens_table.columns
            ]

        except:
            commens_table= initial_df(1, 'There is no comments in this video', 'Elements')
            columns= [
                {'name':i, 'id': i} for i in commens_table.columns if i == 'Elements'
            ]
            data= commens_table.to_dict('records')
            style_data_conditional= [
                {
                    'if': {
                        'column_id': col
                    },
                    'text-align': 'center',
                    'width': '150px'
                } for col in commens_table.columns
            ]
            style_header_conditional= [
                {
                    'if': {
                        'column_id' : 'Elements'
                    },
                    'text-align': 'center'
                }
            ]
        style_table= {"overflowX": "auto"}
        page_size= 9
    else:
        
        commens_table= pd.DataFrame(ESPN_comments)
        columns= [
            {'name':i, 'id': i} for i in commens_table.columns if i != 'id'
        ]
        data= commens_table.to_dict('records')
        style_data_conditional= [
            {
                'if': {
                    'column_id': col
                },
                'text-align': 'left'
            } for col in commens_table.columns
        ]
        style_header_conditional= [
            {
                'if': {
                    'column_id' : col
                },
                'text-align': 'center'
            } for col in commens_table.columns
        ]
        style_table= {"overflowX": "auto"}
        page_size= 9
    return columns, data, style_data_conditional, style_header_conditional, style_table, page_size

if __name__ == '__main__':
    app.run()