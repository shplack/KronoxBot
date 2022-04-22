import datetime
from datetime import datetime as dt, timedelta as td

from icalevents import icalevents
from pytz import timezone

from database.kronox_db import Database

ical_link = 'setup/jsp/SchemaICAL.ics?'
start = '&startDatum='
end = '&slutDatum='
resource = '&resurser='
strftime = '%Y-%m-%d'


class LinkMaker:
    def __init__(self):
        self._start = None
        self._end = None
        self._school = None
        self._school_link = None
        self._program = None
        self._course = None

    @staticmethod
    def _do_date(_input: str) -> datetime.date:
        # TODO: db lookup localizations (today, tmw, etc)
        # TODO: check if value is alpha/numeric to check if shorthand given or straight-up a date

        tdy = ['today', 'tdy', 'idag'], td(days=0)
        tmw = ['tmorrow', 'tmw', 'imorn', 'imorgon', 'i morgon'], td(days=1)
        omw = ['overmorrow', 'over morrow', 'omw', 'imorn', 'imorgon', 'i morgon'], td(days=2)

        for acceptables, delta in [tdy, tmw, omw]:
            if _input in acceptables:
                return dt.today() + delta

        if _input.startswith('days'):
            days = int(''.join(filter(str.isdigit, _input)))
            return dt.today() + td(days=days)

        if _input.startswith('weeks'):
            weeks = int(''.join(filter(str.isdigit, _input)))
            return dt.today() + td(weeks=weeks)

        try:
            return dt.strptime(_input, '%Y-%m-%d')
        except ValueError as e:
            print(e, _input)
            return dt.today()

    @property
    def start(self) -> str:
        return self._start.strftime(strftime)

    @start.setter
    def start(self, value: str) -> None:
        self._start = LinkMaker._do_date(value.lower())

    @property
    def end(self) -> str:
        return self._end.strftime(strftime)

    @end.setter
    def end(self, value: str) -> None:
        self._end = LinkMaker._do_date(value.lower())

    @property
    def school(self) -> str:
        return self._school_link

    @school.setter
    def school(self, school: str) -> None:
        self._school_link = Database.Schools.link(school)
        if self._school_link:
            self._school = school

    @property
    def program(self) -> str:
        return Database.Programs.link(self._school, self._program)

    @program.setter
    def program(self, program: str) -> None:
        if self._school:
            self._program = program

    @property
    def course(self) -> str:
        return Database.Programs.link(self._school, self._course)

    @course.setter
    def course(self, course: str) -> None:
        if self._school:
            self._course = course

    @property
    def link(self) -> str:
        if not self._end or (self._start and self._end < self._start):
            self._end = self._start

        if not (self._start and self._school_link and (self.program or self.course)):
            return ''

        link = self._school_link + ical_link + start + self.start + end + self.end + resource
        if self.program:
            link += 'p.' + self.program + ','
        if self.course:
            link += 'c.' + self.course + ','

        return link

    @property
    def events(self) -> list:
        events = icalevents.events(url=self.link, end=self._end + td(days=1))
        # timedelta 1 day because wanted date is day(0:00:00-23:59:59) but true date
        # is day(0:00:00 - 0:00:00). adding a day resolves this
        _events = []
        _start = len('Kurs.grp: ')
        sign = ' Sign: '
        moment = ' Moment: '

        for event in events:
            _event = {'day': event.start.date()}
            if event.summary.find(sign) >= 0:
                _event['moment'] = event.summary[_start: event.summary.find(sign)]
                _event['professor'] = event.summary[event.summary.find(sign) + len(sign): event.summary.find(moment)]
            else:
                if event.summary.find(' Program: ') >= 0:
                    _event['moment'] = event.summary[event.summary.find(moment) + len(moment):
                                                     event.summary.find(' Program: ')]
                else:
                    _event['moment'] = event.summary[event.summary.find(moment) + len(moment):]
            start_time = event.start.astimezone(timezone('Europe/Stockholm')).strftime('%X')
            end_time = event.end.astimezone(timezone('Europe/Stockholm')).strftime('%X')
            # _event['when'] = event.start.astimezone(timezone('Europe/Stockholm')).strftime('%Y-%m-%d') + ' ' + \
            _event['when'] = start_time + ' - ' + end_time
            if event.location:
                _event['room'] = event.location
            _events.append(_event)

        return _events

    @events.setter
    def events(self, value):
        return
