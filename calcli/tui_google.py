from __future__ import print_function

import datetime, sys
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import tui

# Permissions for using the calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']
# User credentials file
creds_file = os.path.join(sys.path[0], "token.json")


def g_createEventInteractive():
    pass
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
        item += fDate[2] + "-" + fDate[1] + "-" + fDate[0] + "    "
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
    # tui.clear()
    # g_listEvents(20, service)
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
            tui.createEventInteractive()
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
    if os.path.exists(creds_file):
        creds = Credentials.from_authorized_user_file(creds_file, SCOPES)
    # If there are no (valid) credentials available, prompt for user login.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port = 0)
        # Save the credentials for the next run
        with open(creds_file, "w") as token:
            token.write(creds.to_json())
    
    # attempt to create a calendar instance, abort if there is an API error
    try:
        service = build("calendar", "v3", credentials = creds)
    # throw an error if there are connection issues to API
    except HttpError as error:
        print('An error occurred: %s' % error)

    g_menuInteractive(service)



if __name__ == '__main__':
    main()