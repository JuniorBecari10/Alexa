import speech_recognition as sr
import pyttsx3
import webbrowser
from youtube_search import YoutubeSearch
import wikipedia as wiki
import keyboard
import subprocess
import thread6 as thread
import sys
import os
import random
from datetime import date

boas_vindas = ["Pois não?", "Boah", "Qual é?", "Suave?", "Diga.", "Iaê!", "O que foi?", "Chora!"]

engine = pyttsx3.init()

meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

niver = "08/01/2022"

name = "lex" # talvez entende Alex ou Lexa ou Lex
called = False
wiki.set_lang("pt")

def main():
    #thread.run_threaded(quit)
    
    while True:
        com = ask("Escutando", False)
        interpret(com)

@thread.threaded()
def quit():
    while True:
        if keyboard.is_pressed("q"):
            print("Resetando...")
            main()
            break
            #sys.exit()
            #subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:])

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
            print("Você disse: " + text)
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
        
        frase = random.choice(boas_vindas)
        
        print(frase)
        speak(frase)
    
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
            start_len = com.index(" ")
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
        
        if "dia" in com and "hoje" in com:
            today = date.today()
            form = today.strftime("%d/%m/%Y") # 08/01/2022 (por hoje kk)
            
            is_niver = False
            
            if (form == niver):
                is_niver = True
            
            ext = form.replace(form[form.index("/") + 1:form.index("/") + 3], meses[int(form[form.index("/") + 1:form.index("/") + 3]) - 1])
            ext = ext.replace("/", " de ")
            
            speak_ext = ext
            
            if (ext[0] == "0"):
                speak_ext = speak_ext[1:]
            
            print("Hoje é dia " + ext + ".")
            speak("Hoje é dia " + speak_ext + ".")
            
            if (is_niver):
                print("Hoje é o seu aniversário. Parabéns!")
                speak("Hoje é o seu aniversário. Parabéns!")
            

# Functions

def get_video_url(search):
    results = YoutubeSearch(search, max_results=10).to_dict()
    
    return "https://youtube.com/watch?v=" + results[0].get("id") ## exception

def get_youtube_search_dict(search):
    return YoutubeSearch(search, max_results=10).to_dict()

# ------------------------------------------------

if __name__ == "__main__":
    main()
