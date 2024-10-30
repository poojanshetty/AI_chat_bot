import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import random
import time as wait
import numpy as np
import threading
import pyautogui
# import main
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
chatStr = ""
chat_lock = threading.Lock()



def chat(query):
    try:
        global chatStr
        print(chatStr)
        openai.api_key = apikey
        print(f"User: {query}")
        chatStr += f"User: {query}\n : Chatbot"
        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            prompt= chatStr,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        say(response["choices"][0]["text"])
        chatStr += f"{response['choices'][0]['text']}\n"
        return response["choices"][0]["text"]
    except Exception as e:
        say("AI chat not working because of the API key ")


def open_google_and_search():
    webbrowser.open("https://www.google.com")
    wait.sleep(5)  # Wait for the browser to open and the page to load
    say("Google opened. Please speak your search query.")

    while True:
        query = takeCommand()  # Take voice input
        if query.lower() == "search":
            pyautogui.press('enter')  # Simulate pressing the Enter key to search
            say("Searching now.")
            break
        else:
            pyautogui.typewrite(query)  # Type the recognized query into the Google search bar
            say(f"Typed {query}. Say 'search' when you're ready to search.")


def ai_text(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # Make sure to specify the correct model
        messages=[{"role": "user", "content": prompt}],  # New format for the input
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    try:
        print(response['choices'][0]['message']['content'])  # Adjusted to match the new response format
        text += response['choices'][0]['message']['content']

        if not os.path.exists("Openai"):
            os.mkdir("Openai")

        with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
            f.write(text)
    except Exception as e:
        say("AI text generator is not working because of the API key.")


def say(text):
    os.system(f'say "{text}"')


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold =  0.6
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-us")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from User"


def listen_for_commands():
    while True:
        query = takeCommand()
        if query:
            handle_query(query)


def handle_query(query):
    global chatStr
    sites = [
        ["youtube", "https://www.youtube.com"],
        ["wikipedia", "https://www.wikipedia.com"],
        ["google", "https://www.google.com"],
        ["instagram", "https://www.instagram.com/"],
        ["facebook", "https://www.facebook.com/"],
        ["twitter", "https://www.twitter.com/"],
        ["github", "https://www.github.com/"],
        ["linkedin", "https://www.linkedin.com/"],
        ["stackoverflow", "https://www.stackoverflow.com/"],
    ]
    for site in sites:
        if f"open {site[0]}".lower() in query.lower():
            say(f"Opening {site[0]} ...")
            webbrowser.open(site[1])
            return

    # Open applications
    apps = {
        "facetime": "/System/Applications/FaceTime.app",
        "photos": "/System/Applications/Photos.app",
        "messages": "/System/Applications/Messages.app",
    }

    for app_name, app_path in apps.items():
        if f"open {app_name}".lower() in query.lower():
            say(f"Opening {app_name.capitalize()} ...")
            os.system(f"open {app_path}")
            return

    if "open google" in query.lower():
        say("Opening Google...")
        open_google_and_search()

    elif "open music" in query:
        cwd = os.getcwd()
        musicPath = os.path.join(cwd, "fe_chat_bot/assets")
        files = os.listdir(musicPath)
        mp3_files = [file for file in files if file.endswith('.mp3')]

        song_name = query.replace("open music ", "").replace(" ", "_") + ".mp3"

        specific_song = [file for file in mp3_files if song_name.lower() in file.lower()]

        if specific_song:
            fullPath = os.path.join(musicPath, specific_song[0])
            print(f"Playing {fullPath}")
            os.system(f"open \"{fullPath}\"")
        else:
            for mp3_file in mp3_files:
                fullPath = os.path.join(musicPath, mp3_file)
                print(f"Playing {fullPath}")
                os.system(f"open \"{fullPath}\"")
        return

    elif "the time" in query:
        hour = datetime.datetime.now().strftime("%H")
        min = datetime.datetime.now().strftime("%M")
        say(f"The time is {hour} {min}")
        return

    elif "using ai".lower() in query.lower():
        ai_text(prompt=query)
        return

    elif "chat with bot".lower() in query.lower():
        say("Hi, I am your chatbot. How can I help you today?")
        chat(query)
        return

    elif "reset chat".lower() in query.lower():
        chatStr = ""
        return

    elif "exit".lower() in query.lower():
        say("Goodbye! Have a great day!")
        os._exit(0)

    else:
        random_responses = [
            "I am not able to understand. Can you please repeat?",
            "Sorry, I didn't catch that. Could you say it again?",
            "I'm not sure I understood you. Could you try repeating that?"
        ]
        say(random.choice(random_responses))


if __name__ == '__main__':
    print('Welcome to A.I Chat bot, Can I help you with something today?')
    say("Welcome to A.I Chat bot, Can I help you with something today?")
    command_thread = threading.Thread(target=listen_for_commands)
    command_thread.daemon = True
    command_thread.start()

    while True:
        wait.sleep(600)
        say("Sorry no response from user for 10 minutes. I am closing the chat")
        break
