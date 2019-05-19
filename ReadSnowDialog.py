import requests
import winspeech
import GoogleSpeechToText as GSTT
import Unix04Dialog as Unix04
import inflect
import WriteToFile as WTF

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

def AskForInput(message):
    WTF.ChangeHeaderOnly(message)
    print(message)
    winspeech.say_wait(message)
    userInput = GSTT.getSpeechToText().lower()
    
    return userInput

def OutputHelper(targetString):
    print(targetString)
    winspeech.say_wait(targetString)

def MarkIncidentAsResoved(incident):
    url = f"https://dev48697.service-now.com/api/now/table/incident/{incident['sys_id']}"

    payload = "{\"state\": \"6\"}"
    headers = {
        'accept': "application/json",
        'authorization': "Basic YWRtaW46V2FsbnV0YmlyZDEk",
        'content-type': "application/json",
        }

    response = requests.request("PUT", url, data=payload, headers=headers)

    if response.status_code == 200:
        OutputHelper("The incident is successfully resolved.")


def MarkResoveConfirmation(incident):
    
    snowActionConfirmation = AskForInput("Do you want to mark this incident as resolved?")

    if snowActionConfirmation in Confirmation:
        if Confirmation[snowActionConfirmation]:
            MarkIncidentAsResoved(incident)
        else:
            OutputHelper("Okay, keeping the incident open.")
            
    else:
        OutputHelper(f"{snowActionConfirmation} is an invalid choice.")
        MarkResoveConfirmation(incident)

def TryResolvingIncident(incident):
    incidentNameList = incident["short_description"].split()
    resolveType = incidentNameList[0]
    if resolveType == "UNX04":
        resolveFileSystemName = incidentNameList[3]
        serverName = incident["description"]
        OutputHelper(f"Starting {resolveType} on server {serverName}")
        Unix04.StartWorkFlowForLinuxWithoutFileSystemName(resolveFileSystemName)
        MarkResoveConfirmation(incident)
    else:
        OutputHelper("Sorry I cannot resove this incident, You have to do it manually.")

def AskForActionOnIncident(incident):

    OutputHelper("Short Description: "+incident["short_description"])
    snowActionConfirmation = AskForInput("Do you want to take action on this incident?")

    if snowActionConfirmation in Confirmation:
        if Confirmation[snowActionConfirmation]:
            #WTF.WriteToCurrentJson("Incident Details","service-now-single",incident)
            TryResolvingIncident(incident)
        else:
            OutputHelper("Okay")
            
    else:
        OutputHelper(f"{snowActionConfirmation} is an invalid choice.")
        AskForActionOnIncident(incident)

def ReadSnow(output):
    url = "https://dev48697.service-now.com/api/now/table/incident"

    querystring = {"active":"True","assigned_to":"sla.admin","state":"2"}

    headers = {
        'accept': "application/json",
        'authorization': "Basic YWRtaW46V2FsbnV0YmlyZDEk",
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    #print(response.json())
    incidents = response.json()['result']

    countString = ""
    if len(incidents) == 0:
        countString = f"You don't have any incidents assigned to you."
    elif len(incidents) == 1:
        countString = f"You have {len(incidents)} active incident."
    else:
        countString = f"You have {len(incidents)} active incidents."
        
        
    print(countString)
    winspeech.say_wait(countString)

    WTF.WriteToCurrentJson(countString,"service-now-all-tickets",incidents)

    dynamicCount = 1
    for incident in incidents:
        OutputHelper(p.ordinal(dynamicCount)+" Incident")
        OutputHelper("Incident number "+incident["number"])
        AskForActionOnIncident(incident)
        dynamicCount = dynamicCount + 1
        
    OutputHelper("Please let me know if I can help you with anything else.")

#ReadSnow("output")