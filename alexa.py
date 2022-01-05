import speech_recognition as sr
import pyttsx3
import webbrowser
from youtube_search import YoutubeSearch
import wikipedia as wiki

engine = pyttsx3.init()

name = "alex"
called = False
wiki.set_lang("pt")

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
        
        if "toca" in com or "canta" in com or "reproduz" in com:
            start_len = command.index("toca") + len("toca")
            music = com[start_len:]
            
            dictio = get_youtube_search_dict(music)
            url = get_video_url(music)
            
            print("Reproduzindo " + dictio[0].get("title") + " no YouTube.")
            speak("Reproduzindo " + dictio[0].get("title") + " no YouTube.")
            
            webbrowser.open(url, new=1)
            
            called = False
        if "pesquisa" in com: # in com and "wikipedia" 
            start_len = 9 # sim, hardcoded
            query = com[start_len:]
            
            print("Significado de " + query + " na Wikipedia:")
            speak("Significado de " + query + " na Wikipedia:")
            
            print(wiki.summary(query))
            speak(wiki.summary(query))
            

# Functions

def get_video_url(search):
    results = YoutubeSearch(search, max_results=10).to_dict()
    
    return "https://youtube.com/watch?v=" + results[0].get("id") ## exception

def get_youtube_search_dict(search):
    return YoutubeSearch(search, max_results=10).to_dict()

# ------------------------------------------------

if __name__ == "__main__":
    main()
