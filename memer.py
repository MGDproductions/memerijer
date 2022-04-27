import sys
import time
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import aiohttp
import requests
import json
import configparser
import datetime
from datetime import timedelta
import sqlite3
import random
import praw
import discord
from bs4 import BeautifulSoup
import lxml
from deep_translator import GoogleTranslator

with open('config.json') as config_file:
    data = json.load(config_file)

intents = discord.Intents.default()
intents.members = True
intents.messages = True
client = Bot(command_prefix=['m.','M.'],intents=intents)
client.remove_command('help')
TOKEN = data['token']
DEVELOPER_KEY = data['developerkey']
apikey = data['apikey']
qrcodekey = data['qrcodekey']
redditclientid = data['rclientid']
redditsecret = data['rsecret']

with open("common-words.txt") as f:
            words = f.read().split('\n')

@client.event
async def on_ready():
    print('Connected to discord as: {0.user}'.format(client))
    print('done')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="memes (m.help)"))
    print('below me is how many servers i am in.')
    print({len(client.guilds)})
    for i in client.guilds:
        try:
            print(f"{i.name} - {i.id} - {i.member_count}")
        except:
            pass
        
@client.event
async def on_guild_join(guild):
    print("NIEUWE SERVER!")
    print(f"{guild.name} - {guild.id} - {guild.member_count}")
    channel = client.get_channel(794964662361260033)
    await channel.send("<@416525692772286464> AYY NIEUWE SERVER!")
    embed=discord.Embed(title=("Nieuwe server"), color=0xff0000)
    embed.add_field(name=(f"{guild.name}"), value=(f"{guild.id} - {guild.member_count}"), inline=False)
    await channel.send(embed=embed)

@client.command(name="poll")
async def poll(ctx, option1, option2, *, question):
    try:
        print((datetime.datetime.now() + timedelta(hours=2)).strftime('%d/%m/%Y %H:%M:%S'), ctx.message.content, ctx.message.guild.name, ctx.message.author.name)
    except:
        pass
    message = await ctx.send(f"```Nieuwe poll: \n{question}```\n**1️⃣ = {option1}**\n**2️⃣ = {option2}**")
    await message.add_reaction('1️⃣')
    await message.add_reaction('2️⃣')
    
@poll.error
async def on_command_error(error, ctx):
    await error.send("Maak polls met deze structuur: m.poll {1e antwoord} {2e antwoord} {vraag}")
    
@client.command(name="help")
async def help(ctx):
    try:
        print(ctx.message.content, ctx.message.guild.name, ctx.message.author.name)
    except:
        pass
    embed=discord.Embed(title="memerijer commands", color=0x00ff00)
    embed.add_field(name="m.meme", value="serveert je een engelse meme.", inline=False)
    embed.add_field(name="m.memerij", value="serveert je een nederlandse meme.", inline=False)
    embed.add_field(name="m.aww", value="serveert je een random foto waar je aww van zal zeggen.", inline=False)
    embed.add_field(name="m.woord", value="serveert je een random woord.", inline=False)
    embed.add_field(name="m.getal", value="serveert je een random getal tussen een max en een minimum. voorbeeld: m.getal 10 20.", inline=False)
    embed.add_field(name="m.game", value="serveert je een random steam game.", inline=False)
    embed.add_field(name="m.afbeelding", value="serveert je een random afbeelding van je gekozen zoekterm. voorbeeld: m.afbeelding kat", inline=False)
    embed.add_field(name="m.gif", value="serveert je een random gif.", inline=False)
    embed.add_field(name="m.gif {zoekterm}", value="serveert je een random gif van je gekozen zoekterm. voorbeeld: m.gif kat", inline=False) 
    embed.add_field(name="m.qr {link of tekst}", value="serveert je een qr code met je link of met je tekst. voorbeeld: m.qr www.mdproductions.nl", inline=False)
    embed.add_field(name="m.poll {1e antwoord} {2e antwoord} {vraag}", value="serveert je een poll. voorbeeld: m.poll friet patat friet of patat", inline=False)
    embed.add_field(name="m.invite", value="serveert je de invite link om de bot in je server te krijgen.", inline=False)    
    embed.add_field(name="m.credits", value="serveert je de credits voor deze bot.", inline=False)
    await ctx.send(embed=embed)

