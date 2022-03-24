from __future__ import print_function

import datetime, sys
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import pytz
from tzlocal import get_localzone

import tui

# Permissions for using the calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']
# User credentials file
token_file = os.path.join(sys.path[0], "token.json")
creds_file = os.path.join(sys.path[0], "credentials.json")
conf = os.path.join(sys.path[0], "calcli.conf")
dateformat = ""
tz = get_localzone()


def g_createEventInteractive(service):
    title = ""
    done = 0
    print(dateformat)
    while done == 0:
        print(dateformat)
        if dateformat == "1":
            userDate = input("Event Date (e.g. '01 06 2022' for the 1st of June, 2022): \n")
            try:
                uDate = str(datetime.strptime(userDate, "%d %m %Y"))[:1-10]
                uDate = uDate.replace("-", "")
                done = 1
            except ValueError:
                print("Bad formatting, Please retry.\n")
        else:
            userDate = input("Event Date (e.g. '06 01 2022' for the 1st of June, 2022): \n")
            try:
                uDate = str(datetime.strptime(userDate, "%m %d %Y"))[:1-10]
                uDate = uDate.replace("-", "")
                done = 1
            except ValueError:
                print("Bad formatting, Please retry.\n")
    # Start Time
    done = 0
    while done == 0:
        userStartTime = input("Start time (e.g. '09:30' for 10:30AM or '20:45' for 8:45PM): ")
        try:
            uST = userStartTime.split(":")
            if len(uST[0]) < 2:
                uST[0] = "0" + uST[0]
            int(uST[0]) < 25 == True
            int(uST[1]) < 61 == True
            done = 1
        except Exception as e:
            print(e)
            print("Bad formatting, Please retry.\n")
    # End Time
    done = 0
    while done == 0:
        userEndTime = input("End time (e.g. '10:30' for 10:30AM or '20:45' for 8:45PM): ")
        try:
            uET = userEndTime.split(":")
            if len(uET[0]) < 2:
                uET[0] = "0" + uET[0]
            if int(uET[0]) >= int(uST[0]):
                pass
                if int(uET[1]) >= int(uST[1]):
                    pass
                else:
                    raise Exception("Warning: event ending before start time!")
            else:
                raise Exception("Warning: event ending before start time!")
            int(uST[0]) < 25 == True
            int(uST[1]) < 61 == True
            done = 1
        except Exception as e:
            print(e)
            print("Bad formatting, Please retry.\n")
    # Description
    userDesc = input("Event description: ")
    try:
        start = "" + str(uST[0]) + str(uST[1])
        end = "" + str(uET[0]) + str(uET[1])
        calcli.createEvent(uDate, start, end, userDesc)
        print("Event created.\n")
    except Exception as e:
        print("Error:\n" + str(e) + "\n")
    
    event = {
        'summary': title,
        #'location': '800 Howard St., San Francisco, CA 94103',
        'description': '',
        'start': {
            'dateTime': '2022-04-28T09:00:00-07:00',
            'timeZone': tz,
        },
        'end': {
            'dateTime': '2022-04-28T17:00:00-07:00',
            'timeZone': tz,
        },
        #'recurrence': [
        #    'RRULE:FREQ=DAILY;COUNT=2'
        #],
        #'attendees': [
        #    {'email': 'lpage@example.com'},
        #    {'email': 'sbrin@example.com'},
        #],
        #'reminders': {
        #    'useDefault': False,
        #    'overrides': [
        #    {'method': 'email', 'minutes': 24 * 60},
        #    {'method': 'popup', 'minutes': 10},
        #    ],
        #},
        }
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))
    # NYI


def g_deleteEventInteractive():
    pass
    # NYI


def g_sync_OfflinetoGoogle():
    pass
    # NYI


def g_sync_GoogleToOffline():
    pass
    # NYI

# List all upcoming events from Offline calendar and then Google Events
def g_listUpcomingInteractive(n, service):
    tui.listUpcomingInteractive(n)
    print("(Online):")
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    events_result = service.events().list(calendarId = "primary", 
        timeMin = now,
        maxResults = n, 
        singleEvents = True,
        orderBy = "startTime").execute()
    events = events_result.get("items", [])
    if not events:
        print('No Google Calendar Events.')
        return   
    # Prints the start and name of the next 'n' events
    eventCounter = 1
    for event in events:
        # format the number and appropriate whitespace
        if eventCounter < 10:
            item = "  " + str(eventCounter) + "      "
        elif eventCounter < 100:
            item = " " + str(eventCounter) + "      "
        else:
            item = str(eventCounter) + "      "
        # format the date from file, remove time then split by [YYYY], [MM], [DD]
        fDate = event["start"].get("dateTime")[:1-11].split("-")
        # reform the list, reversing the element order whilst adding '-' between
        item += fDate[2][:2] + "-" + fDate[1] + "-" + fDate[0] + "    "
        # format and store the start and end times from file
        itemStartTime = event["start"].get("dateTime")[11:16]
        itemEndTime = event["end"].get("dateTime")[11:16]
        # add formatted times and description
        item += "(" + itemStartTime + " - " + itemEndTime + ")    " + event["summary"]
        print(item)
        eventCounter += 1
        if eventCounter > n:
            break


def g_menuInteractive(service):
    tui.clear()
    tui.calcli.sortEvents()
    g_listUpcomingInteractive(3, service)
    print("\n\n" + tui.help_text)
    
    # user input menu
    done = 0
    while done == 0:
        userInput = input("\n>  ")
        if userInput == "exit":
            done = 1
            exit()
        elif userInput == "help":
            # print help dialog
            help()
        elif userInput == "n":
            # new event
            g_createEventInteractive(service)
            tui.calcli.sortEvents()
        elif userInput == "l":
            # list events
            g_listUpcomingInteractive(1000, service)
        elif userInput == "d":
            # delete/edit events
            tui.deleteEventsInteractive()
        elif userInput == "c":
            # check calendar
            tui.drawCalInteractive()
        else:
            print("Unrecognised command, type 'help' for a list of commands.")

# initialise a calendar and then call menu function
def main():
    creds = None
    # load credentials from a file if already existing
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    # If there are no (valid) credentials available, prompt for user login.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
            creds = flow.run_local_server(port = 0)
        # Save the credentials for the next run
        with open(token_file, "w") as token:
            token.write(creds.to_json())
    
    # attempt to create a calendar instance, abort if there is an API error
    try:
        service = build("calendar", "v3", credentials = creds)
    # throw an error if there are connection issues to API
    except HttpError as error:
        print('An error occurred: %s' % error)
    try:
        with open(conf, "r") as confFile:
            for line in confFile:
                if line[:7] == "datefmt":
                    dateformat = line.split(" ")
                    dateformat = dateformat[1]
    except Exception as e:
        print(e)
        exit(1)
    g_menuInteractive(service)



if __name__ == '__main__':
    main()