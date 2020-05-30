from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageOps
import discord, os, aiohttp
from io import BytesIO
import textwrap
import base64
from config.Permissions import *
from modules.db.db_management import get_welcome_channel, get_img, \
    edit_settings_img, edit_settings_img_text, get_img_text


'''
MIT License

Copyright (c) 2018-2019 https://github.com/hibikidesu/

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''


class IMGWelcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def __is_enabled(self, guild: int):
        if int(await get_img(guild)) == 1:
            return True
        else:
            return False

    @commands.group()
    @commands.has_permissions(administrator=True)
    async def imgwelcome(self, ctx):
        # Base command
        if ctx.invoked_subcommand is None:
            return await ctx.send_help(ctx.command)

    @imgwelcome.command(name="toggle")
    async def imgwelcome_toggle(self, ctx):
        """Toggle on/off the imgwelcomer"""
        toggle = int(await get_img(ctx.guild.id))
        if 0 == toggle:
            await edit_settings_img(ctx.guild.id, 1)
            await ctx.send("Welcome image is now enabled")
        else:
            await edit_settings_img(ctx.guild.id, 0)
            await ctx.send("Welcome image is now disabled")

    @imgwelcome.command(name="img")
    async def imgwelcome_img(self, ctx):
        """Set the image"""
        if not await self.__is_enabled(ctx.guild.id):
            return await ctx.send("Enable imgwelcoming with n!imgwelcome toggle")

        if len(ctx.message.attachments) == 0:

            await ctx.send("Send an image or type anything without sending an image to reset back to default.")

            def check(m):
                return m.author == ctx.message.author and m.channel == ctx.message.channel

            try:
                msg = await self.bot.wait_for('message', check=check, timeout=20)
            except:
                return await ctx.send("Timed out.")

        else:
            msg = ctx.message

        if len(msg.attachments) >= 1:
            attachment = str(msg.attachments[0].url).rpartition(".")[2]
            if attachment.lower() not in ["png", "jpg", "jpeg", "gif"]:
                return await ctx.send("Not a valid image type <:bakaa:432914537608380419>")
            if os.path.exists(f"data/imgwelcome/{ctx.guild.id}.png"):
                os.remove(f"data/imgwelcome/{ctx.guild.id}.png")
            try:
                async with aiohttp.ClientSession() as cs:
                    async with cs.get(msg.attachments[0].url) as r:
                        imgdata = await r.read()
                img = Image.open(BytesIO(imgdata)).convert("RGBA").resize((500, 150))
                bg = Image.new("RGBA", (500, 150), (0, 0, 0, 0))
                bg.alpha_composite(img, (0, 0))
                bg.save(f"data/imgwelcome/{ctx.guild.id}.png")
                await ctx.send("Set image!")
            except Exception as e:
                await ctx.send("Failed to set image... `{}`".format(e))
        else:
            if os.path.exists(f"data/imgwelcome/{ctx.guild.id}.png"):
                os.remove(f"data/imgwelcome/{ctx.guild.id}.png")
            await ctx.send("Reset Image.")

    @imgwelcome.command(name="text")
    async def imgwelcome_text(self, ctx, *, text: str):
        """Change the welcome text,
            user = the user's name
            server = the server's name
        Example:
            n!imgwelcome text Welcome user to server!
        """

        if not await self.__is_enabled(ctx.guild.id):
            return await ctx.send("Enable imgwelcoming with n!imgwelcome toggle")

        text = (base64.b64encode(text.encode("utf8"))).decode("utf8")
        await edit_settings_img_text(ctx.guild.id, text)
        await ctx.send("Updated text!")

    def _circle_border(self, circle_img_size: tuple):
        border_size = []
        for i in range(len(circle_img_size)):
            border_size.append(circle_img_size[0] + 8)
        return tuple(border_size)

    async def setimage(self, member):
        try:
            img = Image.open(f"data/imgwelcome/{member.guild.id}.png").convert("RGBA").resize((500, 150))
            bg = Image.new("RGBA", (500, 150), (0, 0, 0, 0))
            bg.alpha_composite(img, (0, 0))
            bg.save(f"data/imgwelcome/{member.guild.id}.png")
            await member.send("Set image!")
        except Exception as e:
            await member.send("Failed to set image... `{}`".format(e))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        # await self.setimage(member)
        # gets the channel, member and creates the image and sends it to the channel
        # channel = self.bot.get_channel(int(594993305914179597))
        channel_id = await get_welcome_channel(member.guild.id)
        channel = member.guild.get_channel(channel_id)
        if not channel:
            return
        await channel.trigger_typing()

        if os.path.exists(f"data/imgwelcome/{guild.id}.png"):
            background = Image.open(f"data/imgwelcome/{guild.id}.png").convert("RGBA")
        else:
            background = Image.open("data/imgwelcome/transparent.png")

        async with aiohttp.ClientSession() as cs:
            async with cs.get(str(member.avatar_url_as(format="png"))) as res:
                imgdata = await res.read()

        welcome_picture = ImageOps.fit(background, (500, 150), centering=(0.5, 0.5))
        welcome_picture.paste(background)
        welcome_picture = welcome_picture.resize((500, 150), Image.NEAREST)

        profile_area = Image.new("L", (512, 512), 0)
        draw = ImageDraw.Draw(profile_area)
        draw.ellipse(((0, 0), (512, 512)), fill=255)
        profile_area = profile_area.resize((128, 128), Image.ANTIALIAS)
        profile_picture = Image.open(BytesIO(imgdata))
        profile_area_output = ImageOps.fit(profile_picture, (128, 128), centering=(0, 0))
        profile_area_output.putalpha(profile_area)

        mask = Image.new('L', (512, 512), 0)
        draw_thumb = ImageDraw.Draw(mask)
        draw_thumb.ellipse((0, 0) + (512, 512), fill=255, outline=0)
        circle = Image.new("RGBA", (512, 512))
        draw_circle = ImageDraw.Draw(circle)
        draw_circle.ellipse([0, 0, 512, 512], fill=(255, 255, 255, 180), outline=(255, 255, 255, 250))
        circle_border_size = self._circle_border((128, 128))
        circle = circle.resize(circle_border_size, Image.ANTIALIAS)
        circle_mask = mask.resize(circle_border_size, Image.ANTIALIAS)
        circle_pos = (7 + int((136 - circle_border_size[0]) / 2))
        border_pos = (11 + int((136 - circle_border_size[0]) / 2))
        drawtwo = ImageDraw.Draw(welcome_picture)
        welcome_picture.paste(circle, (circle_pos, circle_pos), circle_mask)
        welcome_picture.paste(profile_area_output, (border_pos, border_pos), profile_area_output)

        uname = (str(member.name) + "#" + str(member.discriminator))

        def _outline(original_position: tuple, text: str, pixel_displacement: int, font, textoutline):
            op = original_position
            pd = pixel_displacement

            left = (op[0] - pd, op[1])
            right = (op[0] + pd, op[1])
            up = (op[0], op[1] - pd)
            down = (op[0], op[1] + pd)

            drawtwo.text(left, text, font=font, fill=(textoutline))
            drawtwo.text(right, text, font=font, fill=(textoutline))
            drawtwo.text(up, text, font=font, fill=(textoutline))
            drawtwo.text(down, text, font=font, fill=(textoutline))

            drawtwo.text(op, text, font=font, fill=(textoutline))

        welcome_font = ImageFont.truetype("data/fonts/UniSansHeavy.otf", 50)

        _outline((150, 16), "Welcome", 1, welcome_font, (0, 0, 0, 255))
        drawtwo.text((150, 16), "Welcome", font=welcome_font, fill=(255, 255, 255, 230))
        name_font = ImageFont.truetype("data/fonts/UniSansHeavy.otf", 30)
        name_font_medium = ImageFont.truetype("data/fonts/UniSansHeavy.otf", 22)
        name_font_small = ImageFont.truetype("data/fonts/UniSansHeavy.otf", 18)
        name_font_smallest = ImageFont.truetype("data/fonts/UniSansHeavy.otf", 12)
        server_font = ImageFont.truetype("data/fonts/UniSansHeavy.otf", 22)

        if len(uname) <= 17:
            _outline((152, 63), uname, 1, name_font, (0, 0, 0, 255))
            drawtwo.text((152, 63), uname, font=name_font, fill=(255, 255, 255, 230))

        if len(uname) > 17:
            if len(uname) <= 23:
                _outline((152, 66), uname, 1, name_font_medium, (0, 0, 0, 255))
                drawtwo.text((152, 66), uname, font=name_font_medium, fill=(255, 255, 255, 230))

        if len(uname) >= 24:
            if len(uname) <= 32:
                _outline((152, 70), uname, 1, name_font_small, (0, 0, 0, 255))
                drawtwo.text((152, 70), uname, font=name_font_small, fill=(255, 255, 255, 230))

        if len(uname) >= 33:
            drawtwo.text((152, 73), uname, 1, name_font_smallest, (0, 0, 0, 255))
            drawtwo.text((152, 73), uname, font=name_font_smallest, fill=(255, 255, 255, 230))

        server_text = "\n".join(textwrap.wrap(f"Welcome to {guild.name}!", 25))
        _outline((152, 100), server_text, 1, server_font, (0, 0, 0, 255))
        drawtwo.text((152, 100), server_text, font=server_font, fill=(255, 255, 255, 230))

        welcome_picture.save("data/welcome.png")

        try:
            content = ((base64.b64decode(str(await get_img_text(guild.id)).encode("utf8"))).decode("utf8"))\
                .replace("user", member.mention)\
                .replace("server", guild.name)
        except:
            content = "Welcome {} to {}!".format(member.name, guild.name)

        file = discord.File("data/welcome.png", filename="welcome.png")
        await channel.send(file=file, content=content)


def setup(bot):
    bot.add_cog(IMGWelcome(bot))
