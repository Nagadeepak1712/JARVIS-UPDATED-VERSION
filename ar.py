from Jarvis import JarvisAssistant
import re
import os
import random
import pprint
import datetime
import requests
import sys
import urllib.parse  
import pyjokes
import time
import pyautogui
import pywhatkit
import wolframalpha
from PIL import Image
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from Jarvis.features.gui import Ui_MainWindow
from Jarvis.config import config

# Instantiate Jarvis assistant object
obj = JarvisAssistant()


GREETINGS = ["hello jarvis", "jarvis", "wake up jarvis", "you there jarvis", "time to work jarvis", "hey jarvis",
             "ok jarvis", "are you there"]
GREETINGS_RES = ["always there for you sir", "i am ready sir", "your wish my command", "how can i help you sir?", "i am online and ready sir"]

EMAIL_DIC = {
    'myself': 'atharvaaingle@gmail.com',
    'my official email': 'atharvaaingle@gmail.com',
    'my second email': 'atharvaaingle@gmail.com',
    'my official mail': 'atharvaaingle@gmail.com',
    'my second mail': 'atharvaaingle@gmail.com'
}

CALENDAR_STRS = ["what do i have", "do i have plans", "am i busy"]


# Function to make Jarvis speak
def speak(text):
    obj.tts(text)

# Wolfram Alpha API app ID from config
app_id = config.wolframalpha_id

# Wolfram Alpha query function
def computational_intelligence(question):
    try:
        client = wolframalpha.Client(app_id)
        answer = client.query(question)
        answer = next(answer.results).text
        print(answer)
        return answer
    except:
        speak("Sorry sir I couldn't fetch your question's answer. Please try again ")
        return None

# Startup function to initialize Jarvis
def startup():
    speak("Initializing Jarvis")
    speak("Starting all systems applications")
    speak("Installing and checking all drivers")
    speak("Caliberating and examining all the core processors")
    speak("Checking the internet connection")
    speak("Wait a moment sir")
    speak("All drivers are up and running")
    speak("All systems have been activated")
    speak("Now I am online")

    # Greeting based on time of day
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12:
        speak("Good Morning")
    elif hour > 12 and hour < 18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    
    # Tell time
    c_time = obj.tell_time()
    speak(f"Currently it is {c_time}")
    speak("I am Jarvis. Online and ready sir. Please tell me how may I help you")

# Function to wish user based on time of day
def wish():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12:
        speak("Good Morning")
    elif hour > 12 and hour < 18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    c_time = obj.tell_time()
    speak(f"Currently it is {c_time}")
    speak("I am Jarvis. Online and ready sir. Please tell me how may I help you")

