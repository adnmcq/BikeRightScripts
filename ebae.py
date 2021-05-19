import configparser, csv, os


#https://developer.ebay.com/docs

#inventory API?
#https://developer.ebay.com/api-docs/sell/inventory/resources/methods


import configparser
config = configparser.ConfigParser()
config.read('secret.conf')


ebay_user = config['EBAY']['username']
ebay_pass = config['EBAY']['password']

'''
Ebay does Oauth2 which is a nightmare and ebay docs are terrible

This might show how you can get an Auth token:
https://stackoverflow.com/questions/44046855/getting-an-ebay-oauth-token

#Once have an auth token might be able to use this API wrapper:
https://github.com/timotheus/ebaysdk-python

particularly Trading module
#https://github.com/timotheus/ebaysdk-python/wiki/Trading-API-Class

#api = Trading(appid="YOUR_APPID", devid="YOUR_DEVID", certid="YOUR_CERTID", token="YOUR_AUTH_TOKEN", config_file=None)

#dev_id, app_id and cert_id will HOPEFULLY be associated with my dev account
#token HOPEFULLY from above 'getting-an-ebay-token'

#from horses mouth: https://developer.ebay.com/api-docs/static/oauth-client-credentials-grant.html
#BUT what are client ID and Client Secret???
#I think they are the app_id and the cert_id

#then how linked to bikeright
   
#https://developer.ebay.com/api-docs/static/creating-edp-account.html    ??


?????
My app prob needs to be hosted, so
https://young-bayou-44042.herokuapp.com/
'''


import requests, urllib, base64

def getAuthToken():
     AppSettings = {
          'client_id':'<client_id>',
          'client_secret':'<client_secret>',
         #https://forums.developer.ebay.com/questions/3202/how-to-get-runame.html
          'ruName':'<ruName>'}

     authHeaderData = AppSettings['client_id'] + ':' + AppSettings['client_secret']
     encodedAuthHeader = base64.b64encode(str.encode(authHeaderData))

     headers = {
          "Content-Type" : "application/x-www-form-urlencoded",
          "Authorization" : "Basic " + str(encodedAuthHeader)
          }

     body= {
          "grant_type" : "client_credentials",
          "redirect_uri" : AppSettings['ruName'],
         #https://developer.ebay.com/api-docs/static/oauth-scopes.html
          "scope" : "https://api.ebay.com/oauth/api_scope"
      }

     data = urllib.parse.urlencode(body)

     tokenURL = "https://api.ebay.com/identity/v1/oauth2/token"

     response = requests.post(tokenURL, headers=headers, data=data)
     return response.json()


response = getAuthToken()
print(response)
response['access_token'] #access keys as required
response['error_description'] #if errors

