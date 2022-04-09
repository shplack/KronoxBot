import urllib
from datetime import datetime
from typing import List

from icalevents import icalevents
from school import School


def format_url(schema_url: str, start: datetime, end: datetime, lang: str, courses: List[str], programs: List[str]) -> str:
    url = schema_url
    url += 'setup/jsp/SchemaICAL.ics?'
    url += 'startDatum=' + start.date().isoformat() + '&'
    url += 'slutDatum=' + end.date().isoformat() + '&'
    url += 'sprak=' + lang + '&'
    url += 'resurser='
    
    if courses and courses != []:
        print(courses)
        url += 'k.'
        for course in courses:
            if course[-1] == '-':
                course += ','
            elif course[-2] != '-' and course [-1] == ',':
                course = course[:-1] + '-,'
            else:
                course += '-,'
                
            url += urllib.parse.quote(course)
        
    if programs != []:
        url += 'p.'
        for program in programs:
            if program[-1] == '-':
                program += ','
            elif program[-2] != '-' and program [-1] == ',':
                program = program[:-1] + '-,'
            else:
                program += '-,'
                
            url += urllib.parse.quote(program)
    
    return url

def search(
    school          : School,
    course_codes    : List[str] = None,
    programs        : List[str] = None,
    start           : datetime  = None,
    end             : datetime  = None,
    lang            : str       = 'SV'
):
    
    if not course_codes and not programs:
        raise ValueError
    
    if not start:
        start = datetime.today()
        print()
        
    if not end:
        end = start
        
    url = format_url(school.schema_url, start, end, lang, course_codes, programs)
    ical = icalevents.events(url)
    return ical
