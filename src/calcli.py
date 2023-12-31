# Author C.J. Burton
import csv, calendar, os, itertools
from operator import delitem
from os import path, system, name, sys
from datetime import date, datetime


events = os.path.join(sys.path[0], "events.csv")


# Create an event by writing details to the events.csv file
def createEvent(date, tstart, tend, title):
    with open(events, "a") as eventsFile: # "a" flag APPENDS to END of file, note for later. 
        writer = csv.writer(eventsFile)
        writer.writerow([date, tstart, tend, title])
        eventsFile.close()


# mass rewrites config with new event list
def rewriteConfig(eList):
    with open(events, "w", newline="") as eventsFile:
    # Write the sorted list back to the file
        csvWriter = csv.writer(eventsFile, delimiter=",")
        csvWriter.writerows(eList)


# list upcoming events for a specific time interval
def listEvents():
    with open(events, "r") as eventsFile:
        csvReader = csv.reader(eventsFile, delimiter=",")
        eventList = list(csvReader)
        eventsFile.close()
    return eventList


# Gets next number of events from current date
def getNextEvents():
    currentDate = datetime.now().strftime('%Y%m%d')
    with open(events, "r") as eventsFile:
        csvReader = csv.reader(eventsFile, delimiter=",")
        eventList = list(csvReader)
        eventsFile.close()
    for i in eventList:
        if (i[0] <= currentDate):
            eventList.remove(i)
    # Strange bug where the first target item is not removed, this is a fix
    if os.stat(events).st_size == 0:
        return eventList
    else:
        del eventList[0]
    return eventList


# sorts the csv file by reading in the current file, sorting by date, then re-writing new list
def sortEventsFile():
    # Note to self, r+ is read/write with file pointer at START of file, use a for appending
    with open(events, "r", newline="") as eventsFile:
        csvReader = csv.reader(eventsFile, delimiter=",")
        eventsSorted = sorted(csvReader, key=lambda f: f[0], reverse=False)
    with open(events, "w", newline="") as eventsFile:
    # Write the sorted list back to the file
        csvWriter = csv.writer(eventsFile, delimiter=",")
        csvWriter.writerows(eventsSorted)


# sort a random list of events
def sortEvents(events):
    events.sort()
    eventsSorted = list(events for events,_ in itertools.groupby(events))
    return eventsSorted
        

# initialise a system enviroment for calCLI by rading/creating the required
# files and then sorting them
def main():
    # Attempt to open events file, create one if there isn't already
    try:
        # open a file as read-only
        open(events, "r")
    except FileNotFoundError:
        # create the file if not already present
        with open(events, "a") as eventsFile:
            eventsFile.close()
    try:
        sortEventsFile()
    except Exception as e:
        print(e)
        print("Please delete events.csv or repair to continue")
        exit(1)