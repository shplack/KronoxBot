from functools import cache
from sqlite3 import Connection, connect


class Database:
    _conn: Connection

    @classmethod
    def __init__(cls, path: str) -> None:
        cls._conn = connect(path)

    @classmethod
    def close(cls) -> None:
        cls._conn.close()

    @classmethod
    def query(cls, sql, *args) -> None:
        cls._conn.execute(sql, args)
        cls._conn.commit()

    @classmethod
    def fetchone(cls, sql, *args):
        return cls._conn.execute(sql, args).fetchone()

    @classmethod
    def fetchall(cls, sql, *args) -> list[tuple] or list:
        return cls._conn.execute(sql, args).fetchall()

    @classmethod
    def script(cls, sql) -> None:
        cls._conn.executescript(sql)
        cls._conn.commit()

    class Schools:
        @staticmethod
        def add(name: str, acronym: str, link: str) -> None:
            query = 'INSERT INTO schools (name, acronym, link) VALUES (?, ?, ?);'
            Database.query(query, name, acronym, link)

        @staticmethod
        @cache
        def all() -> dict[str, str]:
            query = 'SELECT name, acronym FROM schools;'
            results = Database.fetchall(query)
            return {acronym: name for name, acronym in results}

        @staticmethod
        @cache
        def get_link(school: str) -> str:
            query = 'SELECT link FROM schools WHERE name = ? OR acronym = ?;'
            results = Database.fetchone(query, school, school)
            return results == [] and '' or results[0]

        @staticmethod
        @cache
        def by_acronym(acronym: str) -> str:
            query = f'SELECT name FROM schools WHERE acronym = ?;'
            results = Database.fetchone(query, acronym)
            return results == [] and '' or results[0]

        @staticmethod
        @cache
        def by_name(name: str) -> str:
            query = 'SELECT acronym FROM schools WHERE name = ?;'
            results = Database.fetchone(query, name)
            return results == [] and '' or results[0]

        class Localizations:
            @staticmethod
            def add(school: str, locale: str, localization: str) -> None:
                query = 'INSERT INTO school_localizations (school, locale, localization) VALUES (?, ?, ?);'
                Database.query(query, school, locale, localization)

            @staticmethod
            @cache
            def all() -> dict[str, dict[str, str]] or {}:
                query = 'SELECT school, locale, localization FROM school_localizations;'
                results = Database.fetchall(query)

                localizations = {}
                for name, locale, localization in results:
                    if name not in localizations:
                        localizations[name] = {}
                    localizations[name][locale] = localization
                return localizations

            @staticmethod
            @cache
            def by_locale(locale: str) -> list[tuple[str, str]] or None:
                return Database.fetchall("""
                    SELECT acronym, localization 
                    FROM school_localizations 
                    INNER JOIN schools
                    ON school_localizations.school = schools.name
                    WHERE locale = ?;
                """, locale)

            @staticmethod
            @cache
            def by_acronym(acronym: str) -> list[tuple[str, str, str]] or None:
                return Database.fetchall("""
                    SELECT acronym, school, localization 
                    FROM school_localizations 
                    INNER JOIN schools
                    ON school_localizations.school = schools.name
                    WHERE acronym = ?;
                """, acronym)

            @staticmethod
            @cache
            def by_school(school: str) -> list[tuple[str, str, str]] or None:
                return Database.fetchall("""
                    SELECT acronym, school, localization 
                    FROM school_localizations 
                    INNER JOIN schools
                    ON school_localizations.school = schools.name
                    WHERE school = ?;
                """, school)

    class Programs:
        @staticmethod
        def add(name: str, school: str, link: str) -> None:
            query = 'INSERT INTO programs (name, school, link) VALUES (?, ?, ?);'
            Database.query(query, name, school, link)

        @staticmethod
        @cache
        def all() -> dict[str, list]:
            query = 'SELECT school, name FROM programs;'
            results = Database.fetchall(query)

            programs: dict[str, list] = {}
            for school, program in results:
                if school not in programs:
                    programs[school] = []
                programs[school].append(program)
            return programs

        @staticmethod
        @cache
        def by_school(school: str) -> list[str] or []:
            query = """
            SELECT programs.name FROM programs 
            INNER JOIN schools on programs.school = schools.name
            WHERE school = ? OR acronym = ?;"""
            results = Database.fetchall(query, school, school)
            return results and [program for program, in results] or []

        class Localizations:
            @staticmethod
            def add(school: str, program: str, locale: str, localization: str) -> None:
                query = 'INSERT INTO program_localizations (school, program, locale, localization) VALUES (?, ?, ?, ?);'
                Database.query(query, school, program, locale, localization)

            @staticmethod
            @cache
            def all() -> dict[str, dict[str, dict[str, str]]]:
                query = 'SELECT school, program, locale, localization FROM program_localizations;'
                results = Database.fetchall(query)

                localizations = {}
                for school, program, locale, localization in results:
                    if school not in localizations:
                        localizations[school] = {}
                    if program not in localizations[school]:
                        localizations[program] = {}
                    localizations[school][program][locale] = localization
                return localizations

            @staticmethod
            @cache
            def by_locale(locale: str) -> dict[str, dict[str, str]] or {}:
                query = 'SELECT school, program, localization FROM program_localizations WHERE locale = ?;'
                results = Database.fetchall(query, locale)

                localizations = {}
                for school, program, localization in results:
                    if school not in localizations:
                        localizations[school] = {}
                    localizations[school][program] = localization
                return localizations

            @staticmethod
            @cache
            def by_school(school: str) -> dict[str, dict[str, str]] or {}:
                query = 'SELECT program, locale, localization FROM program_localizations WHERE school = ?;'
                results = Database.fetchall(query, school)

                localizations = {}
                for program, locale, localization in results:
                    if program not in localizations:
                        localizations[program] = {}
                    localizations[program][locale] = localization
                return localizations

            @staticmethod
            @cache
            def by_school_locale(school: str, locale: str) -> list[tuple[str, str]] or None:
                query = """
                SELECT program, localization
                FROM program_localizations 
                INNER JOIN schools s on program_localizations.school = s.name
                WHERE (school = ? OR acronym = ?) AND locale = ?;
                """
                return Database.fetchall(query, school, school, locale)

        class Courses:
            @staticmethod
            def add(school: str, course: str, link: str) -> None:
                query = 'INSERT INTO courses (name, link, school) VALUES (?, ?, ?);'
                Database.query(query, school, course, link)

            @staticmethod
            @cache
            def all() -> list[tuple[str, str]] or None:
                query = 'SELECT school, name FROM courses;'
                return Database.fetchall(query)

            @staticmethod
            @cache
            def by_school(school: str) -> list[str] or None:
                query = """
                SELECT courses.name FROM courses
                INNER JOIN schools on courses.school = schools.name
                WHERE schools.name = ? OR schools.acronym = ?;
                """
                return Database.fetchall(query, school, school)

            class Localizations:
                @staticmethod
                def add(school: str, course: str, locale: str, localization: str) -> None:
                    query = """
                    INSERT INTO course_localizations 
                    (school, course, locale, localization) VALUES (?, ?, ?, ?);
                    """
                    Database.query(query, school, course, locale, localization)

                @staticmethod
                @cache
                def all() -> dict[str, dict[str, dict[str, str]]]:
                    query = 'SELECT school, course, locale, localization FROM course_localizations;'
                    results = Database.fetchall(query)

                    localizations = {}
                    for school, course, locale, localization in results:
                        if school not in localizations:
                            localizations[school] = {}
                        if course not in localizations[school]:
                            localizations[school][course] = {}
                        localizations[school][course][locale] = localization
                    return localizations

                @staticmethod
                @cache
                def by_locale(locale: str) -> dict[str, dict[str, str]]:
                    query = 'SELECT school, course, localization FROM course_localizations;'
                    results = Database.fetchall(query, locale)

                    localizations = {}
                    for school, course, localization in results:
                        if school not in localizations:
                            localizations[school] = {}
                        localizations[school][course] = localization
                    return localizations

                @staticmethod
                @cache
                def by_school_locale(school: str, locale: str) -> list[tuple[str, str]] or None:
                    query = """
                    SELECT course, localization FROM course_localizations
                    INNER JOIN schools on course_localizations.school = schools.name
                    WHERE (schools.name = ? OR schools.acronym = ?) AND locale = ?;
                    """
                    return Database.fetchall(query, school, locale)
