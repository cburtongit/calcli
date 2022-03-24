# Author C.J. Burtonprint("Not yet implemented")
import csv, calendar, os
from os import path, system, name, sys
from datetime import date, datetime

import calcli


events = os.path.join(sys.path[0], "events.csv")
conf = os.path.join(sys.path[0], "calcli.conf")
help_text = """Availible Commands:
--> c       > Check your calendar
--> n       > Create a new event
--> l       > List all events
--> d       > Delete events
\n--> exit    > Close the program
--> help    > Show this dialog"""
welcome_text = """              __________    ____
  _________ _/ / ____/ /   /  _/
 / ___/ __ `/ / /   / /    / /
/ /__/ /_/ / / /___/ /____/ /
\___/\__,_/_/\____/_____/___/\n"""
dateformat = ""


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
        """
        userDate = input("Event Date (e.g. '06 01 2022' for the 1st of June, 2022): \n")
        try:
            uDate = str(datetime.strptime(userDate, "%m %d %Y"))[:1-10]
            uDate = uDate.replace("-", "")
            done = 1
        except ValueError:
            print("Bad formatting, Please retry.\n")
        """
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


# TUI for listEvents()
def listEventsInteractive(eventList):
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
            # fDate = str(datetime.strptime(event[0], "%Y%d%m"))[:1-10]
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
    print("Upcoming events:")
    eventCounter = 1
    if len(eventList) == 0:
        print("No offline events.")
        return
    for event in eventList:
        # format the number and appropriate whitespace
        if eventCounter < 10:
            item = "  " + str(eventCounter) + "      "
        elif eventCounter < 100:
            item = " " + str(eventCounter) + "      "
        else:
            item = str(eventCounter) + "      "
        # build a string of the date, start time, end time and description
        # format the date from file, remove time then split by [YYYY], [MM], [DD]
        fDate = ""
        
        fDate = str(datetime.strptime(event[0], "%Y%m%d"))[:1-10].split("-")
        # reform the list, reversing the element order whilst adding '-' between
        item += fDate[2] + "-" + fDate[1] + "-" + fDate[0] + "    "
        # format and store the start and end times from file
        itemStartTime = event[1][:2] + ":" + event[1][2:]
        itemEndTime = event[2][:2] + ":" + event[2][2:]
        # add formatted times and description
        item += "(" + itemStartTime + " - " + itemEndTime + ")    " + event[3]
        print(item)
        eventCounter += 1
        if eventCounter > n:
            break


# allows user to delete/edit events
def deleteEventsInteractive():
    listEventsInteractive(calcli.listEvents())
    eventList = calcli.listEvents()
    done = 0
    while done == 0:
        userTargets = input("Select event number(s) to delete (e.g. '1 3 9 14 28'):  ")
        if userTargets == "":
            done = 1
            break
        try:
            userTargets = list(map(int, userTargets.split(" ")))
            for index in sorted(userTargets, reverse=True):
                del eventList[index - 1]
            done = 1
            listEventsInteractive(eventList)
            calcli.overwriteEventFile(eventList)
        except Exception as e:
            print("Bad input, please retry.")


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
        """
        while done == 0:
            userDate = input("For a specific date please enter in the format 'MM DD YYYY'\nor press ENTER to return to menu.\n")
            if userDate == "cancel" or userDate == "":
                done = 1
                break
            try:
                userDate = userDate.split(" ")
                userYear = int(userDate[2])
                userMonth = int(userDate[0])
                print(calendar.month(int(userYear), int(userMonth)))
                done = 1
            except Exception as e:
                print("Unrecognised format, please retry.\n")
                if input("Try again? (y/n):  ") != "y":
                    done = 1
        """

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


def rewriteConfig(eList):
    with open(events, "w", newline="") as eventsFile:
    # Write the sorted list back to the file
        csvWriter = csv.writer(eventsFile, delimiter=",")
        csvWriter.writerows(eList)

# interactive menu for when the user wants to do multiple things
def menuInteractive():
    clear()
    calcli.sortEvents()
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
            #listEventsInteractive(calcli.listEvents())
            listUpcomingInteractive(1000)
        elif userInput == "d":
            # delete/edit events
            deleteEventsInteractive()
        elif userInput == "c":
            # check calendar
            drawCalInteractive()
        else:
            print("Unrecognised command, type 'help' for a list of commands.")


def main():
    calcli.main()
    try:
        with open(conf, "r") as confFile:
            for line in confFile:
                if line[:7] == "datefmt":
                    dateformat = line.split(" ")
                    dateformat = dateformat[1]
    except Exception as e:
        print(e)
        exit(1)
    menuInteractive()
    exit()

if __name__ == '__main__':
    main()