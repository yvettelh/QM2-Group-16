# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 15:26:53 2021

@author: Christian
"""
#libraries for removing punctuation
import re
import string 

test = True

import lyricsgenius
#instantiation of genius object
genius = lyricsgenius.Genius('2uOSW2EUhQLj1E87Ih_keYXVbKEnsKGhJMna9H_ymPuofv7KVrvon5UM3fhCraAwkffgo5WZ2l8FAesDoxoNNA')
#client access token provided by Genius



#sentiment analysis functions
from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
from nrclex import NRCLex

#colour map for emotion analysis printing
from termcolor import colored
colour_map = {'fear':[45,42,123], #dark purple
           'anger':[207,42,40], #red
           'anticipation':[232,110,37], #orange
           'trust':[205,78,157], #pink
           'surprise':[184,147,197], #lilac
           'sadness':[66,190,216], #blue
           'disgust': [19,139,67], #green
           'joy':[243,236,24]} #yellow

colours = colour_map.keys()

#inputs: text to be analysed
        #emotions_breakdown: if True, returns distribution of emotions
        #show_positivity: if True, prints words coloured for poitive and negative
        #show_emotion: if True, prints words coloured by emotion
#output(s) from NLTK: negative score, positive score and compound score
          #from NRC: top emotion

def sentiment(text, emotions_breakdown = False, show_positivity = False, show_emotion = False):
    
    text = re.sub(r'[^\w\s-]', '', text) #remove punctuation from text
    words = re.split(' ',re.sub('\n',' ',text.strip(string.punctuation)))#split the text into individual words for printing later
    
    positivity = sia.polarity_scores(text) #calculate NLTK Score
    emotion = NRCLex(text) #calculate NRC scores
        
    NRC_words = emotion.affect_dict.keys() #list of all the words affect emotion
    
    #printing every word from the lyrics and colouring
    #red if negative,
    #green if positive 
    #white if neutral
    if show_positivity:
        for word in words:
            score = sia.polarity_scores(word)
            colour = 'white'
            if score["neg"] == 1:
                colour = 'red'
            if score["pos"] == 1:
                colour = 'green'
            print(colored(word, colour), end = ' ')
        print('\n\n')
            
    #Printing every word from the lyrics and colouring based on emotion
    #default sets colour to grey for no emotion
    #then checks if the word is in the list of words flagged as affecting emotion
    #if it is, finds the emotion most associated with the word (ignoring positive and negative)
    #colour the word according to that emotion
    if show_emotion:
        for word in words:
            rgb = [130,130,130]
            if word in NRC_words:
                emotions_found = NRCLex(word).top_emotions
                found = False
                while not found:
                    for i in emotions_found:
                        if i[0] in colours and i[1] > 0:
                            #print(i)
                            rgb = colour_map[i[0]]
                            found = True
                    found = True        
                    
            print("\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(rgb[0],rgb[1],rgb[2], word), end = ' ')
        print('\n\n')
            
    percent_positive = positivity['pos'] #positive score
    percent_negative = positivity['neg'] #negative score
    positivity_score = positivity['compound'] #compound score
    
    emotions = emotion.raw_emotion_scores.copy() #creates a copy of the list of scores for each emotion
    
    #removes the emotions 'positive' and 'negative' from the copy list
    if 'positive' in emotions.keys():
        del emotions['positive']
    if 'negative' in emotions.keys():
        del emotions['negative']
    
    top_emotion = None #set the top emotion to None by default in case no emotion is found
    if len(emotions.keys()) > 0: #checks that the list still contains emotions
        top_emotion = max(emotions, key=emotions.get) #sets the top emotion to the highest score in the list
    
    if emotions_breakdown: #returns a list giving the song's percentage of each emotion as well the normal 4 variables
        return [percent_positive, percent_negative, positivity_score, top_emotion, emotion.raw_emotion_scores]   
    else: #otherwise just returns the normal 4 variables
        return [percent_positive, percent_negative, positivity_score, top_emotion]

print(sentiment(song.lyrics, True, True, True))