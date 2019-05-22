import pyttsx3

def say_wait(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say("Hello World!")
    engine.runAndWait()
    engine.stop()
    
    