import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import numpy as np
scope = 'playlist-modify-public playlist-modify-private'
username = 'ENTER USERNAME'

#SET SPOTIPY_CLIENT_ID=
#SET SPOTIPY_CLIENT_SECRET=
#SET SPOTIPY_REDIRECT_URI=

token = SpotifyOAuth(scope=scope, username=username)
spotifyObject = spotipy.Spotify(auth_manager=token)

#Creating the Playlist
playlist_name = input("Enter a playlist name: ")
description = input("Enter a playlist description: ")
spotifyObject.user_playlist_create(user=username,name=playlist_name,public=True,description=description)

#Finding Artist
artist = input("Enter an artists name: ")
results = spotifyObject.search(q='artist:' + artist, type='artist')
artist = results['artists']['items'][0]['id']

#Getting All Albums & Singles
results = spotifyObject.artist_albums(artist_id=artist,album_type='single',country=None,limit=50,offset=0)
list_of_albums = []
for i in range(len(results['items'])):
    list_of_albums.append(results['items'][i]['id'])
results = spotifyObject.artist_albums(artist_id=artist,album_type='album',country=None,limit=50,offset=0)
for l in range(len(results['items'])):
    list_of_albums.append(results['items'][l]['id'])
#Getting All Songs in Album (- duplicates)
list_of_songs = []
list_of_songs_names = []
for i in range(len(list_of_albums)):
    results = spotifyObject.album_tracks(list_of_albums[i],limit=50,offset=0,market=None)
    for j in range(len(results['items'])):
        if(results['items'][j]['name'] not in list_of_songs_names):
            list_of_songs_names.append(results['items'][j]['name'])
            list_of_songs.append(results['items'][j]['id'])

#Locate Playlist to Add to
Playlists = spotifyObject.user_playlists(user=username)
playlist = Playlists['items'][0]['id']

#Adding Tracks
if(len(list_of_songs) <= 100):
    spotifyObject.user_playlist_add_tracks(user=username,playlist_id=playlist,tracks=list_of_songs)
else:
    list_of_lists = np.array(list_of_songs)
    final_list = np.array_split(list_of_lists, 10)
    for k in range(len(final_list)):
        spotifyObject.user_playlist_add_tracks(user=username,playlist_id=playlist,tracks=final_list[k])
