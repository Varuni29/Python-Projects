from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

CLIENT_ID=os.environ["client_id"]
CLIENT_SECRET=os.environ["client_secret"]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                         scope="playlist-modify-private",
                         redirect_uri="http://localhost:8888/callback",
                         client_id=CLIENT_ID,
                         client_secret=CLIENT_SECRET,
                         show_dialog=True,
                         cache_path="token.txt"))

user_id=sp.current_user()["id"]

date=input("What year you would like to travel to? Type in YYY-MM-DD format: ")

URL="https://www.billboard.com/charts/hot-100/"
response=requests.get(URL+date)
website_html=response.text

soup=BeautifulSoup(website_html,"html.parser")

all_songs=soup.find_all(name="h3",class_="a-no-trucate",id="title-of-a-story")
songs_names=[song.getText() for song in all_songs]

songs_names = [item.replace("\t", "") for item in songs_names]
songs_names = [item.replace("\n", "") for item in songs_names]

song_uris = []
year = date.split("-")[0]
for song in songs_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist=sp.user_playlist_create(user=user_id,name=f"{year} Billboard 100",public=False)
sp.user_playlist_add_tracks(playlist_id=playlist["id"],tracks=song_uris,user=user_id)
