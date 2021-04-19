import threading
import os
import aiocron
import discord
from discord.ext import commands, tasks
from leaderboardBot import LeaderBoardBot
from parseRegion import parseRegion

bot = commands.Bot(command_prefix='!')

emotes = [
    'liiHappyCat',
    'liiCat',
    'ninaisFEESH'
]

def getEmbedObject(text, player, command):
    embed = discord.Embed(title=f'{player}\'s {command}', description=text)

    return embed

def removeTwitchEmotes(s):
    for key in emotes:
        s = s.replace(key, '')

    return s

@bot.command()
async def bgrank(ctx, *args):
    args = args or ['lii']
    args = args[:2]

    # Handle !bgrank EU for example
    if parseRegion(args[0]):
        region = parseRegion(args[0])
        args = ['lii', region]

    response = removeTwitchEmotes(leaderboardBot.getRankText(*args))

    if len(args) >= 2:
        region = args[1]
        if parseRegion(region) is None:
            response = "Invalid region provided.\n" + response
        
    await ctx.send(embed = getEmbedObject(removeTwitchEmotes(response), args[0], 'rank'))

@bot.command()
async def bgdaily(ctx, *args):
    args = args or ['lii']
    args = args[:2]

    # Handle !bgdaily EU for example
    if parseRegion(args[0]):
        region = parseRegion(args[0])
        args = ['lii', region]

    response = leaderboardBot.getDailyStatsText(*args)

    if len(args) >= 2:
        region = args[1]
        if parseRegion(region) is None:
            response = "Invalid region provided.\n" + response
    
    await ctx.send(embed = getEmbedObject(removeTwitchEmotes(response), args[0], 'daily'))

@bot.command()
async def goodbot(ctx):
    await ctx.send(':robot: Just doing my job :robot:')

@aiocron.crontab('59 2 * * *')
async def sendDailyRecap():
    climbers = leaderboardBot.getHighestClimbers(5)
    hardcore_gamers = leaderboardBot.getHardcoreGamers(5)

    climbersText = '**The top 5 gains were by:** \n'
    hardcore_gamersText = '**The top 5 grinders were:** \n'

    for index, climber in enumerate(climbers):
        climbersText += f"{index+1}. **{climber['Tag']}** climbed a total of **{climber['Change']}** from {climber['Start']} to {climber['End']} in the {climber['Region']} region \n"

    for index, hardcore_gamer in enumerate(hardcore_gamers):
        hardcore_gamersText += f"{index+1}. **{hardcore_gamer['Tag']}** played a total of **{hardcore_gamer['Gamecount']}** games in the {hardcore_gamer['Region']} region \n"

    text = climbersText + '\n' + hardcore_gamersText

    embed = discord.Embed(title='Daily Recap', description=text)

    dedicated_channel = bot.get_channel(811468284394209300)
    await dedicated_channel.send(embed=embed)

leaderboardBot = LeaderBoardBot()

bot.run(os.environ['DISCORD_TOKEN'])

while True:
    pass