import http.client, urllib.request, urllib.parse, urllib.error, base64
import requests
import json

personGroupId = "tlagroup"
vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/"
headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'ec6542b892234b82b987f6f00a359abf',
}

faceIdList = ["d1eaa492-b409-469a-9617-d047fe5b6aba","3f74c766-a0f9-4837-b755-f26e79d3eede"]

bodyJson = {
    "personGroupId": personGroupId,
    "faceIds": faceIdList,
    "maxNumOfCandidatesReturned": 1,
    "confidenceThreshold": 0.5

}

try:
    identify_url = vision_base_url + "identify"
    responseObj = requests.post(identify_url, headers=headers, data=json.dumps(bodyJson))
    identifyResponse = responseObj.json()
    for identifiedFaces in identifyResponse:
        for candidates in identifiedFaces["candidates"]:
            print(candidates["personId"])
            personId = candidates["personId"]
            person_details_url = vision_base_url + f"persongroups/{personGroupId}/persons/{personId}"
            personDetailsResponse = requests.get(person_details_url, headers=headers)
            print(personDetailsResponse.json()["name"])

except Exception as e:
    print(str(e))