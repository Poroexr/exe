import contextlib
from io import StringIO
from nextcord.ext.commands import Cog
from nextcord import *
from nextcord import slash_command as jeanne_slash
from assets.needed import bot_owner
from assets.errormsgs import owner_only
from os import execv
from sys import executable, argv
from sqlite3 import connect

db=connect("database.db")


format = "%a, %d %b %Y | %H:%M:%S %ZGMT"

def restart_bot():
  execv(executable, ['python'] + argv)

class slashowner(Cog):
    def __init__(self, bot):
        self.bot = bot


    @jeanne_slash(description="Changes the bot's play activity")
    async def activity(self, interaction : Interaction, activitytype=SlashOption(description="Choose an activity type", choices=['listen', 'play'], required=True), activity=SlashOption(description="What is the new activity")):
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                await interaction.response.send_message(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            if interaction.user==self.bot.get_user(bot_owner):        
                if activitytype=="listen":
                    await self.bot.change_presence(activity=Activity(type=ActivityType.listening, name=activity))
                    await interaction.response.send_message(f"Bot's activity changed to `listening to {activity}`")            
                elif activitytype=="play":
                    await self.bot.change_presence(activity=Game(name=activity))
                    await interaction.response.send_message(f"Bot's activity changed to `playing {activity}`")            
            else:
                await interaction.response.send_message(embed=owner_only)                
            

    @jeanne_slash(description="Get mutuals of a user")
    async def mutuals(self, interaction : Interaction, user_id=SlashOption(description="Which user?", required=None)):
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                await interaction.response.send_message(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            if interaction.user==self.bot.get_user(bot_owner):
                
                if user_id == None:
                    user_id=self.bot.user.id

                user=await self.bot.fetch_user(user_id)

                mutuals = f"______\nName: {user}\nMutuals: {len(user.mutual_guilds)}\nServers: {user.mutual_guilds}\n______"
                print(mutuals)
                await interaction.response.send_message(f"`Check console log for {user.name}'s mutuals`", ephemeral=True)
            else:
                await interaction.response.send_message(embed=owner_only)        

    @jeanne_slash(description="Finds a user")
    async def finduser(self, interaction: Interaction, user_id=SlashOption(description="Which user?")):
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                await interaction.response.send_message(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            if interaction.user==self.bot.get_user(bot_owner):
                user = await self.bot.fetch_user(user_id)
                if user.bot == True:
                    botr = ":o:"
                else:
                    botr = ":x:"
                fuser = Embed(title="User Found", color=0xccff33)
                fuser.add_field(name="User Information",
                                value=f"**>** **Name:** {user}\n**>** **ID:** {user.id}\n**>** **Creation Date:** {user.created_at.strftime(format)}\n**>** **Mutuals:** {len(user.mutual_guilds)}\n**>** **Is Bot?:** {botr}",
                                inline=True)
                fuser.set_image(url=user.display_avatar)
                await interaction.response.send_message(embed=fuser)
            else:
                await interaction.response.send_message(embed=owner_only)             

    @jeanne_slash(description="Restart me to be updated")
    async def update(self, interaction:Interaction):
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                await interaction.response.send_message(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            if interaction.user == self.bot.get_user(bot_owner):
                await interaction.response.send_message(f"YAY! NEW UPDATE!")
                restart_bot()
            else:
                await interaction.response.send_message(embed=owner_only)
    
    @jeanne_slash(description="Botban a user from using the bot")
    async def botban(self, interaction: Interaction, user_id=SlashOption(description="Which user?"), reason = SlashOption(description="Add a reason")):
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                await interaction.response.send_message(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            if interaction.user == self.bot.get_user(bot_owner):
                user=await self.bot.fetch_user(user_id)
                channel = self.bot.get_channel(928962613939949618)
                cur = db.execute("INSERT OR IGNORE INTO botbannedData (user_id, reason) VALUES (?,?)", (user.id, reason))

                if cur.rowcount==0:
                    db.execute(
                        f"UPDATE botbannedData SET reason = {reason} WHERE user_id = {user.id}")
                db.commit()
                    
                cur1=db.cursor()
                cur2=db.cursor()
                cur1.execute(
                        f"SELECT * FROM serverxpData WHERE user_id = {user.id}")
                result1=cur1.fetchall()
                cur2.execute(f"SELECT * FROM globalxpData WHERE user_id = {user.id}")
                result2=cur2.fetchone()

                if result1 == None:
                    pass

                else:
                    cur1.execute(
                            f"SELECT user_id FROM serverxpData")
                    result1 = cur1.fetchall()
                    cur1.execute(f"DELETE FROM serverxpData WHERE user_id = {user.id}")
                    
                if result2 == None:
                    pass

                else:
                    cur2.execute(
                            f"SELECT * FROM globalxpData WHERE user_id = {user.id}")
                    result2 = cur1.fetchone()
                    cur2.execute(
                            f"DELETE FROM globalxpData WHERE user_id = {user.id}")
                    botbanned=Embed(title="User has been botbanned!", description="They will no longer use Jeanne, permanently!")
                    botbanned.add_field(name="User",
                                value=f"**>** **Name:** {user}\n**>** **ID:** {user.id}",
                                inline=True)
                    botbanned.add_field(name="Reason of ban",
                                        value=reason,
                                        inline=False)
                    botbanned.set_footer(text="Due to this user botbanned, any data except warnings are immediatley deleted from the database! They will have no chance of appealing their botban.")
                    botbanned.set_thumbnail(url=user.avatar)
                    await channel.send(embed=botbanned)
                    db.commit()

    @jeanne_slash(description="Evaluates a code", guild_ids=[809862945211285555])
    async def evaluate(self, interaction: Interaction):
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                await interaction.response.send_message(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            if interaction.user == self.bot.get_user(bot_owner):
                await interaction.response.defer()
                await interaction.followup.send('Insert your code')
                def check(m):
                    return m.author == interaction.user and m.content

                code = await self.bot.wait_for('message', check=check)


                str_obj = StringIO()
                try:
                    with contextlib.redirect_stdout(str_obj):
                        exec(code.content)
                except Exception as e:
                    embed = Embed(title="Evaluation failed :negative_squared_cross_mark:\nResults:",
                                  description=f"```{e.__class__.__name__}: {e}```", color=0xFF0000)
                    embed.set_footer(
                        text=f"Compiled in {round(self.bot.latency * 1000)}ms")
                    return await interaction.followup.send(embed=embed)
                embed1 = Embed(title="Evaluation suscessful! :white_check_mark: \nResults:",
                               description=f'```{str_obj.getvalue()}```', color=0x008000)
                embed1.set_footer(
                        text=f"Compiled in {round(self.bot.latency * 1000)}ms")
                await interaction.followup.send(embed=embed1)

def setup(bot):
    bot.add_cog(slashowner(bot))
