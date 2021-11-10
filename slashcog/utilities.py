import discord
import aiohttp
from discord.ext import commands
from discord_slash import cog_ext, SlashContext


class utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(description="Get weather information on a city")
    async def weather(self, ctx:SlashContext, city):
        city = city
        urlil = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=f8e10f057f4c41611cc2075f28cd3f2d&units=metric'
        async with aiohttp.ClientSession() as session:
            async with session.get(urlil) as r:
                if r.status == 200:
                    js = await r.json()
                    tempp = js['main']['temp']
                    desc = js['weather'][0]["description"]
                    count = js['sys']['country']
                    hum = js['main']['humidity']
                    pres = js['wind']['speed']
                    embed = discord.Embed(
                        title=f'⛅ Weather details of {city} ⛅', description=f':earth_africa: Country: {count}', colour=0x00FFFF)
                    embed.add_field(name=':thermometer: Temperature:',
                                    value=f'{tempp}° Celsius', inline=True)
                    embed.add_field(name=':newspaper: Description:',
                                    value=f'{desc}', inline=True)
                    embed.add_field(name=":droplet: Humidity:",
                                    value=f'{hum}', inline=True)
                    embed.add_field(name=":cloud: Pressure:",
                                    value=f'{pres} Pa', inline=True)
                    await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(utilities(bot))
