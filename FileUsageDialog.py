import winspeech
import GoogleSpeechToText as GSTT
import Helper.luis as luis
import ScriptExecutionHelper as SEHelper


def FindServerAndRunScript(serverName):

    if serverName == "linux": 

        hostname = "40.114.70.147"
        username = "acn_root"
        password = "Acn_root1234"
        cmd = 'sh /usr/local/scripts/unix_04_automation_local/fs_actual_percentage.sh /data'
        #cmd = "ls"

        returnValue = SEHelper.ExecuteLinuxScript(hostname,username,password,cmd).strip()
        showOutput = "Used: "+returnValue+"%"
        print(showOutput)
        winspeech.say_wait(showOutput)

    elif serverName == "windows":
        print("No windows server registered yet!")
        winspeech.say_wait("No windows server registered yet!")


def FindFileSystemUsage(output):
    try:
        print(output)
        entities = output['entities']
        if len(entities) > 0:
            for entity in entities:
                if entity["entity"].lower() == "windows":
                    print("Getting File System Usage of Windows Server")
                    winspeech.say_wait("Getting File System Usage of Windows Server")
                    FindServerAndRunScript("windows")
                elif entity["entity"].lower() == "linux":
                    print("Getting File System Usage of Linux Server")
                    winspeech.say_wait("Getting File System Usage of Linux Server")
                    FindServerAndRunScript("linux")
        else:
            print("Please provide the server name.")
            winspeech.say_wait("please provide the server name")
            speechResult = GSTT.getSpeechToText()
            print(output["query"])
            luisOutput = luis.AnalyseIntent(str(output['query'])+" of "+speechResult)
            FindFileSystemUsage(luisOutput)

    except Exception as e:
        print("Error in FileSystemUsageDialog "+str(e))