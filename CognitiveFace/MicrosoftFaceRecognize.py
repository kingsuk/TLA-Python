import requests
import json
import CognitiveFace.FaceRecognitionConfig as FRC

subscription_key = FRC.subscription_key
assert subscription_key
vision_base_url = FRC.vision_base_url
personGroupId = FRC.personGroupId
image_path = FRC.image_path


def DetectFaceMyImage(personGroupId,image_path):

    image_data = open(image_path, "rb").read()
    #detecting face with temporary id
    analyze_url = vision_base_url + "detect"


    headerWithMedia = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-Type': 'application/octet-stream'
    }
    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,emotion',
        'recognitionModel': 'recognition_02'
    }
    response = requests.post(analyze_url, headers=headerWithMedia, params=params, data=image_data)
    response.raise_for_status()
    analysis = response.json()
    print(analysis)

    faceIdList = []
    for face in analysis:
        print("Temp face id : "+face['faceId'])
        faceIdList.append(face['faceId'])


    #Get Person Id by temporary Id
    bodyJson = {
        "personGroupId": personGroupId,
        "faceIds": faceIdList,
        "maxNumOfCandidatesReturned": 1,
        "confidenceThreshold": 0.5
    }

    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    try:
        identify_url = vision_base_url + "identify"
        responseObj = requests.post(identify_url, headers=headers, data=json.dumps(bodyJson))
        identifyResponse = responseObj.json()
        for identifiedFaces in identifyResponse:
            for candidates in identifiedFaces["candidates"]:
                print("PersonGroup Person Id : "+candidates["personId"])
                personId = candidates["personId"]
                #Get person details by person Id
                person_details_url = vision_base_url + f"persongroups/{personGroupId}/persons/{personId}"
                personDetailsResponse = requests.get(person_details_url, headers=headers)
                print(personDetailsResponse.json()["name"])
                return personDetailsResponse.json()["name"]

    except Exception as e:
        print("error in DetectFaceMyImage "+str(e))

#DetectFaceMyImage(personGroupId,image_path)