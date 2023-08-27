from disnake.ext import commands
from datetime import datetime


class Message(commands.Cog):
    def __init__(self, client):
        self.lvl = client.lvl
        self.db = client.db

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.guild is None:return
        if msg.author.bot:return

        data_guild = await self.db.find_one(collection='setup', guild_id=msg.guild.id, component='level_chat')
        if not data_guild['enable']:return

        data_member = await self.db.find_one(collection='members', guild_id=msg.guild.id, component=str(msg.author.id))

        timestamp_seconds = int(datetime.now().timestamp())
        if timestamp_seconds - data_member['last_chat_data'] < data_guild['cooldown']:return

        data_member['exp'] = self.lvl.add_exp(exp=data_member['exp'], give_exp=data_guild['give_exp'])
        data_member['last_chat_data'] = timestamp_seconds
        await self.db.update_one(collection='members', guild_id=msg.guild.id, key=str(msg.author.id), value=data_member)


def setup(client):
    client.add_cog(Message(client))