@client.command(name="woord")
async def woord(ctx):
    try:
        print((datetime.datetime.now() + timedelta(hours=2)).strftime('%d/%m/%Y %H:%M:%S'), ctx.message.content, ctx.message.guild.name, ctx.message.author.name)
    except:
        pass
    word = random.choice(words)
    await ctx.send(word)
   
@client.command(name="getal")
async def getal(ctx):
    try:
        print((datetime.datetime.now() + timedelta(hours=2)).strftime('%d/%m/%Y %H:%M:%S'), ctx.message.content, ctx.message.guild.name, ctx.message.author.name)
    except:
        pass
    try:
        splitmessage = ctx.message.content.split()
        startnumber = splitmessage[1]
        endnumber = splitmessage[2]
        randomnumber = random.randint(int(startnumber), int(endnumber))
        await ctx.send(randomnumber)
    except:
        await ctx.send(':warning: Er zit een fout in je command!')
    
@client.command(name="verkrijgservers")
@commands.is_owner()
async def servers(ctx):
    try:
        print((datetime.datetime.now() + timedelta(hours=2)).strftime('%d/%m/%Y %H:%M:%S'), ctx.message.content, ctx.message.guild.name, ctx.message.author.name)
    except:
        pass
    serveraantal = len(client.guilds)
    embed=discord.Embed(title=("Servers (" + str(serveraantal) + ")"), color=0xff0000)
    for i in client.guilds:
        try:
            embed.add_field(name=(f"{i.name}"), value=(f"{i.id} - {i.member_count}"), inline=False)
        except:
            pass
    await ctx.send(embed=embed)

@servers.error
async def on_command_error(error, ctx):
    await error.send(":warning: Je bent niet de eigenaar van deze bot en dan dus deze command niet gebruiken.")
    
@client.command(name="memerij")
async def memerij(ctx):
    try:
        print((datetime.datetime.now() + timedelta(hours=2)).strftime('%d/%m/%Y %H:%M:%S'), ctx.message.content, ctx.message.guild.name, ctx.message.author.name)
    except:
        pass
    await ctx.trigger_typing()
    r = praw.Reddit(check_for_updates='false', check_for_async='false', user_agent='memerijer bot discord', client_id=redditclientid, client_secret=redditsecret)  
    posts = r.subreddit('NederlandseMemes').random()
    while True:
        if posts.url.startswith('https://i.redd.it'):
            break
        elif posts.over_18:
            print("post is NSFW")
            posts = r.subreddit('NederlandseMemes').random()
        else:
            print("post is geen afbeelding")
            posts = r.subreddit('NederlandseMemes').random()
    embedVar = discord.Embed(color=0x00ff00)
    embedVar.set_image(url=posts.url)
    embedVar.add_field(name=posts.title, value=("[link](http://www.reddit.com/" + posts.id + ")"), inline=False)
    embedVar.set_footer(text="gekregen van r/NederlandseMemes")
    await ctx.send(embed=embedVar)
        
@client.command(name="meme")
async def meme(ctx):
    try:
        print((datetime.datetime.now() + timedelta(hours=2)).strftime('%d/%m/%Y %H:%M:%S'), ctx.message.content, ctx.message.guild.name, ctx.message.author.name)
    except:
        pass
    await ctx.trigger_typing()
    r = praw.Reddit(check_for_updates='false', check_for_async='false', user_agent='memerijer bot discord', client_id=redditclientid, client_secret=redditsecret)  
    posts = r.subreddit('memes').random()
    while True:
        if posts.url.startswith('https://i.redd.it'):
            break
        elif posts.over_18:
            print("post is NSFW")
            posts = r.subreddit('memes').random()
        else:
            print("post is geen afbeelding")
            posts = r.subreddit('memes').random()
    embedVar = discord.Embed(color=0x00ff00)
    embedVar.set_image(url=posts.url)
    embedVar.add_field(name=posts.title, value=("[link](http://www.reddit.com/" + posts.id + ")"), inline=False)
    embedVar.set_footer(text=("gekregen van r/memes"))
    await ctx.send(embed=embedVar)

