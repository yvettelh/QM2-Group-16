import pandas
import os
import lyricsgenius #Genius - lyrics
import music_story #MusicStory - gender
import spotipy #Spotify - genre?
from textblob import TextBlob #language detection
from sentiment_analysis_subroutine import sentiment

df = pandas.read_csv('data/raw/yearly_charts_test_tiny.csv') #use 'data/raw/charts_test.csv' for a smaller file
df['gender'] = None
df['nltk_positive'] = None
df['nltk_negative'] = None
df['nltk_score'] = None
df['nltk_top_emotion'] = None

genius_token = '2uOSW2EUhQLj1E87Ih_keYXVbKEnsKGhJMna9H_ymPuofv7KVrvon5UM3fhCraAwkffgo5WZ2l8FAesDoxoNNA'
genius = lyricsgenius.Genius(genius_token)

ms_token = '5c59e24b78896f1f368808fe935869b646397d8c'
ms_secret = '580922ef1cdce8e234c71d2c797787b3c1d37879'
ms_api = music_story.MusicStoryApi(ms_token, ms_secret)
tok = ms_api.token
tok_secret = ms_api.token_secret
ms_api.connect()

spotify_clientid = '7d24fb005e074e9495b640c29624b17c'
spotify_clientsecret = '9c7030f1dfa54d07b837e134e5736de4'
os.environ['SPOTIPY_CLIENT_ID'] = spotify_clientid
os.environ['SPOTIPY_CLIENT_SECRET'] = spotify_clientsecret
auth_manager = spotipy.oauth2.SpotifyClientCredentials()
spotify = spotipy.Spotify(auth_manager=auth_manager)

df_temp = pandas.DataFrame()
df_temp['genres'] = None

for ind, row in df.iterrows():

    print("Quering for entry " + str(ind + 1) + " out of " + str(len(df.index)))

    genius_song = genius.search_song(row['song'])
    if not genius_song:
        df.drop(ind, inplace=True)
        df.reset_index( drop = True, inplace=True)
        ind -= 1
        continue
    #TextBlob language detection
    lyrics = TextBlob(genius_song.lyrics)
    if lyrics.detect_language() != 'en':
        df.drop(ind, inplace=True)
        df.reset_index( drop = True, inplace=True)
        ind -= 1
        continue

    #Genius Query + nltk results
    nltk_results = sentiment(genius_song.lyrics)
    df.loc[ind, 'nltk_positive'] = nltk_results[0]
    df.loc[ind, 'nltk_negative'] = nltk_results[1]
    df.loc[ind, 'nltk_score'] = nltk_results[2]
    df.loc[ind, 'nltk_top_emotion'] = nltk_results[3]

    #Spotify Query
    spotify_result = spotify.search(row['song'])
    if spotify_result['tracks']['items']:
        spotify_track = spotify_result['tracks']['items'][0]    #Only first search result

        spotify_artist = spotify.artist(spotify_track["artists"][0]["external_urls"]["spotify"])    #Only first artist (if there are many)
        df_temp.loc[ind, 'genres'] = spotify_artist['genres'] #couldn't insert directly to df for some reason

    #MusicStory Query
    if ms_api.search('artist',name=row['artist']):
        ms_artist = ms_api.search('artist',name=row['artist'])[0]
        print(ms_artist.name)
        '''if ms_artist:
            df.loc[ind,'gender']=ms_artist.sex'''

df = pandas.concat([df, df_temp], axis=1, join="inner")
df.to_csv('data/data_processed.csv')

