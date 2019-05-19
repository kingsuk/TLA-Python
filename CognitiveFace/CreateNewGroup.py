import requests

endpoint = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/persongroups/"

groupName = "tlagroup1"

url = endpoint + groupName

payload = '{"name": "tlagroup1","userData": "user-provided data attached to the person group.","recognitionModel": "recognition_02"}'
headers = {
    'ocp-apim-subscription-key': "ec6542b892234b82b987f6f00a359abf",
    'content-type': "application/json"
    }

response = requests.request("PUT", url, data=payload, headers=headers)

print(response.text)