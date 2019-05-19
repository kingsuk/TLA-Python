import requests

url = "https://dev48697.service-now.com/api/now/table/incident"

querystring = {"active":"True","assigned_to":"sla.admin","state":"2"}

headers = {
    'accept': "application/json",
    'authorization': "Basic YWRtaW46V2FsbnV0YmlyZDEk",
    'cache-control': "no-cache",
    'postman-token': "22325682-f69e-3819-06d8-74a83dafc132"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)