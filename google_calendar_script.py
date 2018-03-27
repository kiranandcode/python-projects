import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'
CALENDAR_ID='d5us42924d7mpsns1h9c6jlnig@group.calendar.google.com'
seen = set()

def process_item(service, item):
    print("Processing calander event: ", item['summary'])
    event_id = item['id']
    event_title = item['summary']
    
    description_text = "Default Description for Revision Event"
    colour_id = item.get('colorId', '1')

    colour_map = {
        'Computer Arch': '1',

        'Databases': '2',

        'Maths Calculus': '3',

        'Logic': '4',

        'Maths Finance': '5',

        'Compilers': '6',

        'Fitbit Integration': '7'
        }

    description_map = {
        'Maths Statistics': 'Write flashcard notes from Course and Re-do Worksheets and do flashcards',

        'Computer Arch': 'Write full notes from course slides and personal notes, then do flashcards',

        'Databases': 'Do Flashcards',

        'Maths Calculus': 'Write flashcard notes from course then do flashcards',

        'Logic': 'Write full notes from course, finish flashcards, do worksheets, then do flashcards',

        'Maths Finance': 'Write full notes from course, finish flashcards, then do flashcards',

        'Compilers': 'Write flashcards for course then do worksheet exercises',

        'Fitbit Integration': 'Implement system before the 6th'
        }

    colour_id = colour_map.get(event_title, colour_id)
    description_text = description_map.get(event_title, description_text)

    item['description'] = description_text
    item['colorId'] = colour_id

    service.events().update(calendarId=CALENDAR_ID, eventId=event_id, body=item).execute()

def process_item2(service, item):
    dir(item)
    print(item.keys())

    
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
                                   'calendar-python-quickstart.json')
    secret_path = os.path.join(credential_dir,
                                   CLIENT_SECRET_FILE)

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(secret_path, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=1000, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    retrieved = service.events().list(calendarId=CALENDAR_ID).execute()

    items = retrieved['items']

    for item in items:
        process_item(service, item)

    for i in seen:
             print("'{}': '',\n".format(i))

    return service.colors().get()
#    if not events:
#       print('No upcoming events found.')
#    for event in events:
#        start = event['start'].get('dateTime', event['start'].get('date'))
#        print(start, event['summary'])

retrieved = None
if __name__ == '__main__':
    retrieved = main()
