# Author C.J. Burtonprint("Not yet implemented")
import csv, calendar, os
from os import path, system, name, sys
from datetime import date, datetime


events = os.path.join(sys.path[0], "events.csv")


# Create an event and write to the events.csv file
def createEvent(date, tstart, tend, title):
    with open(events, "w") as eventsFile:
        writer = csv.writer(eventsFile)
        writer.writerow([date, tstart, tend, title])
    eventsFile.close()


# deletes an event and removes corresponding line in events.csv file
def deleteEvent():
    # NYI
    print("Not yet implemented")


# list upcoming events for a specific time interval
def listEvents():
    eventsFile = open(events, "r")
    csvReader = csv.reader(eventsFile, delimiter=",")
    eventList = list(csvReader)
    eventsFile.close()
    return eventList


def main():
    # Attempt to open events file, create one if there isn't already
    try:
        open(events, "r")
    except FileNotFoundError:
        # create the file, input the headers and then start a new line
        with open(events, "a") as eventsFile:
            eventsFile.write("date,timeStart,timeEnd,title")
            eventsFile.write(os.linesep)
            eventsFile.close()