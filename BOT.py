/*
MIT License

Copyright (c) 2019 Sanidhya Sharma

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/


#Import Packages \(-_-)/
import speech_recognition as sr
import pyttsx3
import sys
import os
import re
import subprocess
import requests
import datetime
import wikipedia
import webbrowser
import random 
#import pyowm
import json
#from pyowm import OWM
from bs4 import BeautifulSoup as soup
import urllib.request 
from urllib.request import urlopen
#import youtube_dl

#The speech engine 
engine = pyttsx3.init('sapi5')          

#Gender Voice
en_Female_Voice_id = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0"

voices = engine.getProperty('voice')
engine.setProperty('voice', en_Female_Voice_id)

#voice property (Speed and rate)
engine.setProperty('volume', 0.9)
engine.setProperty('rate', 150) 


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

#initiating a wishing system for the user using real time 24hr format 
def wishMe():
    hour = int(datetime.datetime.now().hour)

    if hour>=0 and hour<12:
        speak("Good Morning")

    elif hour>=12 and hour<18:
        speak("Good Afternoon")

    elif hour>=18 and hour<24:
        speak("Good Evening")
    
    speak("Hi i am xaaya!. How may i help you Sir?")


#Takes input (Microphone) from the user and responding to odd events 
def takeCommand():
                                    

    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listning....")
        r.pause_threshold = 1
        r.energy_threshold = 4000
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        print("Recognising....")
        querry = r.recognize_google(audio, language='en-in')
        print(f"User said: {querry}\n")

    except Exception as e:
        print(e)
        speak("Sorry! Could you please repeat that again?")
        print("Sorry! Could you please repeat that again?")
        return "None"
        
    return querry

#The main bot with specific functions it uses to identify the repective function for it 
def Bot():

    while True:
        querry = takeCommand().lower()

        if 'wikipedia' in querry:
            speak("Searching in Wikipedia.....")
            querry = querry.replace('Wikipedia',"")
            results = wikipedia.summary(querry, sentences=2)
            speak("According to Wikipedia")
            speak(results)
        
        elif 'hi' in querry:
            speak('Hi Sir! How are you?')

        #elif 'open youtube' in querry:
            #webbrowser.open("Youtube.com")
                                               #these codes are waste Basically
        #elif 'open google' in querry:
            #webbrowser.open("Google.co.in")
        
        elif "who made you" in querry or "created you" in querry: 
            speak("I have been created by Sanidhya Sharma.")

        
        elif 'play music' in querry:
            r1 = random.randint(0, 20) 
            music_dir = 'D:\\Personal Data Drive\\SONGS\\My Selection (Songs)\\Rock'
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[r1]))
                                                             
        elif "what's the time now" in querry:
            strTime = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"Sir the time is {strTime}")
        
        elif "what's today" in querry:
            strDate = datetime.datetime.now().strftime("%d:%B:%Y:%A")
            speak(f"Sir the day is {strDate}")

        elif 'open chrome' in querry:
            codepath = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
            os.startfile(codepath)

        elif 'shutdown' in querry:
            speak('Shutting down!. Have a nice day')
            sys.exit()

        elif 'tell me a joke' in querry:
            res = requests.get(
                'https://icanhazdadjoke.com/',
                headers={"Accept":"application/json"})
            if res.status_code == requests.codes.ok:
                speak(str(res.json()['joke']))
            else:
                speak('oops!I ran out of jokes')
        
        elif  'open reddit' in querry:
            reg_ex = re.search('open reddit (.*)', querry)
            url = 'https://www.reddit.com/'
            if reg_ex:
                subreddit = reg_ex.group(1)
                url = url + 'r/' + subreddit
            webbrowser.open(url)
            speak('The Reddit content has been opened for you Sir.')

        elif 'search' in querry:
            reg_ex = re.search('search (.+)', querry)
            if reg_ex:
                domain = reg_ex.group(1)
                print(domain)
                url = 'https://www.' + domain + '.com'
                webbrowser.open(url)
                speak('The website you have requested for Search has been opened for you Sir.')
            else:
                pass
        
        elif 'news for today' in querry:
            try:
                news_url="https://news.google.com/news/rss"
                Client=urlopen(news_url)
                xml_page=Client.read()
                Client.close()
                soup_page=soup(xml_page,"xml")
                news_list=soup_page.findAll("item")
                for news in news_list[:15]:
                    speak(news.title.text.encode('utf-8'))
            except Exception as e:
                print(e)

        elif 'launch' in querry:
            reg_ex = re.search('launch (.*)', querry)
            if reg_ex:
                appname = reg_ex.group(1)
                appname1 = appname+".app"
                subprocess.Popen(["open", "-n", "/Applications/" + appname1], stdout=subprocess.PIPE)
                speak('I have launched the desired application')

        elif 'tell me about' in querry:
            reg_ex = re.search('tell me about (.*)', querry)
            try:
                if reg_ex:
                    topic = reg_ex.group(1)
                    ny = wikipedia.page(topic)
                    speak(ny.content[:500].encode('utf-8'))
            except Exception as e:
                    print(e)
                    speak("Sorry i couldn't find" )

        elif 'search a song on youtube' in querry:
            speak('What song shall I Search?')
            mysong = takeCommand()
            if mysong:
                url = "https://www.youtube.com/results?search_query=" + mysong.replace(' ', '+')
                response = urllib.request.urlopen(url)
                html = response.read()
                soup1 = soup(html,"lxml")
                url_list = []
                for vid in soup1.findAll(attrs={'class':'yt-uix-tile-link'}):
                    if ('https://www.youtube.com' + vid['href']).startswith("https://www.youtube.com/watch?v="):
                        final_url = 'https://www.youtube.com' + vid['href']
                        url_list.append(final_url)
                        url = url_list[0]
                webbrowser.open(url) 

            else:
                speak("I have not found anything in Youtube or maybe you aren't connected")


#main function for calling the wishing system and Bot
if __name__ == "__main__":
    wishMe()
    Bot()
