import requests
import CustomSpeech as winspeech
import GoogleSpeechToText as GSTT
import Unix04Dialog as Unix04
import inflect
import WriteToFile as WTF
import OutputHelper as OH
import json

p = inflect.engine()

# snowUserId = "admin"
# snowPassword = "Walnutbir1$"

Confirmation = {
    "confirm" : True,
    "cancle": False,
    "yes" : True,
    "no" : False,
    "approve" : True,
    "yes please": True
}

def GetIncidentsFromShow():
    url = "https://dev48697.service-now.com/api/now/table/incident"

    querystring = {"active":"True","assigned_to":"sla.admin","state":"2"}

    headers = {
        'accept': "application/json",
        'authorization': "Basic YWRtaW46V2FsbnV0YmlyZDEk",
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    #print(response.json())
    return response.json()['result']

def MarkIncidentAsResoved(incident):
    url = f"https://dev48697.service-now.com/api/now/table/incident/{incident['sys_id']}"

    workLog = WTF.ReadStringFromFile("ScriptOutputLog.txt")

    #payload = "{\"state\": \"6\"},\"work_notes\": \"Hey \\n hi\""
    payload = {
        "state": "6",
        "work_notes" : workLog
    }
    headers = {
        'accept': "application/json",
        'authorization': "Basic YWRtaW46V2FsbnV0YmlyZDEk",
        'content-type': "application/json",
        }

    response = requests.request("PUT", url, data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        OH.OutputHelper("The incident is successfully resolved.")


def MarkResoveConfirmation(incident):
    
    snowActionConfirmation = OH.AskForInput("Do you want to mark this incident as resolved?")

    if snowActionConfirmation in Confirmation:
        if Confirmation[snowActionConfirmation]:
            MarkIncidentAsResoved(incident)
        else:
            OH.OutputHelper("Okay, keeping the incident open.")
            
    else:
        OH.OutputHelper(f"{snowActionConfirmation} is an invalid choice.")
        MarkResoveConfirmation(incident)

def TryResolvingIncident(incident):
    
    incidentNameList = incident["short_description"].split()
    resolveType = incidentNameList[0]
    if resolveType == "UNX04":
        resolveFileSystemName = incidentNameList[3]
        serverName = incident["description"]

        resolveText = f"Starting {resolveType} on server {serverName}"
        WTF.ChangeLogOnly(resolveText)
        WTF.WriteToCurrentJson(resolveText,"service-now-single",[incident])
        OH.OutputHelper(resolveText)
        WTF.WriteStringToFile("","ScriptOutputLog.txt")
        Unix04.StartWorkFlowForLinuxWithoutFileSystemName(resolveFileSystemName)
        MarkResoveConfirmation(incident)
    else:
        OH.OutputHelper("Sorry I cannot resove this incident, You have to do it manually.")

def AskForActionOnIncident(incident):

    OH.OutputHelper("Short Description: "+incident["short_description"])
    snowActionConfirmation = OH.AskForInput("Do you want to take action on this incident?")

    if snowActionConfirmation in Confirmation:
        if Confirmation[snowActionConfirmation]:
            #WTF.WriteToCurrentJson("Incident Details","service-now-single",incident)
            TryResolvingIncident(incident)
        else:
            OH.OutputHelper("Okay")
            
    else:
        OH.OutputHelper(f"{snowActionConfirmation} is an invalid choice.")
        AskForActionOnIncident(incident)

def GetIncidentsCounts(incidents):
    countString= ""

    if len(incidents) == 0:
        countString = f"You don't have any incidents assigned to you."
    elif len(incidents) == 1:
        countString = f"You have {len(incidents)} active incident."
    else:
        countString = f"You have {len(incidents)} active incidents."

    return countString
    

def ReadSnow(output):
    incidents = GetIncidentsFromShow()

    countString = GetIncidentsCounts(incidents)
    
    WTF.ChangeHeaderOnly(countString)
        
    print(countString)
    winspeech.say_wait(countString)

    WTF.WriteToCurrentJson(countString,"service-now-all-tickets",incidents)

    dynamicCount = 1
    for incident in incidents:

        currentIncidents = GetIncidentsFromShow()
        currentIncidentCountsString = GetIncidentsCounts(currentIncidents)
        WTF.WriteToCurrentJson(currentIncidentCountsString,"service-now-all-tickets",currentIncidents)
        OH.OutputHelper(p.ordinal(dynamicCount)+" Incident")
        OH.OutputHelper("Incident number "+incident["number"])
        AskForActionOnIncident(incident)
        dynamicCount = dynamicCount + 1
        
    OH.OutputHelper("Please let me know if I can help you with anything else.")

#ReadSnow("output")