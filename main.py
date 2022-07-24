import discord
from discord.ext import commands
import os
import random
import youtube_dl
import requests
import json
import pafy
import asyncio

from utils.music import Player 
from utils.moderator import Mod
from utils.entertainment import Entertainment
from utils.infoandspam import SpamAndInfo
from utils.imagesearch import ImageSearch
from utils.imageedit import ImageEdit
 
intents = discord.Intents.all()
client = commands.Bot(command_prefix="ad@", intents = intents, status = discord.Status.dnd, activity = discord.Game(name = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"))
client.remove_command('help') # To override the default help command

@client.event
async def on_ready():
    print("Ready!")

@client.event
async def on_member_join(member):
    async with ctx.typing():
        s = discord.utils.get(member.guild.text_channels, name="general")
    await s.send(f"{member.display_name} just slid into the server.\n@everyone welcome {member.mention}!!! 🎉🎉🎉")

async def setup():
    await client.wait_until_ready()
    client.add_cog(Player(client))
    client.add_cog(Mod(client))
    client.add_cog(Entertainment(client))
    client.add_cog(SpamAndInfo(client))
    client.add_cog(ImageEdit(client))
    client.add_cog(ImageSearch(client))

client.loop.create_task(setup())
client.run('NO TOKEN 4 U')
