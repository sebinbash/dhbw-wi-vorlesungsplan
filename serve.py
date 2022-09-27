from bottle import route, run, static_file
from pdf2ical.convert import *
import requests
import re
from bs4 import BeautifulSoup

scrape_pdfs = False

years = [
    "https://www.dhbw-stuttgart.de/studierendenportal/wirtschaftsinformatik/plaene/vorlesungsplaene/studienjahrgang-2018/",
    "https://www.dhbw-stuttgart.de/studierendenportal/wirtschaftsinformatik/plaene/vorlesungsplaene/studienjahrgang-2019/",
    "https://www.dhbw-stuttgart.de/studierendenportal/wirtschaftsinformatik/plaene/vorlesungsplaene/studienjahrgang-2020/",
    "https://www.dhbw-stuttgart.de/studierendenportal/wirtschaftsinformatik/plaene/vorlesungsplaene/studienjahrgang-2021/"
    ]

if scrape_pdfs:
    print("Downloading pdfs...")
    for page in years:
        r = requests.get(page)
        soup = BeautifulSoup(r.content, 'html.parser')

        courses = soup.find_all('h2', { 'class' : 'underline' })
        lists = soup.find_all('ul', class_='dhbw-link-list')

        courses = [ re.findall('WWI[0-9]*[A-Z]', course.string) for course in courses ]
        links = [ linklist.find_all('a') for linklist in lists]
        
        for linklist, course in zip(links, courses):
            cal = createCalendar()
            print("Reading schedule for " + course[0] + "...")
            for link in linklist:
                readSchedule("https://www.dhbw-stuttgart.de" + link['href'], cal)
            
            writeCalendar(cal, "public/" + course[0] + ".ics")
    print("Done!")

@route('/')
def index():
    return static_file("index.html", root="./")

@route('/timetable/<file:path>')
def file(file):
    return static_file(file, root="public")

run(host='localhost', port=8080)