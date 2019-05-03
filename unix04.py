import winspeech
import GoogleSpeechToText as GSTT
import Helper.luis as luis
import ScriptExecutionHelper as SEHelper


def FindServerAndRunScript(serverName):

    if serverName == "linux": 

        hostname = "13.68.228.184"
        username = "acn_root"
        password = "Acn_root1234"
        cmd = 'sh /usr/local/scripts/unix_04_automation_local/unix04_main.sh data 30'
        #cmd = "ls"

        returnValue = SEHelper.ExecuteLinuxScript(hostname,username,password,cmd).strip()
        showOutput = "Optimized to "+returnValue+"%"
        print(showOutput)
        winspeech.say_wait(showOutput)

    elif serverName == "windows":
        print("No windows server registered yet!")
        winspeech.say_wait("No windows server registered yet!")


def RunUnix04(output):
    try:
        print(output)
        entities = output['entities']
        if len(entities) > 0:
            for entity in entities:
                if entity["entity"].lower() == "windows":
                    print("Optimizing the Windows Server file system")
                    winspeech.say_wait("Optimizing the Windows Server file system")
                    FindServerAndRunScript("windows")
                elif entity["entity"].lower() == "linux":
                    print("Optimizing the Linux Server file system")
                    winspeech.say_wait("Optimizing the Linux Server file system")
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