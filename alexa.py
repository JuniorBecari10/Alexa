import speech_recognition as sr
import pyttsx3

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
            print("Sim.")
            speak("Sim")
            
            res = ask("E você?")
            
            if "sim" in res or "também" in res:
                print("Que bom.")
                speak("Que bom.")
            
            called = False

if __name__ == "__main__":
    main()
