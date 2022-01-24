# Author C.J. Burton
import csv
import os.path
from os import path, system, name
import calendar
from datetime import date


def interactiveMode(writer):
    pass



def createEvent(writer, eid, y, m, d, ts, te, t, n):
    writer.writerow([eid, y, m, d, ts, te, t, n])


def createEventInteractive(writer):
    # clear screen (UNIX only)
    system('clear')
    print(""" --- You are creating an event. --- \n
            Please enter the date:\n
            e.g. '01 04 2022' for the 1st of April, 2022.\n\n""")
    userDate = input(" ---> ").split(" ")
    print(userDate)



def deleteEvent():
    # delete local event
    pass


def editEvent(event):
    # edit local event
    pass


def listEvents():
    # list all local events
    pass


# Draw a quick calendar (no events)
def drawCal():
    current_date = date.today()
    current_year = int(current_date.strftime("%y"))
    current_month = int(current_date.strftime("%m"))
    print(calendar.month(current_year, current_month))


def main():
    # Attempt to open events file, create one if there isn't already
    try:
        open('events.csv')
    except FileNotFoundError:
        open('events.csv', 'a')
        eventFile = open('events.csv', 'a')
        eventFile.write("eventID,year,month,day,timeStart,timeEnd,title,notes")
        eventFile.write(os.linesep)
        eventFile.close()


    # create a csv reader to scan events
    with open('events.csv') as csv_file:
        csvReader = csv.reader(csv_file, delimiter=',')

    # --- CALENDAR MAINLOOP ---

    system("clear")
    # draw a basic calendar for barebones functionality
    drawCal()
    #createEventInteractive(csvReader)

if __name__ == "__main__":
    main()
