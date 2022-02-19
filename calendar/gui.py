# Author C.J. Burtonprint("Not yet implemented")
import csv, calendar, os
from os import path, system, name, sys
from datetime import date, datetime
import calcli


events = os.path.join(sys.path[0], "events.csv")
help_text = """Availible Commands:
--> c       > Check your calendar
--> n       > Create a new event
--> l       > List all events\n
--> exit    > Close the program
--> help    > Show this dialog"""


# TUI for creating an event
def createEventInteractive():
    # TODO:
    # make better input checking
    # DATE FORMATTING IDEA: try/catch using datetime.strp() format
    clear()
    done = 0
    while done == 0:
        userDate = input("Event Date (e.g. '01 06 2022' for the 1st of June, 2022): \n")
        try:
            uDate = str(datetime.strptime(userDate, "%d %m %Y"))[:1-10]
            uDate = uDate.replace("-", "")
            done = 1
        except ValueError:
            print("Bad formatting, Please retry.\n")
    done = 0
    while done == 0:
        userStartTime = input("Start time (e.g. '10:30' for 10:30AM or '20:45' for 8:45PM): ")
        try:
            uST = userStartTime.split(":")
            print(uDate)
            int(uST[0]) < 25 == True
            int(uST[1]) < 61 == True
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
        print(uDate)
        start = "" + str(uST[0]) + str(uST[1])
        end = "" + str(uET[0]) + str(uET[1])
        calcli.createEvent(uDate, start, end, userDesc)
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
    eventList = calcli.listEvents()
    clear()
    print("#       Date       Time                Description")
    eventCounter = 1
    for event in eventList:
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
    clear()
    drawCal(date.today())
    done = 0
    while done == 0:
        userDate = input("For a specific date please enter in the format 'DD MM YYYY'\nor press ENTER to return to menu.\n")
        if userDate == "cancel" or userDate == "":
            done = 1
            break
        try:
            userYear = int(userDate[-4:])
            userMonth = int(userDate[:2])
            print(calendar.month(int(userYear), int(userMonth)))
            done = 1
        except Exception as e:
            print("Unrecognised format, please retry.\n")
            if input("Try again? (y/n):  ") != "y":
                done = 1


# help menu for interactive mode
def help():
    clear()
    print(help_text)

# Clears the terminal using system calls based on what OS kernel is used
def clear():
    if name == "nt":
        system("cls")
    else:
        system("clear")

# interactive menu for when the user wants to do multiple things
def menuInteractive():
    clear()
    calcli.sortEvents()
    print(help_text)
    # user input menu
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
            calcli.sortEvents()
        elif userInput == "l":
            # list events
            listEventsInteractive()
        elif userInput == "c":
            # check calendar
            drawCalInteractive()
        else:
            print("Unrecognised command, type 'help' for a list of commands.")


def main():
    calcli.main()
    menuInteractive()
    exit()
main()