import json
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import boto3
from datetime import datetime

def lambda_handler(event, context):
    
    client_id = os.environ.get('client_id') # make sure to add this environment variables in Lamda Configuration
    client_secret = os.environ.get('client_secret') # make sure to add this environment variables in Lamda Configuration
    #add your keys here
    client_credentials_manager = SpotifyClientCredentials(client_id = client_id, client_secret = client_secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    playlists = sp.user_playlists('spotify')
        
    playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbLZ52XmnySJg" # Top 50 Bollywood Treanding URL
    playlist_URI = playlist_link.split("/")[-1] # playlistID
        
    spotify_data = sp.playlist_tracks(playlist_URI)
    
    client = boto3.client('s3')
    
    filename = "spotify_raw_" + str(datetime.now()) + ".json"
    
    client.put_object(
        Bucket="spotify-etl-project-ameet",
        Key="raw/to_be_processed/" + filename,
        Body=json.dumps(spotify_data)
        ) #dumps data in raw folder
