import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime
import pandas as pd


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'
#CALENDAR_ID='d5us42924d7mpsns1h9c6jlnig@group.calendar.google.com'
CALENDAR_ID='hp3alje1rhm35da9gf7crgqnhs@group.calendar.google.com'

seen = set()


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None




color_map = {
    'Applications': '1',

    'GRE': '2',

    'Data Mining Coursework': '3',

    'Computability Coursework': '4',

    'Networks Revision': '5',

    'Final Year Work': '6',

    'Background Research': '7'
}

description_map = {
    'Applications': 'Write applications to Universities',

    'GRE': 'Do GRE test practice',

    'Data Mining Coursework': 'Do Data Mining Coursework',

    'Computability Coursework': 'Do Computability Coursework',

    'Networks Revision': 'Do Networks revision',

    'Final Year Work': 'Do final year project work',

    'Background Research': 'Do Background Research',
}


def construct_event(service, title,
                    start_hour, start_minute, start_day, end_hour, end_minute,
                    end_day=None, description=None,
                    start_month='11', start_year='2018',
                    end_month=None, end_year=None,
                    reminder_time=5,
                    location="London"):
    if not end_day:
        end_day = start_day
    if not end_month:
        end_month = start_month
    if not end_year:
        end_year= start_year

    color_id = color_map.get(title) or '8'
    description = description_map.get(title) or 'Mystery Event - Ooohhh'

    event = {
        'summary': str(title),
        'location': str(location),
        'description': str(description),
        'start': {
            'dateTime': '{}-{:0>2}-{:0>2}T{:0>2}:{:0>2}:00'.format(start_year, start_month, start_day, start_hour, start_minute),
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': '{}-{:0>2}-{:0>2}T{:0>2}:{:0>2}:00'.format(end_year, end_month, end_day, end_hour, end_minute),
            'timeZone': 'UTC',
        },
        'recurrence': [],
        'attendees': [],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': reminder_time},
            ],
        },
        'colorId': color_id
    }

    event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()

    print("Constructed event: %s" % event['summary'])




def process_item(service, item):
    print("Processing calander event: ", item['summary'])
    event_id = item['id']
    event_title = item['summary']

    description_text = "Default Description for Revision Event"
    colour_id = item.get('colorId', '1')


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

credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
service = discovery.build('calendar', 'v3', http=http)



retrieved = None
#    retrieved = main()
timetable = pd.read_csv('~/Documents/Midterm Plan - 2018 - Sheet2.csv')


last_date = None
twelve_seen = False
for index, row in timetable.iterrows():
    time_text = row['Time'].split("-")
    ((start_hour, start_minute), (end_hour, end_minute)) = [time.strip().split(":") for time in time_text]
    start_hour = int(start_hour)
    start_minute = int(start_minute)
    end_hour = int(end_hour)
    end_minute = int(end_minute)
    print("Considering Event {}:{} - {}:{}".format(start_hour, start_minute, end_hour, end_minute))

    if not (start_hour == 12 and end_hour == 1):
        continue
    end_hour += 12

    print("Constructing Event {}:{} - {}:{}".format(start_hour, start_minute, end_hour, end_minute))

    current_start_date = datetime.datetime(2018, 11, 10, start_hour, start_minute)
    current_end_date = datetime.datetime(2018, 11, 10, end_hour, end_minute)
    reminder_time = 5
    if last_date:
        delta = current_start_date - last_date
        reminder_time = min(delta.seconds // 60, 60)

    last_date = current_end_date

    for (day, date) in zip(
            ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            [5, 6, 7, 8, 9, 10, 11],
    ):
        construct_event(service, row[day], start_hour, start_minute, date, end_hour, end_minute, reminder_time=reminder_time)




