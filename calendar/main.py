# Author C.J. Burtonprint("Not yet implemented")
import csv
import os
from os import path, system, name, sys
import calendar
from datetime import date, datetime


events = path.relpath("./events.csv")
help_text = """Availible Commands:
-------------------
--> c       > Check your calendar
--> n       > Create a new event
--> d       > Delete an event
--> e       > Edit an event
--> l       > List all events\n
--> exit    > Close the program
--> help    > Show this dialog\n
"""


# Create an event and write to the events.csv file
def createEvent(reader, eid, date, tstart, tend, title):
    with open(events, "w") as eventFile:
        writer = csv.writer(eventFile)
        writer.writerow(listEvents(reader))
        writer.writerow([eid, date, tstart, tend, title])


# TUI for creating an event
def createEventInteractive(reader):
    # TODO:
    # make better input checking
    system('clear')
    print(" --- You are creating an event. --- \n")

    # Sanity checks for date input
    done = 0
    while done == 0:
        userDate = input("Please enter your date (YYYY MM DD):\ne.g. 14th of Febuary 2022 as '2022 02 14' (or 'cancel' to exit back to the main menu)\n\n>  ")
        if userDate.lower() == "cancel":
            done = 1
            return 0
        if len(userDate) != 10:
            print("Bad format, please retry.\n")
        else:
            done = 1
        try:
            uDate = str(datetime.strptime(userDate, "%Y %m %d"))[:1-10]
            print(uDate)
        except Exception as e:
            print("Unrecognised date, please retry.\n")
            print(e)
    done = 0
    while done == 0:
        userStartTime = input("Start Time (HH:MM) >  ")
        if len(userStartTime) != 5:
            print("Bad format, please retry.\n")
        else:
            done = 1
    done = 0
    while done == 0:
        userEndTime = input("End Time (HH:MM) >  ")
        if len(userStartTime) != 5:
            print("Bad format, please retry.\n")
        else:
            done = 1
    done = 0
    while done == 0:
        userTitle = input("Description >  ")
        if len(userTitle) == 0:
            print("Bad format, please retry.\n")
        else:
            done = 1
    createEvent(reader, "test00", uDate, userStartTime, userEndTime, userTitle)


# deletes an event and removes corresponding line in events.csv file
def deleteEvent():
    # NYI
    print("Not yet implemented")


# TUI for deleteEvent
def deleteEventInteractive(reader):
    # NYI
    print("Not yet implemented")


# list upcoming events for a specific time interval
def listEvents(reader):
    eventList = list(reader)
    return eventList


# TUI for listEvents()
def listEventsInteractive(reader):
    # TODO:
    # only show upcoming items
    # give args to specify how many items to show
    print("NOT YET FINISHED\n")
    eventList = listEvents(reader)
    print("ID     Date       Time                Description")
    for event in eventList:
        if event[0] == "eventID": continue
        item = event[0] + " | "
        fDate = str(datetime.strptime(event[1], "%Y%m%d"))[:1-10]
        item += "" + fDate + " | "
        item += "(" + event[2] + " until " + event[3] + ") | "
        item += event[4]
        print(item)


# Draw a quick calendar (no events) 
def drawCal(date):
    current_year = int(date.strftime("%y"))
    current_month = int(date.strftime("%m"))
    print(calendar.month(current_year, current_month))


# TUI for drawing a calendar on a specific month
def drawCalInteractive():
    system("clear")
    drawCal(date.today())
    # prompt them to either find a specific month/year or return to main menu
    userYear = input("--> For a specific year/month, type 's'.\nTo return to main menu, press ENTER:  \n")
    if userYear == "s":
        done = 0
        while done == 0:
            userYear = input("Year (e.g 2022, 2030, 1991):  ")
            userMonth = input("Month (e.g. for Febuary enter '2'):  ")
            # just incase the user didn't read the guide
            if userMonth[0] == '0':
                userMonth = userMonth[1:]
            # incase user enters wrong date, prompt for retry
            try:
                print(calendar.month(int(userYear), int(userMonth)))
                done = 1
            except Exception as e:
                print("Unrecognised format, please retry.\n")
                if input("Try again? (y/n):  ") != "y":
                    done = 1


# help menu for interactive mode
def help():
    system("clear")
    print(help_text)


# interactive menu for when the user wants to do multiple things
def menuInteractive(reader):
    # Greeter and calendar info
    system("clear")
    print("--> Welcome to Calcli! \nBugs/Feedback, contact: C. J. Burton, cjamesburton@outlook.com\n")
    drawCal(date.today())
    print(help_text)

    done = 0
    while done == 0:
        userInput = input(">  ")
        if userInput == "exit":
            done = 1
            exit()
        elif userInput == "help":
            # print help dialog
            help()
        elif userInput == "n":
            # new event
            createEventInteractive(reader)
        elif userInput == "d":
            # delete event
            deleteEventInteractive(reader)
        elif userInput == "e":
            # edit event
            editEventInteractive(reader)
        elif userInput == "l":
            # list events
            listEventsInteractive(reader)
        elif userInput == "c":
            # check calendar
            drawCalInteractive()
        else:
            print("Unrecognised command, type 'help' for a list of commands.\n")


def main():
    # Attempt to open events file, create one if there isn't already
    try:
        with open(os.path.join(sys.path[0], "events.csv"), "r") as ef:
            print(ef.read())
    except FileNotFoundError:
        # create the file, input the headers and then start a new line
        with open(os.path.join(sys.path[0], "events.csv"), "a") as ef:
            ef.write("eventID,date,timeStart,timeEnd,title")
            ef.write(os.linesep)
            ef.close()

    # create a csv reader to scan events
    eventsFile = open(os.path.join(sys.path[0], "events.csv"), "r")
    csvReader = csv.reader(eventsFile, delimiter=",")

    # -- SYSTEM ARGS --
    if len(sys.argv) == 1:
        menuInteractive(csvReader)
    else:
        print("Modular mode with args and stdout coming soon!\n")



if __name__ == "__main__":
    main()
