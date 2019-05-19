import requests
import json
import os
import FaceRecognitionConfig as FRC

#datasets = "datasets"
subscription_key = FRC.subscription_key
assert subscription_key
vision_base_url = FRC.vision_base_url
personGroupId = FRC.personGroupId
#name = "Arindam"
#userData = "arindam.f.ghosh@accenture.com"

headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': subscription_key,
        }

headerWithMedia = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-Type': 'application/octet-stream'
    }

def RegisterNewPerson(groupId,name,userData):
    nameRegisterUrl = vision_base_url + "persongroups/"+groupId+"/persons"

    

    bodyJson = {
        "name": name,
        "userData": userData
    }

    userNameRegisterResponse = requests.post(nameRegisterUrl, headers=headers, data=json.dumps(bodyJson))
    
    print(userNameRegisterResponse.json())

    if userNameRegisterResponse.status_code == 200:
        personId = userNameRegisterResponse.json()["personId"]
        return personId
    else:
        print("Cool Down")
        return RegisterNewPerson(groupId,name,userData)

    

#RegisterNewPerson(personGroupId,name,userData)
def AddFaceByPersonId(groupId,personId,image_path):

    image_data = open(image_path, "rb").read()
    addFaceUrl = vision_base_url + f"persongroups/{groupId}/persons/{personId}/persistedFaces"
    
    response = requests.post(addFaceUrl, headers=headerWithMedia, data=image_data)
    print(response.json())

    if response.status_code == 200:
        print("success")
    else:
        print("cool down")
        return AddFaceByPersonId(groupId,personId,image_path)

def GetImageMaps(folderName):
    for (subdirs, dirs, files) in os.walk(folderName): 
        for subdir in dirs: 
            personId = RegisterNewPerson(personGroupId,subdir,f"{subdir}@accenture.com")
            print(f"training {subdir} folder")
            subjectpath = os.path.join(folderName, subdir) 
            for filename in os.listdir(subjectpath): 
                path = subjectpath + '/' + filename 
                AddFaceByPersonId(personGroupId,personId,path)

    trainling_url = vision_base_url + f"persongroups/{personGroupId}/train"

    trainingResponse = requests.post(trainling_url, headers=headers)

    print(trainingResponse)

GetImageMaps("CognitiveFace/datasets")