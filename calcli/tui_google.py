import sys, os, time, itertools
from threading import local
import os.path
import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import pytz
from tzlocal import get_localzone

import tui

help_text = """Availible Commands:
--> c       > Check your calendar
--> n       > Create a new event
--> l       > List all events
--> d       > Delete events
--> s       > Sync online/offline calendars
\n--> help    > Show this dialog
--> gpl     > Show Licence information
--> quit    > Close the program"""

lic_text = """This software is licenced under
the GNU GPL v3 Licence, more info can be found here: 
https://www.gnu.org/licenses/gpl-3.0.en.html"""

# Permissions for using the calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']
# User credentials file
token_file = os.path.join(sys.path[0], "token.json")
creds_file = os.path.join(sys.path[0], "credentials.json")
tz = get_localzone()
stz = str(tz)



# create event on google calendar
def g_createEvent(service, userDate, userStartTime, userEndTime, userTitle):
    uSdt = userDate + " " + userStartTime
    uEdt = userDate + " " + userEndTime
    sfDate = datetime.datetime.strptime(uSdt, "%Y %m %d %H:%M") # create date time object
    sfDate.replace(tzinfo=tz) # localise
    efDate = datetime.datetime.strptime(uEdt, "%Y %m %d %H:%M")
    efDate.replace(tzinfo=tz)
    startUTC = sfDate.astimezone(pytz.utc) # convert to UTC
    endUTC = efDate.astimezone(pytz.utc)
    # create event
    event = {
        'summary': userTitle,
        'description': '',
        'start': {
            'dateTime': startUTC.isoformat(),
            'timeZone': stz,
        },
        'end': {
            'dateTime': endUTC.isoformat(),
            'timeZone': stz,
        },
    }
    event = service.events().insert(calendarId='primary', body=event).execute() # add to calendar
    print('Event created: %s' % (event.get('htmlLink')))


# menu for creating a new online/offline event
def g_createEventInteractive(service):
    # get date
    done = 0
    while done == 0:
        userDate = input("Date (YYYY-MM-DD): ")
        try:
            datetime.datetime.strptime(userDate, "%Y %m %d")
            done = 1
        except Exception as e:
            print("Bad formatting, Please retry.\n")
    # get start time
    done = 0
    while done == 0:
        userStartTime = input("Start Time (HH:MM): ")
        try:
            datetime.datetime.strptime(userStartTime, "%H:%M")
            done = 1
        except Exception as e:
            print("Bad formatting, Please retry.\n")
    # get end time
    done = 0
    while done == 0:
        userEndTime = input("End Time (HH:MM): ")
        try:
            datetime.datetime.strptime(userEndTime, "%H:%M")
            done = 1
        except Exception as e:
            print("Bad formatting, Please retry.\n")
    # get description
    done = 0
    while done == 0:
        userTitle = input("Event Description: ")
        if len(userTitle) < 1:
            print("Bad formatting, Please retry.\n")
        else:
            done = 1
    g_createEvent(service, userDate, userStartTime, userEndTime, userTitle)


# deletes a google calendar event
def g_deleteEvent(service, eventid):
    service.events().delete(calendarId='primary', eventId=eventid).execute()


# menu for deleting online/offline events
def deleteEventsInteractive(service):
    tui.listEventsInteractive(tui.calcli.listEvents()) # display ALL events
    eventList = tui.calcli.listEvents() # get eventlist
    events_result = service.events().list(calendarId = "primary", singleEvents = True, orderBy = "startTime").execute()
    g_events = events_result.get("items", []) # get google calendar events
    g_targets = []
    done = 0
    while done == 0:
        userTargets = input("Select event number(s) to delete (e.g. '1 3 9 14 28'):  ")
        if userTargets == "": done = 1; break # skip if empty list
        try:
            userTargets = list(map(int, userTargets.split(" ")))
            for index in sorted(userTargets, reverse=True):
                g_targets.append(eventList[index-1]) # remember event for google deletion
                del eventList[index - 1]       
            for t in g_targets:
                for g in g_events:
                    if t[3] == g['summary']: # match date +
                        if t[0] == (g["start"].get("dateTime")[:10]).replace("-", ""): # title
                            g_deleteEvent(service, g['id']) # delete the event
                            print("Event deleted.") # confirm
            tui.calcli.rewriteConfig(eventList) # write to offline
            done = 1
        except Exception as e:
            print("Bad input, please retry.")


