import discord
from discord.ext import commands

import os, shutil
from google_images_download import google_images_download
import random
import requests
from wand.image import Image

#responsible for handling all of the image commands
class ImageSearch(commands.Cog):
    def __init__(self, bot):

        self.bot = bot
        self.download_folder = 'downloads'

        self.keywords = "Spongebob"

        self.response = google_images_download.googleimagesdownload()
        self.arguments = {
            "keywords": self.keywords, 
            "limit":20,
            "size":"medium",
            "no_directory": True
            }

        self.image_names = []
        #get the latest in the folder
        self.update_images()


    @commands.command(name="get", help="Displays random image from the downloads")
    async def get(self, ctx):
        async with ctx.typing():
            img = self.image_names[random.randint(0, len(self.image_names) - 1)]
        await ctx.reply(file=discord.File(img))

    def clear_folder(self):
        for filename in os.listdir(self.download_folder):
            file_path = os.path.join(self.download_folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    def update_images(self):
        self.image_names = []
        #store all the names to the files
        for filename in os.listdir(self.download_folder):
            self.image_names.append(os.path.join(self.download_folder, filename))

    @commands.command(name="lookfor", help="searches for a message on google")
    async def lookfor(self, ctx, *args):
        async with ctx.typing():
            self.clear_folder()

            #fill the folder with new images
            self.arguments['keywords'] = " ".join(args)
            self.response.download(self.arguments)

            self.update_images()
        await ctx.reply("Downloaded images")

    @commands.command(name="delete", help="delete all files in folder downloads")
    async def delete(self, ctx, *args):
        self.clear_folder()

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
    