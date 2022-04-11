import datetime
from datetime import datetime as dt, timedelta as td

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
        self._program_link = None
        self._course_link = None

    @staticmethod
    def _do_date(_input: str) -> datetime.date:
        # TODO: db lookup localizations (today, tmw, etc)
        # TODO: check if value is alpha/numeric to check if shorthand given or straight-up a date

        tdy = ['today', 'tdy', 'idag'], td(days=0)
        tmw = ['tmorrow', 'tmw', 'imorn', 'imorgon', 'i morgon'], td(days=1)
        omw = ['overmorrow', 'over morrow', 'omw', 'imorn', 'imorgon', 'i morgon'], td(days=2)

        for acceptables, delta in [tdy, tmw,omw]:
            if _input in acceptables:
                return (dt.today() + delta).date()
        try:
            return dt.strptime(_input, '%Y-%m-%d')
        except ValueError as e:
            print(e, _input)
        finally:
            return dt.today().date()

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
        return self._program_link

    @program.setter
    def program(self, program: str) -> None:
        if self._school:
            self._program_link = Database.Programs.link(self._school, program)

    @property
    def course(self) -> str:
        return self._course_link

    @course.setter
    def course(self, course: str) -> None:
        if self._school:
            self._course_link = Database.Programs.link(self._school, course)

    @property
    def link(self) -> str:
        if not self._end or (self._start and self._end < self._start):
            self._end = self._start

        if not (self._start and self._school_link and (self._program_link or self._course_link)):
            return ''

        link = self._school_link + ical_link + start + self.start + end + self.end + resource
        if self._program_link:
            link += 'p.' + self._program_link + ','
        if self._course_link:
            link += 'c.' + self._course_link + ','

        return link
