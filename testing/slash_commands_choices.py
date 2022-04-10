from functools import cache

import discord
from discord import Option, AutocompleteContext, ApplicationContext

from database.kronox_db import Database

Database('../database/kronox_db.sqlite')
bot = discord.Bot(intents=discord.Intents.all())

guilds = [958457225096085534]


@bot.event
async def on_ready():
    print('bot tester ready!')


class Autocomplete:
    @staticmethod
    async def schools(ctx: AutocompleteContext):
        locs = Database.Schools.Localizations.by_locale(ctx.interaction.locale)
        return [acro.upper() for acro, x in locs if acro.lower().find(ctx.value.lower()) >= 0] or \
               [loc for x, loc in locs if loc.lower().find(ctx.value.lower()) >= 0]

    @staticmethod
    async def programs(ctx: AutocompleteContext):
        school = ctx.options['school']
        locs = Database.Programs.Localizations.by_school_locale(school, ctx.interaction.locale)
        print(school, locs, ctx.interaction.locale)
        return [loc for x, loc in locs if loc.lower().find(ctx.value.lower()) >= 0]


@bot.slash_command(guild_ids=guilds)
async def kronox(
        ctx: ApplicationContext,
        school: Option(str, "Pick a school", autocomplete=Autocomplete.schools),
        program: Option(str, "Pick a program", autocomplete=Autocomplete.programs)
):
    ctx.respond(school)


@cache
async def idk(ctx: AutocompleteContext):
    return ['1', '2', '3']


@bot.slash_command(guild_ids=guilds)
async def test(
        ctx: ApplicationContext,
        test: Option(str, 'test', autocomplete=idk)
):
    ctx.respond(test)


bot.run("OTU5NzMxMjc1MDY3OTczNjMy.YkgJZg.848kVCV4EAweusY7TNfVYWtTUzs")  # run the bot with the token
