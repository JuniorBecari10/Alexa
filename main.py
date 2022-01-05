# Deprecated. Use alexa.py instead!

from youtube_search import YoutubeSearch
import webbrowser
import speech_recognition as sr
import pyttsx3

name = "alex" # talvez entenda "Alex" ao invés de "Alexa"
engine = pyttsx3.init()

talked_with_me = False

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        
        print("Escutando...")
        #speak("Escutando")
        
        #r.pause_threshold = 1
        audio = r.listen(source)
    
    try:
        print("Recognizing...")
        command = r.recognize_google(audio, language='pt-br')
        print("Você disse: " + command)
        
        return command
    except Exception:
        print("Não entendi.")
        speak("Não entendi.")

def parse_command(com):
    if com == None:
        return
    
    global talked_with_me
    command = com.lower()
    
    if name in command:
        talked_with_me = True # ùnico comando que não precisa ser chamado
        
        print("Pois não?")
        speak("Pois não?")
    
    if talked_with_me:
        if "toca" in command:
            start_len = command.index("toca") + len("toca")
            music = command[start_len:]
            dictio = get_youtube_search_dict(music)
            url = get_video_url(music)
            
            print("Tocando " + dictio[0].get("title"))
            speak("Tocando " + dictio[0].get("title"))
            
            webbrowser.open(url, new=1)
            
            talked_with_me = False
        
        if "cancela" in command:
            talked_with_me = False
            print("Cancelado.")
        
        if "tudo bem" in command or "tudo bom" in command:
            print("Sim.")
            speak("Sim.")
            
            talked_with_me = False

def get_video_url(search):
    results = YoutubeSearch(search, max_results=10).to_dict()
    
    return "https://youtube.com/watch?v=" + results[0].get("id") ## exception

def get_youtube_search_dict(search):
    return YoutubeSearch(search, max_results=10).to_dict()

if __name__ == "__main__":
    while True:
        command = take_command()
        parse_command(command)
