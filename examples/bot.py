import argparse
from datetime import datetime
from io import StringIO
from typing import List

from discord.ext import commands
from icalevents import icalparser
from pytz import timezone

from examples import kronox
from examples.school import schools
from src.logger.botlogger import init_logger

keys = [
    'school',
    'start',
    'end',
    'timezone',
    'programs',
    'courses',
    'language'
]






if __name__ == '__main__':
    init_logger()
    bot = commands.Bot(command_prefix='kronox ', description='Get Kronox schedule')
    
    global argparser
    argparser = argparse.ArgumentParser(prog='KronoxBot')
    argparser.add_argument('-sc', '--school', nargs='?')
    argparser.add_argument('-st', '--start', nargs='?')
    argparser.add_argument('-e', '--end', nargs='?')
    argparser.add_argument('-tz', '--timezone', nargs='?')
    argparser.add_argument('-p', '--programs', nargs='+')
    argparser.add_argument('-c', '--courses', nargs='+')
    argparser.add_argument('-l', '--lang', nargs='?')


    
@bot.command()
async def test(ctx):
    await ctx.send("I am here to do your bidding!")


    
@bot.command()
async def schema(ctx, *args):
    if len(args) == 0:
       return # TODO: help
   
    if args[0] == 'help':
        help = StringIO()
        argparser.print_help(help)
        await ctx.send(f'```{help.getvalue()}```')
        return
   
    args = vars(argparser.parse_args(args))
    
    
    if not args or args == {}:
        help = StringIO()
        argparser.print_help(help)
        await ctx.send(f'```{help.getvalue()}```')
        return
    
    school = schools[args["school"]]
    
    tz = args["timezone"] and timezone(args["timezone"]) or timezone("Europe/Stockholm")
    
    start = args["start"]
    if not start or start == 'idag' or start == 'today':
        start = datetime.today()
    else:
        start = datetime.strptime(start, "%Y-%m-%d")
    start = tz.localize(start)
        
    end = args["end"]
    if end and end != 'idag' and end != 'today':
        end = datetime.strptime(end, "%Y-%m-%d")
        end = tz.localize(end)
        if end < start:
            ctx.send(f'```End time "{end.ctime()}" cannot be before start time "{start.ctime()}"```')
            return
    else:
        end = start
    
    lang = args["lang"] or "SV"
    
    programs = args["programs"]
    courses = args["courses"]
    
    if not (args["programs"] or args["courses"]):
        programs = ["Högskoleingenjör - Datateknik åk 2"]
    
    ical: List[icalparser.Event]
    ical = kronox.search(school, courses, programs, start, end, lang)
    if ical == []:
        await ctx.send('```No events found!```')
        return
        
    output = '```'
    for event in ical:
        output += event.start.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S") + ' '
        #'Kurs.grp: System- och programvaruutveckling Sign: fkl Moment: Lecture   Program: Högskoleingenjör - Datateknik åk 2-'
        output += event.summary[event.summary.find(' ')+1:event.summary.find('Sign: ')]
        output += str(event)[str(event).find('('):str(event).find(')')+1]
        output += '\n'
    output += '```'
    await ctx.send(output)
        
        
    
    # msg = [str(event) for event in kronox.search(school, courses, programs, start, end, lang)]
    # if msg == []:
    #     await ctx.send('```No events found!```')
    #     return
    
    # await ctx.send('```' + '\n'.join(msg) + '```')
    
    

bot.run("OTU4NDU2NDA0ODQxMjIyMTk1.YkNmFg.8oRXpUkaKTNVS7HWY1e_PFrvN6w")