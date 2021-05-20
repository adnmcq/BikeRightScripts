import configparser, csv, os


#https://developer.ebay.com/docs

#inventory API?
#https://developer.ebay.com/api-docs/sell/inventory/resources/methods


import configparser
config = configparser.ConfigParser()
config.read('secret.conf')


client_id = config['EBAY_API_PROD']['client_id']
client_secret = config['EBAY_API_PROD']['client_secret']
dev_id = config['EBAY_API_PROD']['dev_id']
ru_name = config['EBAY_API_PROD']['ru_name']




import requests, urllib, base64

def getAuthToken():
     # AppSettings = {
     #      'client_id':client_id,
     #      'client_secret':client_secret,
     #     #https://forums.developer.ebay.com/questions/3202/how-to-get-runame.html
     #      'ruName':ru_name}

     authHeaderData = client_id + ':' + client_secret
     encodedAuthHeader = base64.b64encode(str.encode(authHeaderData))

     encodedAuthHeader = str(encodedAuthHeader)[2:len(str(encodedAuthHeader)) - 1]
     headers = {
          "Content-Type" : "application/x-www-form-urlencoded",
          "Authorization" : "Basic " + str(encodedAuthHeader)
          }

     body= {
          "grant_type" : "client_credentials",
          "redirect_uri" : ru_name,
         #https://developer.ebay.com/api-docs/static/oauth-scopes.html
          "scope" : "https://api.ebay.com/oauth/api_scope"
      }

     data = urllib.parse.urlencode(body)

     tokenURL = "https://api.ebay.com/identity/v1/oauth2/token"

     response = requests.post(tokenURL, headers=headers, data=data)
     return response.json()


response = getAuthToken()
# print(response)
# response['access_token'] #access keys as required
# response['error_description'] #if errors

token = response['access_token']


from ebaysdk.trading import Connection as Trading
from ebaysdk.exception import ConnectionError

'''
using:
    api = Trading(appid=client_id, devid=dev_id, certid=client_secret, token=token, config_file=None)
    response = api.execute('GetUser', {})

request headers look like:

{'X-EBAY-API-COMPATIBILITY-LEVEL': '837', 
'X-EBAY-API-DEV-NAME': 'd13---436', 
'X-EBAY-API-APP-NAME': 'Ai---a3', 
'X-EBAY-API-CERT-NAME': 'PRD-5---e', 
'X-EBAY-API-SITEID': '0', 'X-EBAY-API-CALL-NAME': 'GetUser', 
'Content-Type': 'text/xml', 'User-Agent': 'eBaySDK/2.2.0 Python/3.7.4 Windows/10', 
'X-EBAY-SDK-REQUEST-ID': '5007---6f6071d66', 'Content-Length': '2079'}

This guy gets same error:

'GetUser: Class: RequestError, Severity: Error, Code: 21916984, Invalid IAF token. IAF token supplied is invalid. '
{'Timestamp': '2021-05-19T15:28:16.391Z', 'Ack': 'Failure', 'Errors': {'ShortMessage': 'Invalid IAF token.', 'LongMessage': 'IAF token supplied is invalid.', 'ErrorCode': '21916984', 'SeverityCode': 'Error', 'ErrorClassification': 'RequestError'}, 'Version': '1191', 'Build': 'E1191_CORE_APISIGNIN_19151597_R1'}


https://forums.developer.ebay.com/questions/41563/error-21916984-invalid-iaf-token-python-sdk.html
'''

try:
    api = Trading(appid=client_id, devid=dev_id, certid=client_secret, token=token, config_file=None)
    response = api.execute('GetUser', {})
    print(response.dict())
    print(response.reply)
except ConnectionError as e:
    print(e)
    print(e.response.dict())

