import pandas
import os
import lyricsgenius #Genius - lyrics
import spotipy #Spotify - genre?
from textblob import TextBlob #language detection
from sentiment_analysis_subroutine import sentiment

#artists' pronoun/gender database
GenderDB = pandas.read_csv('data/raw/GenderDataset.csv')

#Genius API access
genius_token = '2uOSW2EUhQLj1E87Ih_keYXVbKEnsKGhJMna9H_ymPuofv7KVrvon5UM3fhCraAwkffgo5WZ2l8FAesDoxoNNA'
genius = lyricsgenius.Genius(genius_token)

#Spotify API access
spotify_clientid = '7d24fb005e074e9495b640c29624b17c'
spotify_clientsecret = '9c7030f1dfa54d07b837e134e5736de4'
os.environ['SPOTIPY_CLIENT_ID'] = spotify_clientid
os.environ['SPOTIPY_CLIENT_SECRET'] = spotify_clientsecret
auth_manager = spotipy.oauth2.SpotifyClientCredentials()
spotify = spotipy.Spotify(auth_manager=auth_manager)


for i in range(62, 0, -1):
    if os.path.isfile('data/final_processed'+str(i)+'.csv'):
        continue
    df = pandas.read_csv('data/raw/final_unprocessed'+str(i)+'.csv')
    df['gender'] = None
    df['nltk_positive'] = None
    df['nltk_negative'] = None
    df['nltk_score'] = None
    df['nltk_top_emotion'] = None

    df_temp = pandas.DataFrame()
    df_temp['genres'] = None

    for ind, row in df.iterrows():
        print("Quering for entry " + str(ind + 1) + " out of " + str(len(df.index) + 1))

        #Artists' gender DB query
        GDBArtist = GenderDB.loc[ GenderDB['name'] == row['artist']]
        for ind2, row2 in GDBArtist.iterrows():
            GDBname = row2[1]
            GDBpron = row2[3]
            GDBgender = row2[4]
        if GDBname == row['artist']:
            if GDBpron == 'they/them' and GDBgender != None:
                if GDBgender == 'male':
                    df.loc[ind, 'Gender'] = 'Male'
                elif GDBgender == 'female':
                    df.loc[ind, 'Gender'] = 'Female'
            elif GDBpron == 'he/him':
                df.loc[ind, 'Gender'] = 'Male'
            elif GDBpron == 'she/her':
                df.loc[ind, 'Gender'] = 'Female'
        print(df.loc[ind, 'Gender'])

        #Genius Query
        genius_song = genius.search_song(row['song'])
        if not genius_song:
            continue
            #TextBlob language detection
        lyrics = TextBlob(genius_song.lyrics)
        if row['song'] in ['I Wanna Be Loved', 'Reveille Rock', 'Feliz Navidad', 'Dakiti']:    #some problematic songs
            continue
        elif lyrics.detect_language() != 'en':
            continue

        #Genius Query + nltk results
        nltk_results = sentiment(genius_song.lyrics)
        if nltk_results[0] != 0.0 or nltk_results[1] != 0.0 or nltk_results[2] != 0.0 :
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

    df = pandas.concat([df, df_temp], axis=1, join="inner")
    df.to_csv('data/final_processed'+str(i)+'.csv')
