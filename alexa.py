import speech_recognition as sr
import pyttsx3
import webbrowser
from youtube_search import YoutubeSearch

engine = pyttsx3.init()

name = "alex"
called = False

def main():
    while True:
        com = ask("Escutando", False)
        interpret(com)

def speak(text: str):
    engine.say(text)
    engine.runAndWait()

def ask(question: str, speakLoud=True):
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        
        print(question)
        
        if speakLoud:
            speak(question)
        
        audio = r.listen(source)
        
        try:
            text = r.recognize_google(audio, language="pt-br")
            
            return text
        except Exception:
            print("Não entendi.")
            
            if speakLoud:
                speak("Não entendi")

def interpret(command):
    if command == None:
        return
    
    global called
    
    com = command.lower()
    
    if name in com:
        called = True
        
        print("Pois não?")
        speak("Pois não?")
    
    if called:
        if "tudo bem" in com:
            res = ask("Sim, e você?")
            
            if "sim" in res or "também" in res:
                print("Que bom.")
                speak("Que bom.")
            
            elif "não" in res:
                print("Que pena.")
                speak("Que pena.")
            
            called = False
        
        if "cancela" in com or "anula" in com:
            print("Cancelado.")
            speak("Cancelado")
            
            called = False
        
        if "toca" in command or "canta" in command:
            start_len = command.index("toca") + len("toca")
            music = command[start_len:]
            dictio = get_youtube_search_dict(music)
            url = get_video_url(music)
            
            print("Reproduzindo " + dictio[0].get("title") + " no YouTube.")
            speak("Reproduzindo " + dictio[0].get("title") + " no YouTube.")
            
            webbrowser.open(url, new=1)
            
            called = False

# Functions

def get_video_url(search):
    results = YoutubeSearch(search, max_results=10).to_dict()
    
    return "https://youtube.com/watch?v=" + results[0].get("id") ## exception

def get_youtube_search_dict(search):
    return YoutubeSearch(search, max_results=10).to_dict()

# ------------------------------------------------

if __name__ == "__main__":
    main()
