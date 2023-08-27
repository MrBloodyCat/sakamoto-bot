from disnake.ext import commands


class Ready(commands.Cog):

    @commands.Cog.listener()
    async def on_ready(self):
        print('Client is starting!')


def setup(client):
    client.add_cog(Ready(client))
