import pyttsx3  # pip install pyttsx3
import datetime
import wikipedia  # pip install wikipedia
import speech_recognition as sr  # pip install speechRecognition
import webbrowser
import os
import random
import smtplib  # pip install smtplib
import ssl
import pyjokes  # pip install pyjokes

from dotenv import load_dotenv
load_dotenv()

EMAIL_PASS = os.getenv('EMAIL_PASS')

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[0].id)

engine.setProperty('voices', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak('Good morning Hitesh')
    elif hour >= 12 and hour < 18:
        speak('Good afternoon')
    else:
        speak('Good Evening')
    speak('I am Jarvis, How may I help you.')


def takeCommand():
    # it takes microphone input from the user and returns string
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.6
        # r.energy_threshold = 100
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='eng-in')
        print(f"User said: {query}")
    except Exception as e:
        # print(e)
        print("Say that again")
        return 'None'
    return query


def sendEmail(to, content):
    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = "hiteshbhargav420@gmail.com"
    receiver_email = to

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        try:
            server.login(sender_email, EMAIL_PASS)
            res = server.sendmail(sender_email, receiver_email, content)
            print("Email sent successfully")
            speak("Email sent successfully")
        except:
            print("There was an error Please try again")
            speak("There was an error Please try again")


def aMessage(message):
    print(message)
    speak(message)


def addTask(message):
    print(message)


if __name__ == '__main__':
    wishMe()
    while True:
        query = takeCommand().lower()
        # logic for executing tasks based on query
        if 'wikipedia' in query:
            speak("Searching wikipedia...")
            query = query.replace('wikipedia', '')
            results = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia")
            print(results)
            speak(results)

        elif 'thank' in query:
            aMessage("Your Welcome")

        elif 'jarvis' in query:
            aMessage("How may I help you?")

        elif 'hello' in query:
            aMessage("Hello, How may I help you?")

        elif 'youtube' in query:
            def searchOnYoutube():
                speak("What you want to search?")
                keyword = takeCommand().lower()
                print(f"Searching for {keyword}")
                url = "https://www.youtube.com/results?search_query="+keyword
                webbrowser.open(url)
                print(keyword)
            searchOnYoutube()

        elif 'google' in query:
            def searchOnGoogle():
                speak("What you want to search?")
                keyword = takeCommand().lower()
                print(f"Searching for {keyword}")
                url = "https://www.google.com/search?q="+keyword
                webbrowser.open(url)
                speak(f"Here are the results for {keyword}")
                print("Searching for ", keyword)
            searchOnGoogle()

        elif 'how are you' in query:
            aMessage("I am good sir, How are you?")

        elif 'who are you' in query:
            aMessage("I am Jarvis")

        elif 'exit' in query:
            aMessage("Good bye")
            quit()

        elif 'created' in query:
            aMessage("I am a computer program, I am developed by Hitesh")

        elif 'joke' in query:
            jokeIs = pyjokes.get_joke()
            aMessage(jokeIs)

        elif 'play some music' in query:
            music_dir = 'C:\\Users\\Hitesh\\Music'
            songs = os.listdir(music_dir)
            # print(songs)
            randomSong = songs[random.randint(0, len(songs))]
            print("playing ", randomSong)
            os.startfile(os.path.join(music_dir, randomSong))

        elif "time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(f'Its {strTime}')
            speak(f'Its {strTime}')

        elif 'code' in query:
            codePath = "C:\\Users\\Hitesh\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif 'email' in query:
            try:
                speak('What should I say')
                content = takeCommand()
                to = 'harshbhargav49@gmail.com'
                sendEmail(to, content)
            except Exception as e:
                print(e)
                speak("Try again")
        elif "reminder" in query:
            speak("What is the reminder?")
            message = "test message"
            addTask(message)


'''
user input (voice)

'''
