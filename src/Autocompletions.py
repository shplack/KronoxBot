from discord import AutocompleteContext

from database.kronox_db import Database


class Autocomplete:
    last_used = {}
    saved = {}

    @classmethod
    async def schools(cls, ctx: AutocompleteContext):
        _id = ctx.interaction.user.id
        if ctx.value == '' and _id in cls.last_used and 'school' in cls.last_used[_id]:
            return [cls.last_used[_id]['school']]

        value = ctx.value.lower()

        schools = Database.Schools.all()
        acronyms = [acro.upper() for acro, x in schools.items() if acro.lower().find(value) >= 0]
        if acronyms:
            return acronyms

        locs = Database.Schools.Localizations.by_locale(ctx.interaction.locale)
        if locs:  # are there localizations for user's locale yet?
            schools = [loc for x, loc in locs if loc.lower().find(value) >= 0]
            if schools:
                return schools

        # user might be writing in swedish
        locs = Database.Schools.Localizations.by_locale('sv-SE')
        if locs != {}:  # are there localizations for swedish yet?
            schools = [loc for x, loc in locs if loc.lower().find(value) >= 0]
            if schools:
                return schools

        # last resort
        schools = Database.Schools.all()
        return [school for school in schools.values() if school.lower().find(value) >= 0]

    @classmethod
    async def programs(cls, ctx: AutocompleteContext):
        school = ctx.options['school']
        _id = ctx.interaction.user.id
        if ctx.value == '' and _id in cls.last_used:
            if 'school' in cls.last_used[_id] and 'program' in cls.last_used[_id]:
                if cls.last_used[_id]['school'] == school:
                    return [cls.last_used[_id]['program']]

        value = ctx.value.lower()
        locs = Database.Programs.Localizations.by_school_locale(school, ctx.interaction.locale)
        if locs:  # are there localizations for user's locale yet?
            return [loc for x, loc in locs if loc.lower().find(value) >= 0]
        programs = Database.Programs.by_school(school)
        if programs:
            return [program for program in programs if program.lower().find(value) >= 0]
        return []

    @classmethod
    async def courses(cls, ctx: AutocompleteContext):
        value = ctx.value.lower()
        school = ctx.options['school']
        # TODO: database courses

    @classmethod
    async def load(cls, ctx: AutocompleteContext):
        _id = ctx.interaction.user.id
        value = ctx.value.lower()
        if _id not in cls.saved:
            return []
        return [name for name in cls.saved[_id].keys() if name.lower().find(value) >= 0]

    @classmethod
    # def do_last_used(cls, _id: int, school: str, program: str, course: str):
    def do_last_used(cls, _id: int, school: str, program: str):
        def update_last_used(key, value):
            if value and key:
                if key not in cls.last_used[_id]:
                    cls.last_used[_id][key] = {}
                cls.last_used[_id][key] = value

        if _id not in cls.last_used:
            cls.last_used[_id] = {}

        update_last_used('school', school)
        update_last_used('program', program)
        # update_last_used('course', course)

    @classmethod
    # def save(cls, _id: int, school: str, program: str, course: str, start: str, end: str):
    def save(cls, _id: int, name: str, school: str, program: str, start: str, end: str):
        if _id not in cls.saved:
            cls.saved[_id] = {}

        cls.saved[_id][name] = {
            'school': school,
            'program': program,
            # 'course': course,
            'start': start,
            'end': end
        }
