import WriteToFile as WTF
import CustomSpeech as winspeech
import GoogleSpeechToText as GSTT

def AskForInput(message):
    WTF.ChangeHeaderOnly(message)
    print(message)
    winspeech.say_wait(message)
    userInput = GSTT.getSpeechToText().lower()
    
    return userInput

def OutputHelper(targetString):
    #WTF.ChangeHeaderOnly(targetString)
    print(targetString)
    winspeech.say_wait(targetString)