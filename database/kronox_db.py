import os
import sqlite3
from typing import Iterable


class Database:

    def __init__(self, path: str, init: bool = False):
        if path != ':memory:':
            if os.path.isdir(path):
                raise FileNotFoundError(f'This is a directory: {path}')
            if os.path.exists(path) and not os.access(path, os.R_OK):
                raise OSError(f'You do not have permission to read file: {path}')

        self._conn = sqlite3.connect(path)
        self.path = path
        print(f'Connected to sqlite3 database at "{path}"')

    def __str__(self):
        return f'{sqlite3.version} at {self.path}'

    def close(self):
        if self._conn:
            self._conn.close()

    def query(self, query: str, *args: Iterable):
        cursor = self._conn.cursor()
        if len(args) > 0:
            cursor.execute(query, args)
        else:
            cursor.execute(query)
        self._conn.commit()

    def script(self, script: str):
        cursor = self._conn
        cursor.executescript(script)
        self._conn.commit()

    def add_school(self, name: str, acronym: str, link: str):
        query = 'INSERT INTO schools (name, acronym, link) VALUES (?, ?, ?);'
        self.query(query, name, acronym, link)

    def add_program(self, program_name: str, link: str, school_name: str):
        query = 'INSERT INTO programs (name, link, school) VALUES (?, ?, ?)'
        self.query(query, program_name, link, school_name)

    def add_subprogram(self, school_name: str, program_name: str, subprogram_name: str, link: str):
        query = 'INSERT INTO subprograms (school, program, name, link) VALUES (?, ?, ?, ?);'
        self.query(query, school_name, program_name, subprogram_name, link)

    def add_course(self, course_name: str, link: str, school_name: str):
        query = 'INSERT INTO courses (name, link, school) VALUES (?, ?, ?);'
        self.query(query, course_name, link, school_name)

    def get_schools(self, *columns: str) -> dict or None:
        if len(columns) == 0:
            return

        column_names = ['name', 'acronym', 'link']
        if not set(column_names).intersection(set(columns)):
            return

        query = f'select {", ".join(columns)} from schools;'
        return self._conn.cursor().execute(query).fetchall()

    def get_programs(self, school: str, *columns: str) -> dict or None:
        if len(columns) == 0 or school == '':
            return

        column_names = ['name, link']
        if not set(column_names).intersection(set(columns)):
            return

        query = f'select {", ".join(columns)} from programs where school = ?'
        return self._conn.cursor().execute(query, (school,)).fetchall()

    def get_subprograms(self, school: str, program: str, *columns: str) -> dict or None:
        if len(columns) == 0 or school == '' or program == '':
            return

        column_names = ['name', 'link']
        if not set(column_names).intersection(set(columns)):
            return

        query = f'select {", ".join(columns)} from subprograms where school = ? and program = ?'
        return self._conn.cursor().execute(query, (school, program)).fetchall()

    def get_courses(self, school: str, *columns: str) -> dict or None:
        if len(columns) == 0 or school == '':
            return

        column_names = ['name, link']
        if not set(column_names).intersection(set(columns)):
            return

        query = f'select {", ".join(columns)} from courses where school = ?'
        return self._conn.cursor().execute(query, (school,)).fetchall()

    @property
    def conn(self):
        return self._conn
