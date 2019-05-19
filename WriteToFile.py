import json
import os
import psutil    

filePath = r"C:\Users\accenture.robotics\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\buddy.lnk"

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

    WriteToFile(totalJsonData,"currentdata.json")

    # if "Buddy.exe" in (p.name() for p in psutil.process_iter()):
    #     print("Already running closing it")
    #     os.system("TASKKILL /F /IM Buddy.exe")
        
    # os.startfile(filePath)

def OpenUiApplication():
    if "Buddy.exe" in (p.name() for p in psutil.process_iter()):
        print("Already running closing it")
        os.system("TASKKILL /F /IM Buddy.exe")
        
    os.startfile(filePath)

def ChangeHeaderOnly(header):
    with open('currentdata.json') as json_file:  
        data = json.load(json_file)
        data['currentHeader'] = [header]
        WriteToFile(data,"currentdata.json")