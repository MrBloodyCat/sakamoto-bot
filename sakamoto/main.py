import disnake
import config
import os

from disnake.ext import commands
from modules import language, mongodb, level

intents = disnake.Intents.all()
client = commands.Bot(command_prefix=config.command_prefix,
                      test_guilds=config.test_guilds, intents=intents)
client.lang = language.Language()
client.db = mongodb.Database()
client.lvl = level.Level()

config.directory = 'sakamoto/' if 'ubuntu' in os.getcwd() else config.directory

config.languages_list = list(client.lang.get_languages())

print('Loaded extensions:')
for files in os.listdir(f"{config.directory}cogs"):
    if files.endswith('.py'):
        client.load_extension(f'cogs.{files[:-3]}')
        print('✔', files[:-3])

if __name__ == '__main__':
    print('Starting...')
    client.run(config.bot_token)
