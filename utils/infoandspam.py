import discord
from discord.ext import commands

class SpamAndInfo(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(help = "Returns information about the server and user!")
	async def info(self, ctx):
	    await ctx.reply(f"Server: {ctx.guild}\nUser: {ctx.author}\nMessage ID: {ctx.message.id}")

	@commands.command(help = "Get info about a user")
	async def getinfo(self, ctx, member : discord.Member):
	    async with ctx.typing():
	        memberroles = []
	        for role in member.roles:
	            memberroles.append(role.name)
	        roles = ", ".join(memberroles)
	    await ctx.reply(f"Username: {member.display_name}#{member.discriminator}\nServer: {member.guild.name}\nJoined on: {member.joined_at.month}/{member.joined_at.day}/{member.joined_at.year}\nRoles: {roles}")

	@commands.command()
	async def allmembers(self, ctx):
	    # Send a list of members
	    async with ctx.typing():
	        members = ctx.guild.members
	        memberlist = []
	        for member in members:
	            memberlist.append(f"{member.display_name}#{member.discriminator}")
	    await ctx.reply("\n".join(memberlist))

	@commands.command()
	async def spam(self, ctx, times = 5, *, message : str):
	    for _ in range(times):
	        await ctx.send(message)

	@commands.command()
	async def spamping(self, ctx, member : discord.Member, times = 5, *, message : str = ""):
	    for _ in range(times):
	        await ctx.send(f"{member.mention} {message}")