import praw
import datetime 
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

#Authorizations for APIs

sp_client_id = "" #Spotify Client ID
sp_client_secret = ""#Spotify CLient Secret
client_credentials_manager = SpotifyClientCredentials(sp_client_id, sp_client_secret)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager )

username="" #Spotify Username
scope="playlist-modify-public" #Scope for editing playlists
#Get authorizaition token to be able to create and edit playlists
token = util.prompt_for_user_token(username,scope,client_id=sp_client_id
                                   ,client_secret=sp_client_secret
                                   ,redirect_uri='http://localhost:7777/callback') 
sp = spotipy.Spotify(auth=token)

reddit = praw.Reddit(client_id="",#Reddit Client ID
                     client_secret="", #Reddit Client Secret
                     user_agent="", #Name of Reddit App
                     username="", #Reddit Username
                     password="")#Reddit Password


#Change the weekday so that Friday corresponds to 0, Saturday correseponds
#to 1, Sunday to 2, etc...
if datetime.datetime.now().weekday() >=4:
    day = datetime.datetime.now().weekday() -5
else:
    day = datetime.datetime.now().weekday() +3

#Always set the start day to the most recent Friday at 00:00    
start_date=datetime.datetime.now()-datetime.timedelta(days=day, hours=datetime.datetime.now().hour,
                                          minutes=datetime.datetime.now().minute,
                                          seconds=datetime.datetime.now().second,
                                          microseconds=datetime.datetime.now().microsecond)

start_date_UTC=start_date.replace().timestamp() #Convert to UTC

reg=r'\[FRESH ALBUM\] (.+) - (.+)' #Regex expression to capture Artist and Album title from reddit title
songs_to_add=[]
subreddit = reddit.subreddit('indieheads') #Get the indieheads subreddit

for submission in subreddit.top("week",limit=150): #For the top 150 posts in the last week
    #If they are "Fresh Albums", have more than 50 upvotes and were uploaded after the most recent Friday
    if "[FRESH ALBUM]" in submission.title and submission.score >=50 and start_date_UTC < submission.created: 
        #Create a spotify query from the submission title using regex
        regex_obj=re.findall(reg,submission.title)
        query="album:"+regex_obj[0][1].lower()+" artist:"+regex_obj[0][0].lower()
        query_results=spotify.search(q=query , type='album')
        #If the album exists on Spotify extract all the track IDs from
        #it and add to a list
        if len(query_results['albums']['items']) != 0:
            uri=query_results['albums']['items'][0]['uri']
            tracks=spotify.album_tracks(uri)['items']
            for track in tracks:
                songs_to_add.append(track['uri'])
        
#Update playlist with tracks from albums that fit the criteria
sp.playlist_replace_items("",#Spotify playlist ID to add the tracks to
                          songs_to_add)

#Every Thursday make a new playlist with all the albums that fit the criteria
#for that past week
if datetime.datetime.now().weekday() == 3:
    start_date_new=(datetime.datetime.now()-datetime.timedelta(6)).strftime("%d/%m/%Y")
    end_date_new=(datetime.datetime.now()).strftime("%d/%m/%Y")
    new_playlist=sp.user_playlist_create(username, name="Indieheads New Albums "+ start_date_new + " - " + end_date_new)
    sp.playlist_replace_items(new_playlist['uri'], songs_to_add)

