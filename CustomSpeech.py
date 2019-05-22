import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 150) 
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def say_wait(text):
    
    engine.say(text)
    engine.runAndWait()
    #engine.stop()
    
    