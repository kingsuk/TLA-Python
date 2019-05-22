import json
import os
import psutil    

filePath = r"C:\Users\accenture.robotics\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\buddy.lnk"

def ReadStringFromFile(fileName):
    f = open(fileName,"r")
    contents =f.read()
    return contents

def AppendStringToFile(currentData,fileName):
    f = open(fileName,"a+")
    f.write(currentData)
    f.close()

def WriteStringToFile(data,fileName):
    f = open(fileName,"w+")
    f.write(data)
    f.close()

def WriteToFile(jsonData,fileName):
    with open(fileName, 'w') as outfile:  
            json.dump(jsonData, outfile)
            print("Ok, data is saved")

def WriteToCurrentJson(headerText,dataTypeText,data):
    totalJsonData = {}
    headerList = []
    dataType = []
    headerList.append(headerText)
    dataType.append(dataTypeText)
    totalJsonData["dataType"] = dataType
    totalJsonData["currentHeader"] = headerList
    totalJsonData["currentData"] = data
    totalJsonData["currentLog"] = []

    WriteToFile(totalJsonData,"currentdata.json")

    # if "Buddy.exe" in (p.name() for p in psutil.process_iter()):
    #     print("Already running closing it")
    #     os.system("TASKKILL /F /IM Buddy.exe")
        
    # os.startfile(filePath)

def OpenUiApplication():
    # if "Buddy.exe" in (p.name() for p in psutil.process_iter()):
    #     print("Already running closing it")
    #     os.system("TASKKILL /F /IM Buddy.exe")
        
    os.startfile(filePath)

def ChangeHeaderOnly(header):
    with open('currentdata.json') as json_file:  
        data = json.load(json_file)
        data['currentHeader'] = [header]
        WriteToFile(data,"currentdata.json")

def ChangeLogOnly(log):
    with open('currentdata.json') as json_file:  
        data = json.load(json_file)
        if 'currentLog' not in data:
            data['currentLog'] = [log]
        else:
            data['currentLog'].append(log)
        #data['currentLog'] = [log]
        WriteToFile(data,"currentdata.json")

def HardWriteLogOnly(log):
    with open('currentdata.json') as json_file:  
        data = json.load(json_file)
        data['currentLog'] = [log]
        WriteToFile(data,"currentdata.json")
