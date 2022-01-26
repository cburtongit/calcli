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
    # delete local event
    pass


# modifies an event and writes the new line to the file
def editEvent(event):
    # edit local event
    pass


# list upcoming events for a specific time interval
def listEvents():
    # NYI
    # list upcoming events for a specific time interval
    # e.g.  listEvents(w) will return all events for the next 7 days
    #       listEvents(m) will return all events for the next 30 days
    #       listEvents() will return all events from the current date
    pass


# look for a specific event in events.csv
def searchEvents():
    # NYI
    pass


# Draw a quick calendar (no events) 
def drawCal(date):
    current_year = int(date.strftime("%y"))
    current_month = int(date.strftime("%m"))
    print(calendar.month(current_year, current_month))

# interactive menu for when the user wants to do multiple things
def menuInteractive(reader):
    # Greeter and calendar info
    system("clear")
    print("""
     ----- Welcome to Calcli! ------\n
    A terminal Calendar application by C. J. Burton, any bugs/issues/feeback please
    email me at cjamesburton@outlook.com
    """)
    drawCal(date.today())
    print("\n\n")

    """
    # Controls
    userSelection = {
            "help"  : print(">HELP MESSAGE HERE<"),
            "n"     : createEventInteractive(reader),
            "d"     : deleteEventInteractive(reader),
            "l"     : listEventsInteractive(reader),
            "c"     : drawCal(date.today())
    }
    """

    done = 0
    while done != 0:
        userInput = input("--->  ")
        if userInput == "exit":
            done = 1
            exit()
        # else ifs here
        else:
            print("Your input is:  " + userInput + "\n")


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

