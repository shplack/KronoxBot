import sys

import discord
from discord import Option, AutocompleteContext, ApplicationContext
from dotenv import dotenv_values

from database.kronox_db import Database
from src.kronox import LinkMaker

config = None
try:
    config = dotenv_values(sys.argv[1])
except:
    config = dotenv_values('.env')

Database(config['db'])

bot = discord.Bot(intents=discord.Intents.default())

guilds = [int(guild) for guild in config['guilds'].split(',')]


@bot.event
async def on_ready():
    print('KronoxBot ready!')


class Autocomplete:
    @staticmethod
    async def schools(ctx: AutocompleteContext):
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

    @staticmethod
    async def programs(ctx: AutocompleteContext):
        value = ctx.value.lower()
        school = ctx.options['school']
        locs = Database.Programs.Localizations.by_school_locale(school, ctx.interaction.locale)
        if locs:  # are there localizations for user's locale yet?
            return [loc for x, loc in locs if loc.lower().find(value) >= 0]
        programs = Database.Programs.by_school(school)
        if programs:
            return [program for program in programs if program.lower().find(value) >= 0]
        return []

    @staticmethod
    async def courses(ctx: AutocompleteContext):
        value = ctx.value.lower()
        school = ctx.options['school']
        # TODO: database courses


@bot.slash_command(guild_ids=guilds)
async def kronox(
        ctx: ApplicationContext,
        school: Option(str, "Pick a school", autocomplete=Autocomplete.schools),
        program: Option(str, "Pick a program", autocomplete=Autocomplete.programs),
        start: Option(str, "Today, tmw, or date <YYYY-MM-DD>", default='today'),
        end: Option(str, "Today, tmw, or date <YYYY-MM-DD>", default='today')
):
    lm = LinkMaker()
    lm.school = school
    lm.program = program
    lm.start = start
    lm.end = end
    events = lm.events
    if not events:
        await ctx.respond(f"""```
        KronoxBot found no events between {lm.start} and {lm.end} for {lm.program} at {lm.school}
        ```""")
    else:
        await ctx.respond('```' + '\n'.join(events) + '```')


bot.run(config['token'])  # run the bot with the token
