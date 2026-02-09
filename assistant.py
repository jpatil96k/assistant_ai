import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import pyaudio
import webbrowser
import os
import pywhatkit
import importlib.util

pyaudio_spec = importlib.util.find_spec("pyaudio")
MIC_AVAILABLE = pyaudio_spec is not None

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 190)

def speak(audio):
    print(audio)
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("How can I help you today?")

def takecommand():
    """Takes voice input if possible, else asks for typed input."""
    if not MIC_AVAILABLE:
        speak("Microphone not available. Please type your command.")
        return input("Your command: ")

    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
        except Exception:
            speak("No speech detected, please type your command.")
            return input("Your command: ")

    try:
        speak("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query
    except Exception:
        speak("Sorry, I didn't understand. Please type your command.")
        return input("Your command: ")

def open_and_search(query):
    query = query.lower()
    if 'youtube' in query:
        if 'search' in query:
            search_term = query.split('search', 1)[1].strip()
            speak(f"Searching YouTube for {search_term}")
            pywhatkit.playonyt(search_term)
        else:
            speak("Opening YouTube")
            webbrowser.open("https://youtube.com")

    elif 'google' in query:
        if 'search' in query:
            search_term = query.split('search', 1)[1].strip()
            speak(f"Searching Google for {search_term}")
            webbrowser.open(f"https://www.google.com/search?q={search_term}")
        else:
            speak("Opening Google")
            webbrowser.open("https://google.com")

    elif 'instagram' in query:
        if 'search' in query or 'id' in query:
            if 'id' in query:
                username = query.split('id', 1)[1].strip().replace(" ", "")
            else:
                username = query.split('search', 1)[1].strip().replace(" ", "")
            speak(f"Opening Instagram profile {username}")
            webbrowser.open(f"https://instagram.com/{username}")
        else:
            speak("Opening Instagram")
            webbrowser.open("https://instagram.com")

    elif 'spotify' in query:
        if 'play' in query or 'search' in query:
            if 'play' in query:
                song = query.split('play', 1)[1].strip()
            else:
                song = query.split('search', 1)[1].strip()
            speak(f"Searching Spotify for {song}")
            webbrowser.open(f"https://open.spotify.com/search/{song.replace(' ', '%20')}")
        else:
            speak("Opening Spotify")
            webbrowser.open("https://spotify.com")

    else:
        speak("Sorry, I don't know how to handle that website yet.")

if __name__ == "__main__":
    wishMe()
    while True:
        try:
            query = takecommand()
            if not query or query.strip().lower() == "none":
                continue

            query = query.lower()

            if 'wikipedia' in query:
                speak("Searching Wikipedia")
                search_term = query.replace("wikipedia", "").strip()
                try:
                    results = wikipedia.summary(search_term, sentences=3)
                    speak("According to Wikipedia")
                    speak(results)
                except Exception:
                    speak("Sorry, I couldn't find information on Wikipedia.")

            elif any(site in query for site in ['youtube', 'google', 'instagram', 'spotify']):
                open_and_search(query)

            elif 'the time' in query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"The time is {strTime}")

            elif 'today date' in query:
                strDate = datetime.datetime.now().strftime("%B %d, %Y and %A")
                speak(f"Today's date is {strDate}")

            elif 'open vs code' in query:
                codepath = "C:\\Users\\vjogd\\OneDrive\\Desktop\Visual Studio Code.lnk"
                if os.path.exists(codepath):
                    speak("Opening Visual Studio Code.")
                    os.startfile(codepath)
                else:
                    speak("VS Code shortcut not found.")

            elif 'bye' in query or 'quit' in query:
                speak("Goodbye!")
                break

        except KeyboardInterrupt:
            speak("Exiting. Goodbye!")
            break
