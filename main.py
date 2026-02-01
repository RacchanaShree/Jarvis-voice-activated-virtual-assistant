import speech_recognition as sr
import webbrowser
import musicLibrary
import re
import requests
import time
from playsound import playsound
import asyncio
import edge_tts
import os
from client import ask_ai
from dotenv import load_dotenv

EXIT_ASSISTANT = False


recogniser = sr.Recognizer()

load_dotenv()
newsapi = os.getenv("NEWS_API_KEY")



def speak(text):
    async def _speak():
        print("Jarvis :", text)
        filename = "jarvis.mp3"

        communicate = edge_tts.Communicate(
            text,
            voice="en-IN-NeerjaNeural"
        )

        await communicate.save(filename)
        playsound(filename)

        # 🔥 RELEASE FILE LOCK
        os.remove(filename)

    asyncio.run(_speak())       #creates and manages event loop 

def speak_summary_only(text):
    async def _speak():
        filename = "jarvis.mp3"

        communicate = edge_tts.Communicate(
            text,
            voice="en-IN-NeerjaNeural",
            rate="+15%",
            pitch="+2Hz"
        )

        await communicate.save(filename)
        playsound(filename)
        os.remove(filename)

    asyncio.run(_speak())

def extract_summary(text):
    if "SUMMARY:" in text:
        return text.split("SUMMARY:", 1)[1].strip()
    return "I have shared the details on the screen."

def processCommand(c):
    
    global EXIT_ASSISTANT

    exit_phrases = [
        "exit",
        "quit",
        "stop",
        "stop listening",
        "i am done",
        "i'm done",
        "bye jarvis",
        "shutdown"
    ]

    if any(phrase in c.lower() for phrase in exit_phrases):
        speak("Okay. Shutting down. Have a good day.")
        EXIT_ASSISTANT = True
        return

    elif  "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif  "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif  "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif  "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
       
              
        song = c.lower()
        song = song.replace("play", "")
        song = re.sub(r'[^a-z0-9 ]', '', song)      #re.sub(pattern, replacement, string) -"Find pattern in string and replace it with replacement" where r is raw string

        song = song.strip()
    
        print("FINAL SONG:", repr(song))
        print("AVAILABLE SONGS:", musicLibrary.music.keys())

        if song in musicLibrary.music:
            webbrowser.open(musicLibrary.music[song])
        else:
            speak("Song not found")

    elif "news" in c.lower():
        url = "https://newsdata.io/api/1/latest"
        params = {
            "apikey": newsapi,
            "language": "en"
        }

        r = requests.get(url, params=params)

        if r.status_code == 200:
            data = r.json()

            articles = data.get("results", [])

            if not articles:
                speak("No news found")
                return

            speak("Here are the latest headlines")

            for article in articles[:3]:   # limit to 3 headlines
                title = article.get("title")
                if title:                  
                    speak(title)
                    
        else:
            speak("Failed to fetch news")

    else:
        ai_response = ask_ai(c)

        # 🖥️ PRINT FULL RESPONSE (NOT SHORTENED)
        print("\n========== AI RESPONSE ==========\n")
        print(ai_response)
        print("\n=================================\n")

        # 🔊 SPEAK ONLY IMPORTANT POINTS
        summary = extract_summary(ai_response)
        speak_summary_only(summary)



if __name__ == "__main__":
    speak("Initializing Jarvis...")
    with sr.Microphone() as source:
        print("Calibrating microphone...")
        recogniser.adjust_for_ambient_noise(source, duration=1)

    while not EXIT_ASSISTANT:
        #listen for the wake word "Jarvis"
        # obtain audio from the microphone
      
        print("recognising...")
        try: 
            with sr.Microphone() as source:
                print("Listening...")
                audio = recogniser.listen(source, timeout = 3, phrase_time_limit=3)
            
            word = recogniser.recognize_google(audio)
            print("Wake word : ", word)
            if "jarvis" in word.lower() :
                time.sleep(0.1)
                speak("ya")

                #Listen for command
                #time.sleep(0.3)
                
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = recogniser.listen(source)
                command = recogniser.recognize_google(audio)
                processCommand(command)

        except sr.WaitTimeoutError:
            continue
        except sr.UnknownValueError:
            print("Could not understand audio")
        except Exception as e:
            print("Unexpected error:", e)



