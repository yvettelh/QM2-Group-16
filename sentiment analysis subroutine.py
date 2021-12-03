# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 15:26:53 2021

@author: Christian
"""
test = False

import lyricsgenius
genius = lyricsgenius.Genius('2uOSW2EUhQLj1E87Ih_keYXVbKEnsKGhJMna9H_ymPuofv7KVrvon5UM3fhCraAwkffgo5WZ2l8FAesDoxoNNA')

song = genius.search_song("Happy")

from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
from nrclex import NRCLex

from termcolor import colored

colour_map = {'fear':[45,42,123], #dark purple
           'anger':[207,42,40], #red
           'anticip':[232,110,37], #orange
           'trust':[205,78,157], #pink
           'surprise':[184,147,197], #lilac
           'sadness':[66,190,216], #blue
           'disgust': [19,139,67], #green
           'joy':[243,236,24]} #yellow

colours = colour_map.keys()

#NLTK Linear Sentiment Analysis function
#input = text to be analysed
#output(s) = 

def sentiment(text, positivity_breakdown = False, emotion_breakdown = False):
    positivity = sia.polarity_scores(text)
    emotion = NRCLex(text)
    if test:
        print(positivity)
        print(emotion.top_emotions)
    #print(emotion.raw_emotion_scores)
    NRC_words = emotion.affect_dict.keys()
    
    if positivity_breakdown:
        words = text.split(' ')
        for word in words:
            score = sia.polarity_scores(word)
            colour = 'white'
            if score["neg"] == 1:
                colour = 'red'
            if score["pos"] == 1:
                colour = 'green'
            print(colored(word, colour), end = ' ')
            
    if emotion_breakdown:
        for word in emotion.words:
            rgb = [130,130,130]
            if word in NRC_words:
                feels = NRCLex(word).top_emotions
                found = False
                while not found:
                    for i in feels:
                        if i[0] in colours and i[1] > 0:
                            #print(i)
                            rgb = colour_map[i[0]]
                            found = True
                    found = True        
                    
            print("\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(rgb[0],rgb[1],rgb[2], word), end = ' ')
      
    return [positivity,emotion.raw_emotion_scores]   
    

print(sentiment(song.lyrics))