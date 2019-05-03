import requests

def AnalyseIntent(userInput):
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': '08e66a5c2e024e28963d0b23e1702b15',
    }
    params ={
        # Query parameter
        'q': userInput,
        # Optional request parameters, set to default values
        'timezoneOffset': '0',
        'verbose': 'false',
        'spellCheck': 'false',
        'staging': 'false',
    }

    try:
        r = requests.get('https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/d32c3cee-6e4b-45b7-9c8c-c7d38f5e7985',headers=headers, params=params)
        return r.json()
    except Exception as e:
        return "[Errno {0}] {1}".format(e.errno, e.strerror)
        