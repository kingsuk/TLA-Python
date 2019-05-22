import Helper.luis as luis
import CustomSpeech as winspeech
import speech_recognition as sr
import GoogleSpeechToText as GSTT
import config
import CpuUtilizationDialog as CpuDialog
import FileUsageDialog as FUD
import Unix04Dialog as unix04
import CognitiveFace.FaceDetectAndLogin as FaceLogin
import ReadSnowDialog as ReadSnow
import WriteToFile as WTF

LoginSuccess = False

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
        elif topScoringIntent == "ReadSnow":
            ReadSnow.ReadSnow(output)

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

# authenticationOutput = FaceLogin.CaptureFaceAndStartRecognize()

# if authenticationOutput == None:
#     sayString = f"Authentication failed."
#     print(sayString)
#     winspeech.say_wait(sayString)
# else:
#     sayString = f"Authentication successful. Welcome {authenticationOutput}."
#     LoginSuccess = True
#     winspeech.say_wait(sayString)
#     winspeech.say_wait("Please wait")
#     WTF.OpenUiApplication()
#     print(sayString)
#     WTF.ChangeLogOnly(sayString)
#     winspeech.say_wait("How can I help you today")
    


LoginSuccess = True
WTF.OpenUiApplication()
winspeech.say_wait("Hi I am Buddy, How can I help you today")
while LoginSuccess:
    
    WTF.WriteToCurrentJson("How can I help you?","",[])
    
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