def g_sync(service):
    total_events = tui.calcli.listEvents() # get local event list
    google_events = [] # get google event list
    g_serv = service.events().list(calendarId = "primary", singleEvents = True, orderBy = "startTime").execute()
    g_events = g_serv.get("items", [])   
    for event in g_events:
        eStart = event["start"].get("dateTime")[:16]
        eStart = datetime.datetime.strptime(eStart, "%Y-%m-%dT%H:%M")
        eStart = eStart.astimezone(tz)
        eEnd = event["end"].get("dateTime")[:16]
        eEnd = datetime.datetime.strptime(eEnd, "%Y-%m-%dT%H:%M")
        eEnd = eEnd.astimezone(tz)
        eventDate = (str(eStart)[:10]).replace("-", "")
        eventStart = (str(eStart)[11:-9]).replace(":", "")
        eventEnd = (str(eEnd)[11:-9]).replace(":", "")
        eventDesc = event['summary']
        new_event = [eventDate, eventStart, eventEnd, eventDesc]
        google_events.append(new_event)
    total_events.extend(google_events) # merge lists
    events = tui.calcli.sortEvents(total_events)
    tui.calcli.rewriteConfig(events)
    

# List all upcoming events from Offline calendar and then Google Events
def g_listUpcomingInteractive(n, service):
    tui.clear()
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
        if eventCounter < 10: item = "  " + str(eventCounter) + "      "
        elif eventCounter < 100:item = " " + str(eventCounter) + "      "
        else: item = str(eventCounter) + "      "
        eStart = event["start"].get("dateTime")[:16]
        eStart = datetime.datetime.strptime(eStart, "%Y-%m-%dT%H:%M")
        eStart = eStart.astimezone(tz)
        eEnd = event["end"].get("dateTime")[:16]
        eEnd = datetime.datetime.strptime(eEnd, "%Y-%m-%dT%H:%M")
        eEnd = eEnd.astimezone(tz)
        item += str(eStart)[:10] + "    "
        item += "(" + str(eStart)[11:-9] + " - " + str(eEnd)[11:-9] + ")"
        item += "    " + event['summary']
        print(item) # + event['id'])
        eventCounter += 1
        if eventCounter > n:
            break


# spit out help text
def help():
    tui.clear()
    print(help_text)


# prints licence
def licence():
    tui.clear()
    print(lic_text)


# main menu
def g_menuInteractive(service):
    tui.clear()
    g_sync(service) # sync up local and google calendars
    print(tui.welcome_text + "\n" + help_text + "\n")
    while 1: # user input
        userInput = input(">  ")
        if userInput == "exit" or userInput == "q" or userInput == "quit": tui.clear(); exit()
        elif userInput == "help": help() # print help dialog
        elif userInput == "n": g_createEventInteractive(service); g_sync(service) # new event
        elif userInput == "l": tui.listEventsInteractive(tui.calcli.listEvents()) # list events
        elif userInput == "d": deleteEventsInteractive(service) # delete/edit events
        elif userInput == "c": tui.drawCalInteractive() # check calendar
        elif userInput == "s": g_sync(service); print("Syncing complete.") # sync events between offline and online
        elif userInput == "gpl": licence() # print licence
        else: print("Unrecognised command, type 'help' for a list of commands.")


# initialise a calendar and then call menu function
def main():
    creds = None
    if os.path.exists(token_file): # load credentials from a file if already existing
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    if not creds or not creds.valid: # If there are no (valid) credentials available, prompt for user login.
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
            creds = flow.run_local_server(port = 0)
        with open(token_file, "w") as token: # Save the credentials for the next run
            token.write(creds.to_json())
    try: # attempt to create a calendar instance
        service = build("calendar", "v3", credentials = creds)
    except HttpError as error: # throw an error if there are connection issues to API
        print('An error occurred: %s' % error)
    g_menuInteractive(service) # load menu



if __name__ == '__main__':
    main()