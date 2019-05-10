import Helper.luis as luis
import winspeech
import speech_recognition as sr
import GoogleSpeechToText as GSTT
import config
import CpuUtilizationDialog as CpuDialog
import FileUsageDialog as FUD
import Unix04Dialog as unix04

# def WriteEmailParser(output):
#     entities = output['entities']
#     recipientNameInput = ""
#     if len(entities) > 0:
#         entity = entities[0]["entity"].lower()
#         recipientNameInput = entity
#     else:
#         print("Please provide the recipient name: ")
#         winspeech.say("Please provide the recipient name: ")
#         recipientNameInput = input(" : ")
#     OF.CreateMail("","",recipientNameInput)



def ParseIntent(output):

    try:
        topScoringIntent = output['topScoringIntent']['intent']
        print(topScoringIntent)

        if topScoringIntent == "CpuUtilization":
            CpuDialog.FindCpuUtilization(output)
        elif topScoringIntent=="GreetingIntent":
            winspeech.say_wait("Hi, how can I help you today?")
        elif topScoringIntent == "FileSystemUsage":
            FUD.FindFileSystemUsage(output)
        elif topScoringIntent == "Unix04":
            unix04.RunUnix04(output)

        # if topScoringIntent=="openApplication":
        #     AHD.OpenApplicationParser(output)
        # # elif topScoringIntent=="writeMail":
        # #     WriteEmailParser(output)
        # elif topScoringIntent=="showMeetings":
        #     OD.ShowMeetings(output)
        # elif topScoringIntent=="freeSlots":
        #     OD.FreeSlots(output)
        # elif topScoringIntent=="Reminder.Create":
        #     RD.CreateReminderDialog(output)
        # elif topScoringIntent == "Reminder.Find":
        #     RD.FindReminders(output)
        # elif topScoringIntent == "writeMail":
        #     OD.CreateEmail(output)


        
    except Exception as e:
        print("Error in intent parsing "+str(e))

while True:
    if config.voiceEnable == True:
        speechResult = GSTT.getSpeechToText()
    else:
        speechResult = input(" : ")
    
    if speechResult!="":
        output = luis.AnalyseIntent(speechResult)
        if str(output) == "{'statusCode': 404, 'message': 'Resource not found'}":
            print("Luis error")
            output = luis.AnalyseIntent(speechResult)
        else: 
            print(output)
        ParseIntent(output)