@client.command(name="aww")
async def meme(ctx):
    try:
        print((datetime.datetime.now() + timedelta(hours=2)).strftime('%d/%m/%Y %H:%M:%S'), ctx.message.content, ctx.message.guild.name, ctx.message.author.name)
    except:
        pass
    await ctx.trigger_typing()
    r = praw.Reddit(check_for_updates='false', check_for_async='false', user_agent='memerijer bot discord', client_id=redditclientid, client_secret=redditsecret)  
    posts = r.subreddit('aww').random()
    while True:
        if posts.url.startswith('https://i.redd.it'):
            break
        elif posts.over_18:
            print("post is NSFW")
            posts = r.subreddit('aww').random()
        else:
            print("post is geen afbeelding")
            posts = r.subreddit('aww').random()
    embedVar = discord.Embed(color=0x00ff00)
    embedVar.set_image(url=posts.url)
    embedVar.add_field(name=posts.title, value=("[link](http://www.reddit.com/" + posts.id + ")"), inline=False)
    embedVar.set_footer(text=("gekregen van r/aww"))
    await ctx.send(embed=embedVar)

        
@client.command(name="testconn")
async def test(ctx):
    try:
        print((datetime.datetime.now() + timedelta(hours=2)).strftime('%d/%m/%Y %H:%M:%S'), ctx.message.content, ctx.message.guild.name, ctx.message.author.name)
    except:
        pass
    await ctx.send('hey daar gast!')
    
@client.command(name="credits")
async def credits(ctx):
    try:
        print((datetime.datetime.now() + timedelta(hours=2)).strftime('%d/%m/%Y %H:%M:%S'), ctx.message.content, ctx.message.guild.name, ctx.message.author.name)
    except:
        pass
    embed=discord.Embed(color=0x0000FF)
    embed.add_field(name="memerijer bot", value="v3.2.1", inline=False)      
    embed.add_field(name="© MD productions 2022", value="[www.mdproductions.nl](https://www.mdproductions.nl)", inline=False)    
    await ctx.send(embed=embed)

@client.command(name="invite")
async def credits(ctx):
    try:
        print((datetime.datetime.now() + timedelta(hours=2)).strftime('%d/%m/%Y %H:%M:%S'), ctx.message.content, ctx.message.guild.name, ctx.message.author.name)
    except:
        pass
    await ctx.trigger_typing()
    embed=discord.Embed(title="memerijer invite", color=0x0000FF)     
    embed.add_field(name="Gebruik deze invite om de bot in je server te krijgen!", value="[invite link](https://top.gg/bot/776829080447746049)", inline=False)    
    await ctx.send(embed=embed)

@client.command(name="game")
async def game(ctx):
    try:
        print((datetime.datetime.now() + timedelta(hours=2)).strftime('%d/%m/%Y %H:%M:%S'), ctx.message.content, ctx.message.guild.name, ctx.message.author.name)
    except:
        pass
    await ctx.trigger_typing()
    r = requests.get('http://store.steampowered.com/explore/random/') 
    shorten = (r.url)
    await ctx.send(shorten.replace('?snr=1_239_random_', ''))
    
@client.command(name="qr")
async def qr(ctx):
    try:
        print((datetime.datetime.now() + timedelta(hours=2)).strftime('%d/%m/%Y %H:%M:%S'), ctx.message.content, ctx.message.guild.name, ctx.message.author.name)
    except:
        pass
    await ctx.trigger_typing()
    thing = ctx.message.content[5:]
    if thing == "":
        await ctx.send(':warning: uhh wtf doe je? geef me een link of tekst!')
    else:
        thinggood = thing.replace(' ','%20')
        if len(thinggood) > 1000:
            await ctx.send(':warning: oef die tekst is wel erg lang. qr codes kunnen alleen gemaakt worden tot 1000 karakters. (spaties tellen voor 3)')
        else:
            embedVar = discord.Embed(color=0x00ff00)
            url = ("https://api.qr-code-generator.com/v1/create?access-token=" + qrcodekey + "&qr_code_pattern=rounded-2&image_format=PNG&image_width=400&qr_code_text=" + thinggood)
            embedVar.set_image(url=(url))         
            await ctx.send(embed=embedVar)
            
@qr.error
async def on_command_error(error, ctx):
    await error.send(":warning: Kon deze qr code niet maken.")
            
