import camelot
import argparse
import locale
import pandas as pd
import re
from datetime import datetime
from icalendar import Calendar, Event

locale.setlocale(locale.LC_ALL, 'de_DE.utf8')
BLOCK = "BLOCK"

parser = argparse.ArgumentParser(description="Converts DHBW WI lecture schedule from pdf to ical format")
parser.add_argument('-i', '--input', help='input pdf')
parser.add_argument('-r', '--room', help='default room', required=False)
parser.add_argument('output', help='output file (ical format)')
args = parser.parse_args()

# set room default
room = args.room if args.room != None else ""

# convenience functions
def create_meeting(calendar, name, start, end, location):
    event = Event()
    event.add("summary", name)
    event.add("dtstart", start)
    event.add("dtend", end)
    event.add("location", location)
    calendar.add_component(event)

# import table
tables = camelot.read_pdf(args.input)
df = tables[0].df

# filter out rows with weeks
df2 = df[df.applymap(lambda row: "Woche" not in row if isinstance(row,str) else True).to_numpy()[:,1]]

# concat all columns to a series
ser = pd.Series(dtype="object")
for col in df2.columns:
    ser = pd.concat([ser,df2[col]], axis=0, ignore_index=True)

# prepare regex
time_regex = re.compile("(\d{2})[\.:](\d{2}) - (\d{2})[\.:](\d{2})")
room_regex = re.compile("([RP][\d\.,\\ ]+)|\[([\w ]+)\]")

# create calendar
cal = Calendar()

# iterate over items in series
for (_, datestr), (_, cell) in zip(ser.iloc[::2].items(),ser.iloc[1::2].items()):
    try:
        date = datetime.strptime(datestr, "%A, %d.%m.%Y")
    except ValueError:
        continue
    lines = cell.split("\n")

    if len(lines) > 2:
        times = []
        events = ["", ""]
        for line in lines:
            
            if time_regex.match(line):
                times.append(line)
            elif len(times) == 1:
                events[0] += line + " "
            else:
                events[1] += line + " "
            
        for time, event in zip(times, events):
            if BLOCK in event or event == "":
                continue

            time_match = time_regex.match(time)
            room_match = room_regex.search(event)

            start = date.replace(hour=int(time_match.group(1)), minute=int(time_match.group(2)))
            end = date.replace(hour=int(time_match.group(3)), minute=int(time_match.group(4)))
            location = room_match.group(0) if room_match != None else room
            create_meeting(cal, event.strip(), start, end, location)

# write ical to file
file = open(args.output, 'wb')
file.write(cal.to_ical())
file.close()
