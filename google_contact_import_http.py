


import httplib2
from apiclient import errors
from oauth2client.client import OAuth2WebServerFlow
import urllib.parse
import json
# Copy your credentials from the console


CLIENT_ID = '767382404910-4kbfqo75oinv9vhqcb3g5i479u3g9ao8.apps.googleusercontent.com'
CLIENT_SECRET = '4aiqPgmIQgnTWWRSe2jQ1LnU'

OAUTH_SCOPE = 'https://www.googleapis.com/auth/contacts'

# Redirect URI for installed apps
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

# Run through the OAuth flow and retrieve credentials
flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)
authorize_url = flow.step1_get_authorize_url()
print(authorize_url)
code = input('Enter verification code: ').strip()
credentials = flow.step2_exchange(code)

# Create an httplib2.Http object and authorize it with our credentials
http = httplib2.Http()
http = credentials.authorize(http)

resp, content = http.request(
    uri='https://people.googleapis.com/v1/people:createContact',
    method='POST',
    body=json.dumps({ "names": [{ "givenName": "John1", "familyName": "Doe" }], "emailAddresses": [{ "value": "john1.doe@gmail.com" }] }),
)

a = "asdf"