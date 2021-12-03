import pandas
import os
import lyricsgenius #Genius - lyrics
import music_story #MusicStory - gender
import spotipy #Spotify - genre?

df = pandas.read_csv('data/raw/charts_test.csv') #use 'data/raw/charts_test.csv' for a smaller file
#df.head(1000).to_csv('data/raw/charts_test.csv')
df.drop(columns = ['last-week','peak-rank','weeks-on-board'], inplace = True)
df['date'] = pandas.to_datetime(df['date'])
df['date'] = pandas.DatetimeIndex(df['date']).year
print (df.head())
print(df.dtypes)
df['gender'] = None

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
    #Genius Query (unused)

df = pandas.concat([df, df_temp], axis=1, join="inner")
df.to_csv('data/data_processed.csv')
