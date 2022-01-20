# Author C.J. Burton
import calendar
from datetime import date

# Draw a quick calendar (no events)
def drawCal():
    current_date = date.today()
    current_year = int(current_date.strftime("%y"))
    current_month = int(current_date.strftime("%m"))
    print(calendar.month(current_year, current_month))


def main():
    drawCal()

if __name__ == "__main__":
    main()
