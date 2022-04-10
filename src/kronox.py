from functools import cache

from database.kronox_db import Database

Database("../database/kronox_db.sqlite")  # TODO: remove!

ical_link = 'setup/jsp/SchemaICAL.ics'
start = '?startDatum='
end = '?slutDatum='
resource = '?resurser='


class MakeLink:
    @staticmethod
    @cache
    def program(school: str, program: str) -> str:
        school_link = Database.Schools.link(school)
        if not school_link:
            assert school_link != ''

        program_link = Database.Programs.link(school, program)
        if not program_link:
            assert program_link != ''

        return school_link + ical_link + start + 'idag' + resource + program_link


print(MakeLink.program('ORU', 'Högskoleingenjör - Datateknik åk 2'))
