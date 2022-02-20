# Author C.J. Burtonprint("Not yet implemented")
import csv, calendar, os
from os import path, system, name, sys
from datetime import date, datetime
import calcli


events = os.path.join(sys.path[0], "events.csv")
help_text = """Availible Commands:
--> c       > Check your calendar
--> n       > Create a new event
--> l       > List all events
\n--> exit    > Close the program
--> help    > Show this dialog"""


# TUI for creating an event
def createEventInteractive():
    clear()
    # Date
    done = 0
    while done == 0:
        userDate = input("Event Date (e.g. '01 06 2022' for the 1st of June, 2022): \n")
        try:
            uDate = str(datetime.strptime(userDate, "%d %m %Y"))[:1-10]
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


# TUI for deleteEvent
def deleteEventInteractive(reader):
    # NYI
    print("Not yet implemented")


# TUI for listEvents()
def listEventsInteractive():
    eventList = calcli.listEvents()
    clear()
    print("#        Date          Time               Description")
    print("---------------------------------------------------------")
    eventCounter = 1
    for event in eventList:
        if eventCounter < 10:
            item = str(eventCounter) + "        "
        else:
            item = str(eventCounter) + "       "
        fDate = str(datetime.strptime(event[0], "%Y%m%d"))[:1-10]
        item += "" + fDate + "    "
        itemStartTime = event[1][:2] + ":" + event[1][2:]
        itemEndTime = event[2][:2] + ":" + event[2][2:] 
        item += "(" + itemStartTime + " - " + itemEndTime + ")    "
        item += event[3]
        print(item)
        eventCounter += 1


# Lists next N number of UPCOMING EVENTS (no screen clearing)
def listUpcomingInteractive(n):
    eventList = calcli.getNextEvents()
    print("Your next " + str(n) + " upcoming events:")
    eventCounter = 1
    for event in eventList:
        if eventCounter < 10:
            item = str(eventCounter) + "        "
        else:
            item = str(eventCounter) + "       "
        fDate = str(datetime.strptime(event[0], "%Y%m%d"))[:1-10]
        item += "" + fDate + "    "
        itemStartTime = event[1][:2] + ":" + event[1][2:]
        itemEndTime = event[2][:2] + ":" + event[2][2:] 
        item += "(" + itemStartTime + " - " + itemEndTime + ")    "
        item += event[3]
        print(item)
        eventCounter += 1
        if eventCounter > n:
            break


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
            userDate = userDate.split(" ")
            userYear = int(userDate[2])
            userMonth = int(userDate[1])
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

# Clears the terminal using system calls based on what OS  is used
def clear():
    if name == "nt":
        # windows
        system("cls")
    else:
        # *nix
        system("clear")

# interactive menu for when the user wants to do multiple things
def menuInteractive():
    clear()
    calcli.sortEvents()
    drawCal(date.today())
    print("\n")
    listUpcomingInteractive(3)
    print("\n\n" + help_text)
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