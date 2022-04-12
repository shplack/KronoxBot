import sys

import discord
from discord import Option, ApplicationContext
from dotenv import dotenv_values

from Autocompletions import Autocomplete
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

last_used = {}


@bot.event
async def on_ready():
    print('KronoxBot ready!')


kronox = bot.create_group(name="kronox", description="Get Kronox schedule", guild_ids=guilds)


def events_output(school: str, program: str, start: str, end: str):
    lm = LinkMaker()
    lm.school = school
    lm.program = program
    lm.start = start
    lm.end = end
    events = lm.events

    if not events:
        return f"""```KronoxBot found no events between {start} and {end} for {program} at {school}```"""
    else:
        return '```' + '\n'.join(events) + '```'


@kronox.command(name='schema', description='Get your Kronox schedule')
async def schema(
        ctx: ApplicationContext,
        school: Option(str, "Pick a school", autocomplete=Autocomplete.schools),
        program: Option(str, "Pick a program", autocomplete=Autocomplete.programs),
        start: Option(str, "Today, tmw, or date <YYYY-MM-DD>", default='today'),
        end: Option(str, "Today, tmw, or date <YYYY-MM-DD>", default='today')
):
    # Autocomplete.do_last_used(ctx.user.id, school, program, course)
    Autocomplete.do_last_used(ctx.user.id, school, program)
    await ctx.respond(events_output(school, program, start, end))


saved = {}


@kronox.command(name='save', description='Save custom Kronox commands')
async def save(
        ctx: ApplicationContext,
        name: Option(str, 'Choose a name to identify your saved options'),
        school: Option(str, "Pick a school", autocomplete=Autocomplete.schools),
        program: Option(str, "Pick a program", autocomplete=Autocomplete.programs),
        start: Option(str, "Today, tmw, or date <YYYY-MM-DD>", default='today'),
        end: Option(str, "Today, tmw, or date <YYYY-MM-DD>", default='today')
):
    # Autocomplete.save(ctx.user.id, name, school, program, course, start, end)
    Autocomplete.save(ctx.user.id, name, school, program, start, end)

    await ctx.respond(f"""```Name: {name}
School: {school}
Program: {program}
Start: {start}
End: {end}```""")


@kronox.command(name='load', description='Load your saved commands')
async def load(
        ctx: ApplicationContext,
        name: Option(str, 'Choose a saved command', autocomplete=Autocomplete.load)
):
    _id = ctx.user.id
    if _id not in Autocomplete.saved or name not in Autocomplete.saved[_id]:
        await ctx.respond('```Use /save to first save a command```')
        return

    _saved = Autocomplete.saved[_id][name]
    await ctx.respond(events_output(_saved['school'], _saved['program'], _saved['start'], _saved['end']))


bot.run(config['token'])  # run the bot with the token
