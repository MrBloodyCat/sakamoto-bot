import disnake
from disnake.ext import commands


class Ping(commands.Cog):
    def __init__(self, client):
        self.lang = client.lang
        self.db = client.db

    @commands.slash_command(name='ping', description='Check communication with the client')
    @commands.cooldown(rate=1, per=6)
    async def ping(self, inter: disnake.ApplicationCommandInteraction):
        lang = await self.db.find_one(collection='setup', guild_id=inter.guild.id, component='language')
        await inter.response.send_message(self.lang.get_text(key='ping', language=lang), ephemeral=True)

    @ping.error
    async def on_user_command_error(self, inter: disnake.ApplicationCommandInteraction, error: commands.CommandError):
        lang = await self.db.find_one(collection='setup', guild_id=inter.guild.id, component='language')
        if isinstance(error, commands.CommandOnCooldown):
            await inter.response.send_message(self.lang.get_text(key='ping_error_cooldown', language=lang), ephemeral=True)
        else:
            raise error
        

def setup(client):
    client.add_cog(Ping(client))
