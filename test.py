import datetime
import os

from api.untis_api import UnitsApi
from api.ploty_api import PlotyApi
from api.timetable_generator import TimetableGenerator
from api.models.theme_data import ThemeData
from api.models.color import Color
import time
from datetime import timedelta
import discord
from dotenv import load_dotenv
import locale
import datetime

load_dotenv()
locale.setlocale(locale.LC_TIME,os.getenv("LOCALE"))
untis = UnitsApi(server=os.getenv("SERVER"),
                 username=os.getenv("UUSERNAME"),
                 password=os.getenv("PASSWORD"),
                 school=os.getenv("SCHOOL"),
                 useragent=os.getenv("USERAGENT")
                 )
plotly = PlotyApi(themeData=ThemeData(
            cancelled_color=Color(251, 72, 72),
            irregular_color=Color(189, 163, 199),
            none_color=Color(243, 184, 98),
            first_column_color=Color(199, 131, 32)
        ))
generator = TimetableGenerator(units=untis,plotly=plotly)

botInstance = discord.Bot()


@botInstance.slash_command(name="update", guild_ids=[930058237942824960], description='Creates a timetable')
async def update(ctx):
    file = discord.File('images/timetable.png', filename="image.png")
    embed = discord.Embed(
        title=f"Timetable",
        timestamp=datetime.datetime.now(),
        color=0x098D3A
    )
    embed.set_image(url="attachment://image.png")
    await ctx.respond(embed=embed, file=file)



@botInstance.slash_command(name="find", guild_ids=[930058237942824960])
async def finding(ctx):
    if value == True:
        file = discord.File('images/timetable.png',filename="image.png")
        embed = discord.Embed(
            title=f"Timetable",
            timestamp=datetime.now(),
            colour=0x098D3A
        )
        embed.set_image(url="attachment://image.png")
        await ctx.respond(embed=embed, file=file)
    else:
        print(value)
        await ctx.respond("Es wurden keine Änderungen gefunden...")


def start():
    botInstance.run(os.getenv("TOKEN"))


if __name__ == "__main__":
    untis.login()
    generator.generate(classId=1144)
    start()
