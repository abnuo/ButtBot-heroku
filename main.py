import shlex, subprocess
import copy
import discord
import discord.utils
from discord.ext import commands
from urllib.parse import unquote
import urllib.parse as urlparse
from urllib.parse import parse_qs
import os
import ast
import asyncio
import aiofiles
from concurrent.futures import ProcessPoolExecutor
import time
import random
import tracery
import requests
import json
import itertools
import string
import markovify
from tracery.modifiers import base_english
token = os.environ['WinTokeny']
msglist = []
msglistwa = []
statesize = 1
memeybear = ["Thicc", "Chonky", "Big", "Lil"]
memeygummy = ["Bonkus", "Yeetus", "Yeezus", "Bingus", "Chungus", "Fingus"]
templatesy = [
    "MeAlsoMe", "ItsRetarded", "Headache", "ItsTime", "ClassNote", "NutButton",
    "Pills", "Balloon", "Classy", "Cola", "Loud", "Milk", "Finally", "Cliff"
]
rules = {
    'origin': ['(WATCHING)your #funny# #wario#!!', "(PLAYING)#games#", "(STREAMING)#videos#", "(WATCHING)my new friend #nametypes# dab"],
    'funny': ['butt', 'ass', 'asshole', 'voidling oc'],
    'wario': ['poop', 'fart', 'yeet', 'fite'],
    'games': ['Voidling Collecters :3', 'Fite #who.capitalize#!'],
    'who': ['coyyy', 'meeed', 'mimlo', 'queddd', 'boohaloo', 'jimy'],
    'videos': ['https://www.youtube.com/watch?v=I8Wf0u8dTWA', 'https://www.youtube.com/watch?v=doWx1vSG22Y', 'https://www.youtube.com/watch?v=rBhbxVmolTE', 'https://www.youtube.com/watch?v=yRUhxFOf_6k', 'https://www.youtube.com/watch?v=lZP41xZ8sjM', 'https://www.youtube.com/watch?v=tw8zVld9OIA', 'https://www.youtube.com/watch?v=oquojYZUL7U', 'https://www.youtube.com/watch?v=F5Vp31IKlik', 'https://www.youtube.com/watch?v=F0htFTcXlCg', 'https://www.youtube.com/watch?v=AFGneaOt9bM'],
    'c': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'],
    'nametypes': ['#c##c##c##c#', '#c##c##c# the #BOIS# Stan#c##c##c#', '#BOIS#SuperFan#c##c##c##c#'],
    'BOIS': ['Meeed', 'Mimlo', 'Coyoboyo', 'DankyBoi', 'Shmlorp', 'Fruccus', 'Brappus', 'Jimy', 'Grantlogan', 'WSB', 'Mario', 'Wario', 'Spongebob', 'Chutnus']
}
p = subprocess.Popen(["python", "server.py"])
grammar = tracery.Grammar(rules)
grammar.add_modifiers(base_english)
bot = commands.Bot(command_prefix='f!')

def genString(length):
	return ''.join(random.choice(string.ascii_letters) for i in range(length))

def comb(l):
     yield from itertools.product(*([l] * 3))

@bot.event
async def on_ready():
    print("I AM ALIVE")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    with open("corpus.txt", "a+") as f:
            f.write(message.content + " ")
    with open("corpus.txt") as f:
        text = f.read()
    text_model = markovify.Text(text, state_size=statesize, well_formed=False)
    text_model = text_model.compile()
    if message.channel.id == 836649499089698816:
        changel = bot.get_channel(836649499089698816)
        await changel.send(str(text_model.make_short_sentence(random.randint(50, 280))))
    if message.content.lower().startswith("buttbot") == True:
        chanle = bot.get_channel(message.channel.id)
        but = message.content.split()
        try:
            seed = but[random.randint(1, len(but) - 1)]
            await chanle.send(' '.join(str(text_model.make_sentence_with_start(seed)).split()[0:random.randint(5, 15)]))
        except:
            await chanle.send(str(text_model.make_short_sentence(random.randint(50, 280))))
    await bot.process_commands(message)

@bot.command()
async def combs(ctx, str):
    for i in comb(str):
        await ctx.send(str(i))

@bot.command()
async def scratch(ctx, user):
  url = f'https://api.scratch.mit.edu/users/{user}'
  print(url)
  r = requests.get(url)
  jsony = json.loads(r.text)
  fart = jsony["profile"]
  bio = fart["bio"]
  status = fart["status"]
  avatar = fart["images"]["90x90"]
  avatar = avatar.replace("png", "gif")
  if bio == "":
    bio = "[Blank]"
  if status == "":
    status = "[Blank]"
  try:
    embed=discord.Embed(color=0xff7f00)
    embed.set_author(name=f'{user}', url=f'https://scratch.mit.edu/users/{user}', icon_url=avatar)
    embed.add_field(name="About me", value=bio, inline=False)
    embed.add_field(name="What I'm working on", value=status, inline=False)
    await ctx.send(embed=embed)
  except Exception as e:
    await ctx.send('Free Error: ' + str(e))

@bot.command()
async def tracery(ctx):
	await ctx.send(grammar.flatten("#origin#"))
@bot.command()
async def updoot(ctx, id):
  massage = await ctx.fetch_message(id)
  await massage.add_reaction('<:updoot:763716527203549194>')
  await ctx.send('Updooted!')
@bot.command()
async def react(ctx, emoji, id):
  massage = await ctx.fetch_message(id)
  await massage.add_reaction(emoji)
  await ctx.send('i did it B O I')
@bot.command()
async def u8(ctx, data):
  filename = 'u8_' + genString(5)
  if ctx.message.attachments:
      r = requests.get(ctx.message.attachments[0].url)
      os.system('echo ' + r.text + ' | ffmpeg -f u8 -ar 8000 -ac 1 -i - ' + filename + '.wav')
  elif data.startswith('http://') or data.startswith('https://'):
      #r = requests.get(data)
      os.system('ffmpeg -f u8 -ar 8000 -ac 1 -i ' + data + ' ' + filename + '.wav')
  else:
      await ctx.send('Bruh There No TEXT Or URL')
  try:
      await ctx.send(file=discord.File(filename + '.wav'))
  except Exception as e:
      await ctx.send('Fail: ```' + str(e) + '```')
  #await ctx.send(file=discord.File(filename + '.wav'))
@bot.command()
async def tou8(ctx, data):
  filename = 'u8_' + genString(5)
  if ctx.message.attachments:
      r = requests.get(ctx.message.attachments[0].url)
      os.system('ffmpeg -i ' + ctx.message.attachments[0].url + ' -f u8 -ar 8000 -ac 1 ' + filename + '.raw')
  elif data.startswith('http://') or data.startswith('https://'):
      os.system('ffmpeg -i ' + data + ' -f u8 -ar 8000 -ac 1 ' + filename + '.raw')
  else:
      await ctx.send('Bruh There No ATTACHMENT Or URL')
  try:
      await ctx.send(file=discord.File(filename + '.raw'))
  except Exception as e:
      await ctx.send('Fail: ```' + str(e) + '```')
bot.run(token)
