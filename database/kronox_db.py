from functools import cache
from sqlite3 import Connection, connect


class Database:
    _conn: Connection

    @classmethod
    def __init__(cls, path: str):
        cls._conn = connect(path)

    @classmethod
    def close(cls):
        cls._conn.close()

    @classmethod
    def query(cls, sql, *args):
        cls._conn.execute(sql, args)
        cls._conn.commit()

    @classmethod
    def fetchone(cls, sql, *args):
        return cls._conn.execute(sql, args).fetchone()

    @classmethod
    def fetchall(cls, sql, *args):
        return cls._conn.execute(sql, args).fetchall()

    @classmethod
    def script(cls, sql):
        cls._conn.executescript(sql)
        cls._conn.commit()

    class Schools:
        @staticmethod
        @cache
        def add(name: str, acronym: str, link: str):
            query = 'INSERT INTO schools (name, acronym, link) VALUES (?, ?, ?);'
            Database.query(query, name, acronym, link)

        @staticmethod
        @cache
        def all() -> dict:
            query = 'SELECT name, acronym FROM schools;'
            results = Database.fetchall(query)
            return {acronym: name for name, acronym in results}

        @staticmethod
        @cache
        def by_acronym(acronym: str) -> str:
            query = f'SELECT name FROM schools WHERE acronym = ?;'
            results = Database.fetchone(query, acronym)
            return results == [] and '' or results[0]

        @staticmethod
        @cache
        def by_name(name: str) -> str:
            query = f'SELECT acronym FROM schools WHERE name = ?;'
            results = Database.fetchone(query, name)
            return results == [] and '' or results[0]

        class Localizations:
            @staticmethod
            @cache
            def all() -> dict:
                query = 'SELECT school, locale, localization FROM school_localization;'
                results = Database.fetchall(query)

                localizations = {}
                for name, locale, localization in results:
                    if name not in localizations:
                        localizations[name] = {}
                    localizations[name][locale] = localization
                return localizations

            @staticmethod
            @cache
            def by_locale(locale: str) -> list[tuple[str, str, str]]:
                return Database.fetchall("""
                    SELECT acronym, localization 
                    FROM school_localization 
                    INNER JOIN schools
                    ON school_localization.school = schools.name
                    WHERE locale = ?;
                """, locale)

            @staticmethod
            @cache
            def by_acronym(acronym: str) -> list[tuple[str, str, str]]:
                return Database.fetchall("""
                    SELECT acronym, school, localization 
                    FROM school_localization 
                    INNER JOIN schools
                    ON school_localization.school = schools.name
                    WHERE acronym = ?;
                """, acronym)

            @staticmethod
            @cache
            def by_school(school: str) -> list[tuple[str, str, str]]:
                return Database.fetchall("""
                    SELECT acronym, school, localization 
                    FROM school_localization 
                    INNER JOIN schools
                    ON school_localization.school = schools.name
                    WHERE school = ?;
                """, school)

    class Programs:
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
        def by_school(school: str) -> list:
            query = 'SELECT name FROM programs WHERE school = ?;'
            results = Database.fetchall(query, school)
            return results and [program for program, in results] or []

        class Localizations:
            @staticmethod
            @cache
            def all() -> dict:
                query = 'SELECT school, program, locale, localization FROM program_localization;'
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
            def by_locale(locale: str) -> dict:
                query = 'SELECT school, program, localization FROM program_localization WHERE locale = ?;'
                results = Database.fetchall(query, locale)

                localizations = {}
                for school, program, localization in results:
                    if school not in localizations:
                        localizations[school] = {}
                    localizations[school][program] = localization
                return localizations

            @staticmethod
            @cache
            def by_school(school: str) -> dict:
                query = 'SELECT program, locale, localization FROM program_localization WHERE school = ?;'
                results = Database.fetchall(query, school)

                localizations = {}
                for program, locale, localization in results:
                    if program not in localizations:
                        localizations[program] = {}
                    localizations[program][locale] = localization
                return localizations

            @staticmethod
            @cache
            def by_school_locale(school: str, locale: str) -> list[tuple]:
                query = """
                SELECT program, localization
                FROM program_localization 
                INNER JOIN schools s on program_localization.school = s.name
                WHERE (school = ? OR acronym = ?) AND locale = ?;
                """
                return Database.fetchall(query, school, school, locale)
