from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime
from datetime import datetime as dt
import sys
import json
import time
from pytz import timezone


try:
	import argparse
	flags = tools.argparser.parse_args([])
except ImportError:
	flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'eManager'

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
		print ("not credentionals")
		os.makedirs(credential_dir)
	credential_path = os.path.join(credential_dir,
								   'calendar-python-quickstart.json')

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
	store.delete()

	return credentials

def main(event):
	"""Shows basic usage of the Google Calendar API.

	Creates a Google Calendar API service object and outputs a list of the next
	10 events on the user's calendar.
	"""
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('calendar', 'v3', http=http)

	start = event.start_date.astimezone(timezone('Europe/Moscow'))
	start = start.__str__()[0:10]
	
	event_body = {
		'summary': event.description,
		'location': event.address,
		'start': {
			'date': start,
		}, 
		'end': {
			'date': start,
		} 
	}

	service.events().insert(calendarId='primary', body = event_body).execute()
