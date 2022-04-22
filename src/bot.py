import sys
from datetime import datetime

import discord
from discord import Embed
from discord import Option, ApplicationContext
from discord.ext.pages import Page, Paginator
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


def events_output(school: str, program: str, start: str, end: str) -> list[Page]:
    lm = LinkMaker()
    lm.school = school
    lm.program = program
    lm.start = start
    lm.end = end
    events = lm.events
    embeds = []
    pages = []

    def make_embed(title: str = '', description: str = '') -> Embed:
        default = Embed(timestamp=datetime.now(), colour=discord.Colour.blue(), title=title, description=description)
        default.set_footer(text='KronoxBot', icon_url='https://kronox.oru.se/images/favicon.gif')
        return default

    if not events:
        when = ''
        if start == end:
            when += f'on `{start}`'
        else:
            when += f'between `{start}` and `{end}`'
        _embed = make_embed(
            title='No events found',
            description=f'KronoxBot {when} found no events  for `{program}` at `{school}`'
        )
        embeds.append(_embed)
        pages.append(Page(embeds=embeds))
    else:
        current_day = None
        for event in events:
            if event['day'] != current_day:
                current_day = event['day']
                if embeds:
                    pages.append(Page(embeds=embeds))
                embeds = []
            _embed = make_embed(event['moment'], event['day'])
            if 'professor' in event:
                _embed.add_field(name='Who', value=event['professor'])
            _embed.add_field(name='When', value=event['when'])
            if 'room' in event:
                _embed.add_field(name='Where', value=event['room'])
            embeds.append(_embed)
        pages.append(Page(embeds=embeds))

    return pages


@kronox.command(name='schema', description='Get your Kronox schedule')
async def schema(
        ctx: ApplicationContext,
        school: Option(str, "Pick a school", autocomplete=Autocomplete.schools),
        program: Option(str, "Pick a program", autocomplete=Autocomplete.programs),
        start: Option(str, "Today, tmw, YYYY-MM-DD, days=3, weeks=1", default='today'),
        end: Option(str, "Today, tmw, YYYY-MM-DD, days=3, weeks=1", required=False)
):
    # Autocomplete.do_last_used(ctx.user.id, school, program, course)
    Autocomplete.do_last_used(ctx.user.id, school, program)
    if not end:
        end = start

    pages = events_output(school, program, start, end)
    await Paginator(pages=pages).respond(ctx.interaction)


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
    await schema(ctx, _saved['school'], _saved['program'], _saved['start'], _saved['end'])


@bot.slash_command(guilds_ids=guilds)
async def embed(
        ctx: ApplicationContext
):
    _embed = Embed(
        description='Test', colour=discord.Colour.blue(), title='Title test', timestamp=datetime.now(),
        url='https://kronox.oru.se',
    )
    _embed.set_footer(text='KronoxBot', icon_url='https://kronox.oru.se/images/favicon.gif')
    _embed.add_field(name='field', value='poopoo peepee')

    await ctx.respond(embed=_embed)


bot.run(config['token'])  # run the bot with the token