@client.command(name="gif")
async def gif(ctx):
    try:
        print((datetime.datetime.now() + timedelta(hours=2)).strftime('%d/%m/%Y %H:%M:%S'), ctx.message.content, ctx.message.guild.name, ctx.message.author.name)
    except:
        pass
    await ctx.trigger_typing()
    message_random_nl = ctx.message.content[6:]
    if message_random_nl == "":
        message_random = random.choice(words)
    else:
        message_random = GoogleTranslator(source='nl', target='en').translate(message_random_nl)
    datetime_now = datetime.datetime.now()
    time = datetime_now.strftime("%d/%m/%Y %H:%M:%S")
    search_random = "https://api.tenor.com/v1/random?key={}&q={}&limit=5&media_filter=basic".format(apikey, message_random)
    random_request = requests.get(search_random)
    if random_request.status_code == 200:
        try:
            json_random = random_request.json()['results']
            gif = json_random[0]
            title = gif['title']
            ID = gif['id']
            url = gif['url']
            gif = gif.get("media")
            gif = gif[0]
            gif = gif.get("gif")
            gif = gif.get("url")
            if title == "":
                title = "None" 
                    
            await ctx.send(url)
        except:
            await ctx.send(":warning: Geen gif gevonden!")

@client.command(name="afbeelding")
async def afbeelding(ctx):
    try:
        print((datetime.datetime.now() + timedelta(hours=2)).strftime('%d/%m/%Y %H:%M:%S'), ctx.message.content, ctx.message.guild.name, ctx.message.author.name)
    except:
        pass
    if ctx.message.content[13:] == "":
        await ctx.send(':warning: Om een afbeelding te zoeken moet je me wel een zoekterm geven!')
    else:
        await ctx.trigger_typing()
        searchnl = ctx.message.content[13:]
        search = GoogleTranslator(source='nl', target='en').translate(ctx.message.content[13:])
        url = ('https://www.google.com/search?q=' + search.replace(" ", "+") + '&tbm=isch&safe=active')
        headers = {
            'Accept': 'text/html',
            'User-Agent': 'Chrome'
        }
        links = []
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, "lxml")
        images = soup.findAll('img')
        for image in images:
            links.append(image['src'])
        if links == []:
            await ctx.send(':warning: Geen afbeelding gevonden met die zoekterm!')
        else:
            links.pop()
            randomlink = random.choice(links)
            embedVar = discord.Embed(title=searchnl + " gevonden!", color=0x00ff00)
            embedVar.set_image(url=randomlink)
            try:
            	await ctx.send(embed=embedVar)
            except:
            	await ctx.send(':warning: Afbeelding gevonden maar niet kunnen sturen. Probeer opnieuw.')

@client.command(name="leave")
@commands.is_owner()
async def leave(ctx):
    leavethis = ctx.message.content[8:]
    if ctx.message.content[13:] == "":
        await ctx.send(':warning: Om een server te verlaten moet je me wel een id geven!')
    else:
        try:
            toleave = client.get_guild(int(leavethis))
            await toleave.leave()
            await ctx.send(leavethis + ' Verlaten!')
        except:
            await ctx.send(':warning: Kon deze server niet verlaten.')

@leave.error
async def on_command_error(error, ctx):
    await error.send(":warning: Je bent niet de eigenaar van deze bot en dan dus deze command niet gebruiken.")
    
@client.command(name="ping")
async def ping(ctx):
    try:
        print((datetime.datetime.now() + timedelta(hours=2)).strftime('%d/%m/%Y %H:%M:%S'), ctx.message.content, ctx.message.guild.name, ctx.message.author.name)
    except:
        pass
    await ctx.send(f'Pong! ({round(client.latency * 1000)}ms)')
    
@client.command(name="status")
@commands.is_owner()
async def status(ctx):
    try:
        print((datetime.datetime.now() + timedelta(hours=2)).strftime('%d/%m/%Y %H:%M:%S'), ctx.message.content, ctx.message.guild.name, ctx.message.author.name)
    except:
        pass
    newstatus = ctx.message.content[8:]
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=newstatus))
    await ctx.send('status veranderd!')
    
@status.error
async def on_command_error(error, ctx):
    await error.send(":warning: Je bent niet de eigenaar van deze bot en dan dus deze command niet gebruiken.")

print("Connecting to discord")
client.run(TOKEN)
