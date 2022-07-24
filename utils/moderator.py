import discord
import asyncio
from discord.ext import commands

class Mod(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(help="Clear a number of recent message, default is 5")
	async def clear(self, ctx, amount=5):
		user_permissions = ctx.message.author.guild_permissions
		if user_permissions.manage_messages and user_permissions.read_message_history:
			await ctx.channel.purge(limit = amount+1)
		else:
			await ctx.reply("You do not have permission to do this")

	@commands.command()
	async def changenickname(self, ctx, member: discord.Member, new_nickname, reason=None):
		user_permissions = ctx.message.author.guild_permissions
		if user_permissions.manage_nicknames:
			await member.edit(nick = new_nickname, reason = reason)
		else:
			await ctx.reply("You do not have permission to do this")

	@commands.command()
	async def kick(self, ctx, member: discord.Member, *, reason=None):
		user_permissions = ctx.message.author.guild_permissions
		if user_permissions.kick_members:
			await ctx.send(f"Kicked {member.mention}")
			await member.kick(reason = reason)
		else:
			await ctx.reply("You do not have permission to do this")


	@commands.command()
	async def ban(self, ctx, member: discord.Member, *, reason=None):
		user_permissions = ctx.message.author.guild_permissions
		if user_permissions.ban_members:
			await ctx.send(f"Banned {member.mention}")
			await member.ban(reason = reason)
		else:
			await ctx.reply("You do not have permission to do this")

	@commands.command()
	async def unban(self, ctx, member : discord.Member, *, reason = None):
		user_permissions = ctx.message.author.guild_permissions
		if user_permissions.ban_members:
			banned_users = await ctx.guild.bans()
			member_name, member_discriminator = member.split('#')

			for ban_entry in banned_users:
				user = ban_entry.user

				if (user.name, user.discriminator) == (member_name, member_discriminator):
					await ctx.guild.unban(user)
					await ctx.send(f"Unbanned {user.mention}")
					return
		else:
			await ctx.reply("You do not have permission to do this")

	@commands.command()
	async def mute(self, ctx, member: discord.Member, duration : int, *, unit : str):
		user_permissions = ctx.message.author.guild_permissions
		if user_permissions.mute_members:
			role = discord.utils.get(ctx.message.guild.roles, name="Muted")
			await member.add_roles(role)
			await ctx.send(f"Muted {member.mention}")
			if unit == "s": wait = 1 * duration
			elif unit == "m": wait = 60 * duration
			elif unit == "h": wait = 3600 * duration
			else: pass
			await asyncio.sleep(wait)
			await member.remove_roles(role)
		else:
			await ctx.reply("You do not have permission to do this")
