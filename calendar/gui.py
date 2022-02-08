# Author C.J. Burtonprint("Not yet implemented")
import csv, calendar, os
from os import path, system, name, sys
from datetime import date, datetime
import calcli


events = os.path.join(sys.path[0], "events.csv")
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


# TUI for creating an event
def createEventInteractive():
    # TODO:
    # make better input checking
    # DATE FORMATTING IDEA: try/catch using datetime.strp() format
    system('clear')
    done = 0
    while done == 0:
        userDate = input("Event Date (e.g. '01 06 2022' for the 1st of June, 2022): \n")
        try:
            uDate = datetime.strptime(userDate, "%d %m %Y")[:1-10]
            done = 1
        except ValueError:
            print("Bad formatting, Please retry.\n")
    done = 0
    while done == 0:
        userStartTime = input("Start time (e.g. '10:30' for 10:30AM or '20:45' for 8:45PM): ")
        try:
            uST = userStartTime.split(":")
            int(uST[0]) < 25 == True;
            int(uST[1]) < 61 == True;
            done = 1
        except Exception as e:
            print(e)
            print("Bad formatting, Please retry.\n")
    done = 0
    while done == 0:
        userEndTime = input("End time (e.g. '10:30' for 10:30AM or '20:45' for 8:45PM): ")
        try:
            uET = userEndTime.split(":")
            int(uST[0]) < 25 == True;
            int(uST[1]) < 61 == True;
            done = 1
        except Exception as e:
            print(e)
            print("Bad formatting, Please retry.\n")
    userDesc = input("Event description: ")
    try:
        calcli.createEvent(uDate, uST, uET, userDesc)
        print("Event created.\n")
    except Exception as e:
        print("Error:\n" + str(e) + "\n")


# TUI for deleteEvent
def deleteEventInteractive(reader):
    # NYI
    print("Not yet implemented")


# TUI for listEvents()
def listEventsInteractive():
    # TODO:
    # only show upcoming items
    # give args to specify how many items to show
    print("NOT YET FINISHED\n")
    eventList = calcli.listEvents()
    print("Number  Date       Time                Description")
    eventCounter = 1
    for event in eventList:
        if event[0] == "date": continue
        item = str(eventCounter) + "     | "
        fDate = str(datetime.strptime(event[0], "%Y%m%d"))[:1-10]
        item += "" + fDate + " | "
        item += "(" + event[1] + " until " + event[2] + ") | "
        item += event[3]
        print(item)

        eventCounter += 1


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
def menuInteractive():
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
            createEventInteractive()
        elif userInput == "d":
            # delete event
            deleteEventInteractive()
        elif userInput == "e":
            # edit event
            editEventInteractive()
        elif userInput == "l":
            # list events
            listEventsInteractive()
        elif userInput == "c":
            # check calendar
            drawCalInteractive()
        else:
            print("Unrecognised command, type 'help' for a list of commands.\n")


def main():
    menuInteractive()
    pass
main()