import datetime
import json
import os
import random
import smtplib  # pip install smtplib
import ssl
import webbrowser
import keyboard
import pyjokes  # pip install pyjokes
import pyttsx3  # pip install pyttsx3
import speech_recognition as sr  # pip install speechRecognition
import wikipedia  # pip install wikipedia
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

load_dotenv()


EMAIL_PASS = os.getenv('EMAIL_PASS')

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[0].id)

engine.setProperty('voices', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def aMessage(message):
    print(message)
    speak(message)


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        aMessage('Good morning Hitesh')
    elif hour >= 12 and hour < 18:
        aMessage('Good afternoon')
    else:
        aMessage('Good Evening')
    aMessage('I am echo, How may I help you.')


def takeCommand():
    # it takes microphone input from the user and returns string
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.6
        r.energy_threshold = 300
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='eng-in')
        print(f"User said: {query}")
    except Exception as e:
        aMessage("Say that again")
        return 'None'
    return query


def getCurrWeather(currCity):
    url = f"https://www.google.com/search?q=weather in {currCity}"
    r = requests.get(url)
    data = BeautifulSoup(r.text, "html.parser")
    temp = data.find("div", class_="BNeawe").text
    aMessage(f"current weather in {currCity} is {temp}")


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
            aMessage("Email sent successfully")
        except(RuntimeError):
            print(f'error: {RuntimeError}')
            aMessage("There was an error Please try again")


def setReminder(message, time, createdAtTime, createdAtDate):
    task = {}
    # speak("What is the message do you want to save?")
    task["message"] = message
    fullTime = ""

    if "minutes" not in time:
        onlyHours = time.split(" hours")[0]

        # hours = onlyHours if len(onlyHours) == 0 else pass
        if len(onlyHours) == 1:
            onlyHours = f"0{onlyHours}"
        else:
            pass
        task['remindAt'] = f"{onlyHours}:00:00.00"
        task["createdAtTime"] = createdAtTime
        task["createdAtDate"] = createdAtDate
        task['done'] = "false"
    else:
        fullTime = time.replace(" hours ", "|").replace(
            "and ", "").replace(" minutes", "").split("|")
        if len(fullTime[0]) == 1:
            fullTime[0] = f"0{fullTime[0]}"
        else:
            pass
        if len(fullTime[1]) == 1:
            fullTime[1] = f"0{fullTime[1]}"
        else:
            pass

        task['remindAt'] = f"{fullTime[0]}:{fullTime[1]}:00.00"
        task["createdAtTime"] = createdAtTime
        task["createdAtDate"] = createdAtDate
        task['done'] = "false"

    print(task)
    with open("./list.json", "r+") as openfile:
        # First we load existing data into a dict
        json_object = json.load(openfile)
        # Join new_data with json_object
        json_object['task'].append(task)
        # Sets file's current position at offset
        openfile.seek(0)
        # convert back to json.
        json.dump(json_object, openfile, indent=4)


def getReminderData(message):
    # take message
    if message:
        # take reminder time
        aMessage("So, When do you want to be reminded?")
        time = takeCommand().lower()
        # created at time and date
        createdAtTime = datetime.datetime.now().strftime("%H:%M:%S")
        createdAtDate = datetime.date.today().strftime("%B %d, %Y")
        setReminder(message, time, createdAtTime, createdAtDate)
        aMessage("You task has been added")
        print("set a reminder")
    else:
        aMessage("Say that again")


def allReminders():
    jsonFile = open("list.json", "r")
    data = json.load(jsonFile)
    j = 1
    for i in data['task']:
        aMessage(
            f"You have to {i['message']}")
        j += 1


def changeCurrCity():
    aMessage("What is your current city?")
    currCity = takeCommand().lower()
    aMessage(f"Ok, I have set you current city to {currCity}")
    with open("./list.json", "r+") as openfile:
        # First we load existing data into a dict
        json_object = json.load(openfile)
        # Join new_data with json_object
        json_object['currCity'] = currCity
        # Sets file's current position at offset
        openfile.seek(0)
        # convert back to json.
        json.dump(json_object, openfile, indent=4)


if __name__ == '__main__':
    wishMe()
    while True:
        query = takeCommand().lower()
        # logic for executing tasks based on query
        if "task" in query or "add a task" in query:
            aMessage("What is the task?")
            message = takeCommand().lower()
            getReminderData(message)

        elif "list all reminders" in query or "are my reminders" in query or "reminders" in query:
            allReminders()

        elif "weather" in query:
            jsonFile = open("list.json", "r")
            data = json.load(jsonFile)
            if data['currCity']:
                getCurrWeather(data['currCity'])
                aMessage("You can change the current city anytime")
            else:
                changeCurrCity()

        elif "change current city" in query:
            changeCurrCity()

        elif "what are you capable" in query or "what can you do" in query or "what you can do" in query:
            aMessage("I am fully working on voice commands, I can do some of your tasks such as playing musics, search somehting on google, youtube, etc, I am also capable of taking reminders, I can also tell the current time and weather and much more")
            aMessage("what can I do for you?")

        elif 'wikipedia' in query:
            aMessage("Searching wikipedia...")
            query = query.replace('wikipedia', '')
            results = wikipedia.summary(query, sentences=1)
            aMessage("According to wikipedia")
            aMessage(results)

        elif "click" in query:
            aMessage("What do you want to press?")
            command = keyword = takeCommand().lower()
            keyboard.press_and_release(command)

        elif 'thank' in query:
            aMessage("Your Welcome")

        elif 'echo' in query:
            aMessage("Hello, How may I help you?")

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
            aMessage("I am echo")

        elif 'exit' in query:
            aMessage("Good bye")
            quit()

        elif 'created' in query:
            aMessage("I am a computer program, I am developed by Hitesh")

        elif 'joke' in query:
            jokeIs = pyjokes.get_joke()
            aMessage(jokeIs)

        elif 'play some music' in query:
            music_dir = 'G:\Music\ENG'
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
                aMessage('What should I say')
                content = takeCommand()
                to = 'hiteshcodes@gmail.com'
                sendEmail(to, content)
            except Exception as e:
                print(e)
                aMessage("Try again")
