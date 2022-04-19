import datetime
import sys

import discord
from discord import Embed
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


def events_output(school: str, program: str, start: str, end: str) -> Embed:
    lm = LinkMaker()
    lm.school = school
    lm.program = program
    lm.start = start
    lm.end = end
    events = lm.events

    _embed = Embed(timestamp=datetime.datetime.now(), colour=discord.Colour.blue())
    _embed.set_footer(text='KronoxBot', icon_url='https://kronox.oru.se/images/favicon.gif')
    if not events:
        _embed.description = f"""```KronoxBot found no events between {start} and {end} for {program} at {school}```"""
        return _embed
    else:
        for event in events:
            _embed.description = '#' + event['moment'] + '\n'
            if 'professor' in event:
                _embed.description = _embed.description + '##' + event['professor'] + '\n'
            _embed.add_field(name='When', value=event['when'])
            _embed.add_field(name='Where', value=event['room'])

        return _embed


@kronox.command(name='schema', description='Get your Kronox schedule')
async def schema(
        ctx: ApplicationContext,
        school: Option(str, "Pick a school", autocomplete=Autocomplete.schools),
        program: Option(str, "Pick a program", autocomplete=Autocomplete.programs),
        start: Option(str, "Today, tmw, YYYY-MM-DD, days=3, weeks=1", default='today'),
        end: Option(str, "Today, tmw, YYYY-MM-DD, days=3, weeks=1", default='today')
):
    # Autocomplete.do_last_used(ctx.user.id, school, program, course)
    Autocomplete.do_last_used(ctx.user.id, school, program)
    await ctx.respond(embed=events_output(school, program, start, end))


saved = {}


@kronox.command(name='save', description='Save custom Kronox commands')
async def save(
        ctx: ApplicationContext,
        name: Option(str, 'Choose a name to identify your saved options'),
        school: Option(str, "Pick a school", autocomplete=Autocomplete.schools),
        program: Option(str, "Pick a program", autocomplete=Autocomplete.programs),
        start: Option(str, "Today, tmw, YYYY-MM-DD, days=3, weeks=1", default='today'),
        end: Option(str, "Today, tmw, YYYY-MM-DD, days=3, weeks=1", default='today')
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
    await ctx.respond(embed=events_output(_saved['school'], _saved['program'], _saved['start'], _saved['end']))


@bot.slash_command(guilds_ids=guilds)
async def embed(
        ctx: ApplicationContext
):
    _embed = Embed(
        description='Test', colour=discord.Colour.blue(), title='Title test', timestamp=datetime.datetime.now(),
        url='https://kronox.oru.se',
    )
    _embed.set_footer(text='KronoxBot', icon_url='https://kronox.oru.se/images/favicon.gif')
    _embed.add_field(name='field', value='poopoo peepee')

    await ctx.respond(embed=_embed)


bot.run(config['token'])  # run the bot with the token
