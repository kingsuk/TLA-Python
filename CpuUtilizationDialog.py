import ScriptExecutionHelper as SEHelper
import CustomSpeech as winspeech
import GoogleSpeechToText as GSTT
import Helper.luis as luis

def FindServerAndRunScript(serverName):

    if serverName == "linux": 

        hostname = "139.59.90.136"
        username = "root"
        password = "Splyking1"
        cmd = './cpu_usage'

        returnValue = SEHelper.ExecuteLinuxScript(hostname,username,password,cmd)
        print(returnValue)
        winspeech.say_wait(returnValue)

    elif serverName == "windows":
        print("No windows server registered yet!")
        winspeech.say_wait("No windows server registered yet!")


def FindCpuUtilization(output):
    try:
        print(output)
        entities = output['entities']
        if len(entities) > 0:
            for entity in entities:
                if entity["entity"].lower() == "windows":
                    print("Getting Cpu Utilization of Windows Server")
                    winspeech.say_wait("Getting Cpu Utilization of Windows Server")
                    FindServerAndRunScript("windows")
                elif entity["entity"].lower() == "linux":
                    print("Getting Cpu Utilization of Linux Server")
                    winspeech.say_wait("Getting Cpu Utilization of Linux Server")
                    FindServerAndRunScript("linux")
        else:
            print("Please provide the server name.")
            winspeech.say_wait("please provide the server name")
            speechResult = GSTT.getSpeechToText()
            print(output["query"])
            luisOutput = luis.AnalyseIntent(str(output['query'])+" of "+speechResult)
            FindCpuUtilization(luisOutput)

    except Exception as e:
        print("Error in CpuUtilizationDialog "+str(e))
    