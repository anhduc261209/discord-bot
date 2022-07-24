import discord
from discord.ext import commands
import requests
import json
import random

class Entertainment(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(help="Ping!")
	async def ping(self, ctx):
	    await ctx.send('Pong!')

	@commands.command()
	async def whoisowner(self, ctx):
	    await ctx.send("Anh Duc")

	@commands.command(help="Flips a coin!")
	async def flip(self, ctx):
	    await ctx.send(random.choice(['heads', 'tails']))

	@commands.command(help="Rolls a dice!")
	async def roll(self, ctx):
	    await ctx.send(random.randint(1, 6))

	@commands.command(help = "Play rock paper scissors!")
	async def rockpaperscissors(self, ctx, arg):
	    async with ctx.typing():
	        bot_choice = random.choice(['rock', 'paper', 'scissors'])
	        user_choice = arg
	    await ctx.send(f"I choose {bot_choice}.\nYou choose {user_choice}.")
	    if user_choice == bot_choice:
	        await ctx.send('It\'s a tie!')
	    elif user_choice == 'rock':
	        if bot_choice == 'paper':
	            await ctx.send('I win!')
	        else:
	            await ctx.send('You win!')
	    elif user_choice == 'paper':
	        if bot_choice == 'scissors':
	            await ctx.send('I win!')
	        else:
	            await ctx.send('You win!')
	    elif user_choice == 'scissors':
	        if bot_choice == 'rock':
	            await ctx.send('I win!')
	        else:
	            await ctx.send('You win!')

	@commands.command(help = "Tell a joke!")
	async def joke(self, ctx, category = None):
	    if category == None:
	        await ctx.reply('Please specify a category: Programming, Miscellaneous, Dark, Pun, Spooky, Christmas.\nUse "Any" for any categories')
	    else:
	        if category not in ["Programming", "Miscellaneous", "Dark", "Pun", "Spooky", "Christmas", "Any"]:
	            await ctx.reply("Hmm.. Please type the category again")
	        else:
	            async with ctx.typing():
	                response = requests.get(f"https://v2.jokeapi.dev/joke/{category}?format=json")
	                response = response.json()
	            try: # single joke
	                await ctx.reply(response["joke"])
	            except: # two-part joke
	                await ctx.reply(response["setup"])
	                await ctx.reply(response["delivery"])

	@commands.command(help = "Tell a dad joke!")
	async def dadjoke(self, ctx):
	    async with ctx.typing():
	        url = "https://dad-jokes.p.rapidapi.com/random/joke"

	        headers = {
	            "X-RapidAPI-Key": "d3c5dbe6ccmsh37d38169379cda7p1d66a8jsn4f5b8d97ed41",
	            "X-RapidAPI-Host": "dad-jokes.p.rapidapi.com"
	        }

	        response = requests.request("GET", url, headers=headers)

	        response = response.json()

	    await ctx.reply(response["body"][0]["setup"] + "\n" + response["body"][0]["punchline"])

	@commands.command(help = "Tell a mom joke!")
	async def momjoke(self, ctx):
	    async with ctx.typing():
	        url = "https://yo-mama.p.rapidapi.com/random/joke"

	        headers = {
	            "X-RapidAPI-Key": "d3c5dbe6ccmsh37d38169379cda7p1d66a8jsn4f5b8d97ed41",
	            "X-RapidAPI-Host": "yo-mama.p.rapidapi.com"
	        }

	        response = requests.request("GET", url, headers=headers)

	        response = response.json()

	    await ctx.reply(response["joke"])