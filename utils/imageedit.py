import discord
from discord.ext import commands

import requests
from wand.image import Image

class ImageEdit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.attachment = None
        self.file_name = "image_to_edit.jpg"

    @commands.command(name = "saveimg")
    async def saveimg(self, ctx):
        async with ctx.typing():
            if len(ctx.message.attachments) > 0:
                self.attachment = ctx.message.attachments[0];
            else:
                await ctx.reply("No images included!")
                return
            img_data = requests.get(self.attachment.url).content
            with open(self.file_name, 'wb') as handler:
                handler.write(img_data)
        await ctx.send("Download complete!")

    @commands.command(name="editimg")
    async def _edit(self, ctx, option = ""):
        if option == "grayscale":
            with Image(filename=self.file_name) as img:
                img.transform_colorspace("gray")
                img.save(filename=self.file_name)
        elif option == "implode":
            with Image(filename=self.file_name) as img:
                img.implode(0.7, "blend")
                img.save(filename=self.file_name)
        elif option == "swirl":
            with Image(filename=self.file_name) as img:
                img.swirl(100, "blend")
                img.save(filename=self.file_name)
        else:
            await ctx.send("Please provide an option: grayscale, implode, swirl")
            return
        await ctx.send(file = discord.File(self.file_name))