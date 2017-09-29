from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import csv

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/people.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/contacts'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'People API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'people.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_contacts():
    contacts = []
    with open('contacts_small.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            #givenName row header has that weird symbol and I'm not sure why
            #if you use the debugger and stop on the line below you can see it
            contacts += [{"names": [{ "givenName": row['ï»¿givenName'], "familyName": row['familyName'] }], "emailAddresses": [{ "value": row['emailAddress'] }]}]
    return contacts


def main():
    """Shows basic usage of the Google People API.
    """
    credentials = get_credentials()
    #force http library to use auth headers
    http = credentials.authorize(httplib2.Http())

    #dynamically build service object from the discovery url
    service = discovery.build('people', 'v1', http=http,
        discoveryServiceUrl='https://people.googleapis.com/$discovery/rest')

    #read contacts from csv file
    contacts = get_contacts()
    #cache service objects
    people = service.people()
    results = []

    #create contact for each line in csv
    for contact in contacts:
        results += [people.createContact(body=contact).execute()]

    for result in results:
        print(result.resourceName)


if __name__ == '__main__':
    main()