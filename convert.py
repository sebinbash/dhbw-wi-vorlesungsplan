import tabula
import locale
from datetime import datetime
from icalendar import Calendar, Event
import re
import ssl

locale.setlocale(locale.LC_ALL, 'de_DE')

def createMeeting(cal, name, start, end, location="Raum 2.10"):
    ev = Event()
    ev.add("summary", name)
    ev.add("dtstart", start)
    ev.add("dtend", end)
    ev.add("location", location)
    cal.add_component(ev)

def readSchedule(pdf, cal):
    dfs = tabula.read_pdf(pdf, lattice=True, pages='all')
    df = dfs[0]
    df = df.replace({r'\r': ' '}, regex=True)
    for (colName, colData) in df.iteritems():
        # print(colData.values)
        col = colData.values
        for i in range(len(col)):
            if type(col[i]) is str:
                try:
                    day = datetime.strptime(col[i], "%A, %d.%m.%Y")
                except ValueError:
                    # print(col[i])
                    pass
                else:
                    if len(col) > i+1 and type(col[i+1]) is str:
                        info = col[i+1]
                        timeranges = re.findall("[0-9]{2}[\.:][0-9]{2} - [0-9]{2}[\.:][0-9]{2}", info)
                        timeranges = [ item.replace(":", ".") for item in timeranges]
                        times = [ item.split(" - ") for item in timeranges]
                        meetings = re.split("[0-9]{2}[\.:][0-9]{2} - [0-9]{2}[\.:][0-9]{2}", info)
                        meetings = [ item.strip() for item in meetings ]
                        if len(meetings) > 1 and meetings[1] != '':
                            # print(meetings[1], times[0][0], times[0][1], col[i])
                            startdt = datetime.strptime(col[i] + " " + times[0][0], "%A, %d.%m.%Y %H.%M")
                            enddt = datetime.strptime(col[i] + " " + times[0][1], "%A, %d.%m.%Y %H.%M")
                            createMeeting(cal, meetings[1], startdt, enddt)
                        if len(meetings) > 2 and meetings[2] != '':
                            # print(meetings[2], times[1][0], times[1][1], col[i])
                            startdt = datetime.strptime(col[i] + " " + times[1][0], "%A, %d.%m.%Y %H.%M")
                            enddt = datetime.strptime(col[i] + " " + times[1][1], "%A, %d.%m.%Y %H.%M")
                            createMeeting(cal, meetings[2], startdt, enddt)

def writeCalendar(cal, file):
    schedule = open(file, 'wb')
    schedule.write(cal.to_ical())
    schedule.close()

def createCalendar():
    return Calendar()

# cal = createCalendar()
# readSchedule("/Users/sebastian/Programming/Python/02 PDFExtract/pdfs/VL-Plan-WWI2020H_4Sem.pdf", cal)
# writeCalendar(cal, "vorlesungsplan_4_sem.ics")