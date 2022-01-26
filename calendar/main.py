# Author C.J. Burton
import csv
import os.path
from os import path, system, name, sys
import calendar
from datetime import date



# Create an event and write to the events.csv file
def createEvent(writer, eid, date, tstart, tend, title):
    writer.writerow([eid, date, tstart, tend, title])


# TUI for creating an event
def createEventInteractive(writer):
    # clear screen (UNIX only)
    system('clear')
    print(" --- You are creating an event. --- \n")

    userYear = input("Year:  \n")
    userMonth = input("Month:  \n")
    userDay = input("Date:  \n")

    date_print = "You have entered:  %s-%s-%s.\n" % (userDay, userMonth, userYear)
    print(date_print)


# deletes an event and removes corresponding line in events.csv file
def deleteEvent():
    # NYI
    print("Not yet implemented")


# TUI for deleteEvent
def deleteEventInteractive(reader):
    # NYI
    print("Not yet implemented")


# modifies an event and writes the new line to the file
def editEvent(event):
    # NYI
    print("Not yet implemented")


# list upcoming events for a specific time interval
def listEvents():
    # NYI
    # list upcoming events for a specific time interval
    # e.g.  listEvents(w) will return all events for the next 7 days
    #       listEvents(m) will return all events for the next 30 days
    #       listEvents() will return all events from the current date
    print("Not yet implemented")


# TUI for listEvents()
def listEventsInteractive(reader):
    # NYI
    print("Not yet implemented")


# Draw a quick calendar (no events) 
def drawCal(date):
    current_year = int(date.strftime("%y"))
    current_month = int(date.strftime("%m"))
    print(calendar.month(current_year, current_month))


# TUI for drawing a calendar on a specific month
def drawCalInteractive():
    system("clear")
    drawCal(date.today())
    userYear = input("--> For a specific year/month, type 's'.\nTo return to main menu, press ENTER:  \n")
    if userYear == "s":
        done = 0
        while done == 0:
            userYear = input("Year (e.g 2022, 2030, 1991):  ")
            userMonth = input("Month (e.g. for Febuary enter '02'):  ")
            try:
                print(calendar.month(int(userYear[2:]), int(user_month)))
                done = 1
            except Exception as e:
                print("Unrecognised format, please retry.\n")
                if input("Try again? (y/n):  ") != "y":
                    done = 1


# help menu for interactive mode
def help():
    system("clear")
    print("Availible Commands:\n-------------------\n--> c       > Check your calendar\n--> n       > Create a new event\n--> d       > Delete an event\n--> e       > Edit an event\n--> l       > List all events\n\n--> exit    > Close the program\n--> help    > Show this dialog\n")


# interactive menu for when the user wants to do multiple things
def menuInteractive(reader):
    # Greeter and calendar info
    system("clear")
    print("--> Welcome to Calcli! \nAuthor: C. J. Burton, cjamesburton@outlook.com\n\n")
    drawCal(date.today())
    print("\n\n")
    print("Availible Commands:\n-------------------\n--> c       > Check your calendar\n--> n       > Create a new event\n--> d       > Delete an event\n--> e       > Edit an event\n--> l       > List all events\n\n--> exit    > Close the program\n--> help    > Show this dialog\n")

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
        open('events.csv')
    except FileNotFoundError:
        open('events.csv', 'a')
        eventFile = open('events.csv', 'a')
        eventFile.write("eventID,date,timeStart,timeEnd,title")
        eventFile.write(os.linesep)
        eventFile.close()


    # create a csv reader to scan events
    with open('events.csv') as csv_file:
        csvReader = csv.reader(csv_file, delimiter=',')

    # -- SYSTEM ARGS --
    if len(sys.argv) == 1:
        menuInteractive(csvReader)
    else:
        system("clear")
        drawCal(date.today())



if __name__ == "__main__":
    main()

