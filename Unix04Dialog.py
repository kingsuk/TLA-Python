import winspeech
import GoogleSpeechToText as GSTT
import Helper.luis as luis
import ScriptExecutionHelper as SEHelper

FSActualPercentageUsageScript = "sh /usr/local/scripts/unix_04_automation_local/fs_actual_percentage.sh "
FSDesciptionDialog = "By optimizing the file system, I will archive old log files and notify the concern application owner with the big file list responsible for high utilization. "

FSOptimizationScript = "sh /usr/local/scripts/unix_04_automation_local/fs_extension_deletion_opti.sh 60 "
FSExtensionDialog = "You can extend the file system to bring down the utilization. Please note once file space is extended can't be reverted."

FSExtensionScript = "sh /usr/local/scripts/unix_04_automation_local/unix04_main.sh 60 "

fileSystemTypeList = {
    "root" : "/",
    "data" : "/data",
    "oracle data" : "/oradata",
    "route" : "/"
}

Confirmation = {
    "confirm" : True,
    "cancle": False,
    "yes" : True,
    "no" : False,
    "approve" : True,
    "yes please": True
}

def ExecuteScriptToServer(cmd):
    hostname = "40.76.45.125"
    username = "acn_root"
    password = "Acn_root1234"
    cmd = cmd

    returnValue = SEHelper.ExecuteLinuxScript(hostname,username,password,cmd)
    return returnValue

def AskForInput(message):
    print(message)
    winspeech.say_wait(message)
    userInput = GSTT.getSpeechToText().lower()
    return userInput

def ExtensionConfirmation(FileSystemTypeInput):
    try:
        optimizationReply = AskForInput(f"Are you sure, you want to approve the {fileSystemTypeList[FileSystemTypeInput]} extension action?")

        if optimizationReply in Confirmation:
            if Confirmation[optimizationReply]:
                print("Please wait.")
                winspeech.say_wait("Please wait.")
                print(FSExtensionScript+fileSystemTypeList[FileSystemTypeInput])
                afterOptimizaResult = ExecuteScriptToServer(FSExtensionScript+fileSystemTypeList[FileSystemTypeInput])
                print(afterOptimizaResult)
                winspeech.say_wait(afterOptimizaResult)

            else:
                print("okay")
                winspeech.say_wait("okay")
        else:
            print(f"{optimizationReply} is an invalid choice.")
            winspeech.say_wait(f"{optimizationReply} is an invalid choice.")
            ExtensionConfirmation(FileSystemTypeInput)
    except Exception as e:
        print("Error in ExtensionConfirmation"+str(e))

def OptimaizationConfirmation(FileSystemTypeInput):
    try:
        optimizationReply = AskForInput(f"Are you sure, you want to optimize the {fileSystemTypeList[FileSystemTypeInput]} file system?")
        if optimizationReply in Confirmation:
            if Confirmation[optimizationReply]:
                print("Please wait.")
                winspeech.say_wait("Please wait.")
                print(FSOptimizationScript+fileSystemTypeList[FileSystemTypeInput])
                afterOptimizaResult = ExecuteScriptToServer(FSOptimizationScript+fileSystemTypeList[FileSystemTypeInput])
                print(afterOptimizaResult)
                winspeech.say_wait(afterOptimizaResult)

                if fileSystemTypeList[FileSystemTypeInput] != fileSystemTypeList["root"]:
                    print(FSExtensionDialog)
                    winspeech.say_wait(FSExtensionDialog)
                    ExtensionConfirmation(FileSystemTypeInput)

            else:
                print("okay")
                winspeech.say_wait("okay")
        else:
            print(f"{optimizationReply} is an invalid choice.")
            winspeech.say_wait(f"{optimizationReply} is an invalid choice.")
            OptimaizationConfirmation(FileSystemTypeInput)
    except Exception as e:
        print("Error in OptimaizationConfirmation"+str(e))
    

def StartWorkFlowForLinux():
    
    try:
        FileSystemTypeInput = AskForInput("please specify the file system you want to optimize? Root, Data or Oracle Data")

        if FileSystemTypeInput in fileSystemTypeList:
            currentFileSystemUsage = ExecuteScriptToServer(FSActualPercentageUsageScript+fileSystemTypeList[FileSystemTypeInput])
            print("Please wait.")
            winspeech.say_wait("Please wait.")
            print(currentFileSystemUsage)
            winspeech.say_wait(currentFileSystemUsage)

            print(FSDesciptionDialog)
            winspeech.say_wait(FSDesciptionDialog)

            OptimaizationConfirmation(FileSystemTypeInput)


        else:
            print(f"{FileSystemTypeInput} is an invalid choice.")
            winspeech.say_wait(f"{FileSystemTypeInput} is an invalid choice.")
            StartWorkFlowForLinux()
    except Exception as e:
        print("Error in StartWorkFlowForLinux"+str(e))

def FindServer(serverName):

    if serverName == "linux": 

        StartWorkFlowForLinux()

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
                    FindServer("windows")
                elif entity["entity"].lower() == "linux":
                    #print("Optimizing the Linux Server file system")
                    #winspeech.say_wait("Optimizing the Linux Server file system")
                    FindServer("linux")
        else:
            print("Please provide the server name.")
            winspeech.say_wait("please provide the server name")
            speechResult = GSTT.getSpeechToText()
            print(output["query"])
            luisOutput = luis.AnalyseIntent(str(output['query'])+" of "+speechResult)
            FindFileSystemUsage(luisOutput)

    except Exception as e:
        print("Error in FileSystemUsageDialog "+str(e))