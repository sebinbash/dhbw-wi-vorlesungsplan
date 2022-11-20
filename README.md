# DHBW WI Vorlesungsplan pdf2ical

## Requirements & Setup

- [ghostscript](https://www.ghostscript.com/)
- tk

Die dependencies installiert man am besten in einem virtual environment mit:
```
pip -r requirements.txt
```

## Usage


```
usage: convert_pdf.py [-h] [-i INPUT] [-r ROOM] output

Converts DHBW WI lecture schedule from pdf to ical format

positional arguments:
  output                    output file (ical format)

options:
  -h, --help                show this help message and exit
  -i INPUT, --input INPUT   input pdf
  -r ROOM, --room ROOM      default room
```