# Main thread execution to start tasks
class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.TaskExecution()

    def TaskExecution(self):
        # Call startup and wish functions
        startup()
        wish()

        while True:
            command = obj.mic_input()

            # Command for telling date
            if re.search('date', command):
                date = obj.tell_me_date()
                print(date)
                speak(date)

            # Command for telling time
            elif "time" in command:
                time_c = obj.tell_time()
                print(time_c)
                speak(f"Sir the time is {time_c}")

            # Command for launching applications
            elif re.search('launch', command):
                dict_app = {
                    'chrome': 'C:/Program Files/Google/Chrome/Application/chrome'
                }

                app = command.split(' ', 1)[1]
                path = dict_app.get(app)

                if path is None:
                    speak('Application path not found')
                    print('Application path not found')
                else:
                    speak(f'Launching: {app} for you sir!')
                    obj.launch_any_app(path_of_app=path)

            # Handle greetings commands
            elif command in GREETINGS:
                speak(random.choice(GREETINGS_RES))

            # Command to open websites
            elif re.search('open', command):
                domain = command.split(' ')[-1]
                open_result = obj.website_opener(domain)
                speak(f'Alright sir !! Opening {domain}')
                print(open_result)

            # Command for weather information
            elif re.search('weather', command):
                city = command.split(' ')[-1]
                weather_res = obj.weather(city=city)
                print(weather_res)
                speak(weather_res)

            # Command for Wikipedia queries
            elif re.search('tell me about', command):
                topic = command.split(' ')[-1]
                if topic:
                    wiki_res = obj.tell_me(topic)
                    print(wiki_res)
                    speak(wiki_res)
                else:
                    speak("Sorry sir. I couldn't load your query from my database. Please try again")

            # Command for showing news headlines
            elif "buzzing" in command or "news" in command or "headlines" in command:
                news_res = obj.news()
                speak('Source: The Times Of India')
                speak('Todays Headlines are..')
                for index, articles in enumerate(news_res):
                    pprint.pprint(articles['title'])
                    speak(articles['title'])
                    if index == len(news_res)-2:
                        break
                speak('These were the top headlines, Have a nice day Sir!!..')

            # Command for searching Google
            elif 'search google for' in command:
                obj.search_anything_google(command)

            # Command to play music
            elif "play music" in command or "hit some music" in command:
                music_dir = "F://Songs//Imagine_Dragons"
                songs = os.listdir(music_dir)
                for song in songs:
                    os.startfile(os.path.join(music_dir, song))

            # Command to play video on YouTube
            elif 'youtube' in command:
                video = command.split(' ')[1]
                speak(f"Okay sir, playing {video} on youtube")
                pywhatkit.playonyt(video)

            # Command to send emails
            elif "email" in command or "send email" in command:
                sender_email = config.email
                sender_password = config.email_password

                try:
                    speak("Whom do you want to email sir ?")
                    recipient = obj.mic_input()
                    receiver_email = EMAIL_DIC.get(recipient)
                    if receiver_email:
                        speak("What is the subject sir ?")
                        subject = obj.mic_input()
                        speak("What should I say?")
                        message = obj.mic_input()
                        msg = 'Subject: {}\n\n{}'.format(subject, message)
                        obj.send_mail(sender_email, sender_password, receiver_email, msg)
                        speak("Email has been successfully sent")
                        time.sleep(2)

                    else:
                        speak("I couldn't find the requested person's email in my database. Please try again with a different name")

                except:
                    speak("Sorry sir. Couldn't send your mail. Please try again")

            # Command for calculations using WolframAlpha
            elif "calculate" in command:
                question = command
                answer = computational_intelligence(question)
                speak(answer)

            # Command to open Google Calendar events
            elif "what do i have" in command or "do i have plans" or "am i busy" in command:
                obj.google_calendar_events(command)

            # Command to make notes
            if "make a note" in command or "write this down" in command or "remember this" in command:
                speak("What would you like me to write down?")
                note_text = obj.mic_input()
                obj.take_note(note_text)
                speak("I've made a note of that")

            # Command to close notepad
            elif "close the note" in command or "close notepad" in command:
                speak("Okay sir, closing notepad")
                os.system("taskkill /f /im notepad++.exe")

            # Command to tell a joke
            if "joke" in command:
                joke = pyjokes.get_joke()
                print(joke)
                speak(joke)

            # Command to show system information
            elif "system" in command:
                sys_info = obj.system_info()
                print(sys_info)
                speak(sys_info)

            # Command to locate places
            elif "where is" in command:
                place = command.split('where is ', 1)[1]
                current_loc, target_loc, distance = obj.location(place)
                city = target_loc.get('city', '')
                state = target_loc.get('state', '')
                country = target_loc.get('country', '')
                speak(f"Located at: {city}, {state}, {country}")
                speak(f"Distance: {distance}")
                print(f"Located at: {city}, {state}, {country}")
                print(f"Distance: {distance}")

            # Exit command
            elif "exit" in command:
                speak("Exiting Jarvis, Have a good day sir!")
                sys.exit()


if __name__ == "__main__":
    MainThread().start()
