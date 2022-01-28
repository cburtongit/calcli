# Author C.J. Burtonprint("Not yet implemented")
import csv
import os.path
from os import path, system, name, sys
import calendar
from datetime import date, datetime
import dates_header



# Create an event and write to the events.csv file
def createEvent(writer, eid, date, tstart, tend, title):
    writer.writerow([eid, date, tstart, tend, title])


# TUI for creating an event
def createEventInteractive(writer):
    system('clear')
    print(" --- You are creating an event. --- \n")

    # Sanity checks for date input
    done = 0
    while done == 0:
        userDate = input("Please enter your date (YYYY MM DD):\ne.g. 14th of Febuary 2022 as '2022 02 14' (or 'cancel' to exit back to the main menu)\n\n>  ")
        if userDate.lower() == "cancel":
            done = 1
            break
        if len(userDate) != 10:
            print("Bad format, please retry.\n")
        try:
            uDate = datetime.strptime(userDate, "%Y %m %d")
            print(uDate)
        except Exception as e:
            print("Unrecognised date, please retry.\n")
            print(e)

   

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
    print("NOT YET FINISHED\n")
    # skip the header (first row)
    next(reader)
    print("Showing All Events:\n")
    for line in reader:
        item = ""
        item += line[1][:-2]
        item += "-" + line[1][4:-2]
        item += "-" + line[1][4:]
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
    events = open("events.csv", "r+")
    csvReader = csv.reader(events, delimiter=',')

    # -- SYSTEM ARGS --
    if len(sys.argv) == 1:
        menuInteractive(csvReader)
    else:
        print("Modular mode with args and stdout coming soon!\n")



if __name__ == "__main__":
    main()

