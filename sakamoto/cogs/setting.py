import disnake
from config import languages_list
from disnake.ext import commands


class Setting(commands.Cog):
    def __init__(self, client):
        self.lang = client.lang
        self.db = client.db

    @commands.slash_command(name='setting')
    @commands.has_permissions(administrator=True)
    async def setting(self, inter: disnake.ApplicationCommandInteraction):
        pass


    @setting.sub_command(name='language', description='Change the language of the bot')
    @commands.cooldown(rate=2, per=8)
    async def language(self, inter: disnake.ApplicationCommandInteraction, language: str = commands.Param(choices=languages_list, description='Language selection')):
        lang = await self.db.find_one(
            collection='setup',
            guild_id=inter.guild.id,
            component='language'
        )

        await self.db.update_one(
            collection='setup',
            guild_id=inter.guild.id,
            key='language',
            value=language
        )

        await inter.response.send_message(
            self.lang.get_text(key='language_set',language=lang) % language,
            ephemeral=True
        )


    @setting.sub_command(name='chat-enable', description='Enable the level system in chat')
    @commands.cooldown(rate=2, per=8)
    async def enable(self, inter: disnake.ApplicationCommandInteraction):
        lang = await self.db.find_one(
            collection='setup',
            guild_id=inter.guild.id,
            component='language'
        )

        level_chat = await self.db.find_one(
            collection='setup',
            guild_id=inter.guild.id,
            component='level_chat'
        )

        level_chat['enable'] = False if level_chat['enable'] else True
        await self.db.update_one(
            collection='setup',
            guild_id=inter.guild.id,
            key='level_chat',
            value=level_chat
        )

        message = 'level_system_on' if level_chat['enable'] else 'level_system_off'
        await inter.response.send_message(
            self.lang.get_text(key=message,language=lang),
            ephemeral=True
        )

    @setting.sub_command(name='chat-cd', description='Set the cooldown in chat to gain experience')
    @commands.cooldown(rate=2, per=8)
    async def cd(self, inter: disnake.ApplicationCommandInteraction, cooldown: int = commands.Param(description='cd in chat', ge=0, le=700000)):
        lang = await self.db.find_one(
            collection='setup',
            guild_id=inter.guild.id,
            component='language'
        )
        level_chat = await self.db.find_one(
            collection='setup',
            guild_id=inter.guild.id,
            component='level_chat'
        )

        level_chat['cooldown'] = cooldown
        await self.db.update_one(
            collection='setup',
            guild_id=inter.guild.id,
            key='level_chat',
                                 value=level_chat)

        await inter.response.send_message(
            self.lang.get_text(key='level_system_cd', language=lang)% cooldown,
            ephemeral=True
        )

    @setting.sub_command(name='chat-give_exp', description='Set how much experience the member will be given')
    @commands.cooldown(rate=2, per=8)
    async def give_exp(
            self, inter: disnake.ApplicationCommandInteraction,
                 exp_min: int = commands.Param(description='minimum amount of experience you can get', ge=0, le=700000),
                       exp_max: int = commands.Param(description='maximum amount of experience you can get', ge=0, le=700000)
    ):
        lang = await self.db.find_one(
            collection='setup',
            guild_id=inter.guild.id,
            component='language'
        )

        if exp_min > exp_max:
            await inter.response.send_message(
                self.lang.get_text(key='level_system_give_exp_error', language=lang),
                ephemeral=True
            )
            return

        level_chat = await self.db.find_one(
            collection='setup',
            guild_id=inter.guild.id,
            component='level_chat'
        )

        level_chat['give_exp'] = exp_max if exp_max == exp_min else [exp_min,exp_max+1]
        await self.db.update_one(
            collection='setup',
            guild_id=inter.guild.id,
            key='level_chat',
            value=level_chat)

        message = self.lang.get_text(key='level_system_give_exp', language=lang) % exp_max if type(level_chat['give_exp']) is int else self.lang.get_text(key='level_system_give_exp_list', language=lang)% (exp_min, exp_max)
        await inter.response.send_message(
            message,
            ephemeral=True
        )


    @language.error
    async def on_user_command_error(self, inter: disnake.ApplicationCommandInteraction, error: disnake.ext.commands.CommandError):
        lang = await self.db.find_one(collection='setup', guild_id=inter.guild.id, component='language')
        if isinstance(error, commands.CommandOnCooldown):
            await inter.response.send_message(
                self.lang.get_text(key='language_set_error_cooldown', language=lang),
                ephemeral=True
            )
        else:
            raise error


    @enable.error
    async def on_user_command_error(self, inter: disnake.ApplicationCommandInteraction, error: disnake.ext.commands.CommandError):
        lang = await self.db.find_one(collection='setup', guild_id=inter.guild.id, component='language')
        if isinstance(error, commands.CommandOnCooldown):
            await inter.response.send_message(
                self.lang.get_text(key='level_chat_enable_error_cooldown', language=lang),
                                              ephemeral=True
            )
        else:
            raise error

    @cd.error
    async def on_user_command_error(self, inter: disnake.ApplicationCommandInteraction,
                                    error: disnake.ext.commands.CommandError):
        lang = await self.db.find_one(collection='setup', guild_id=inter.guild.id, component='language')
        if isinstance(error, commands.CommandOnCooldown):
            await inter.response.send_message(
                self.lang.get_text(key='level_system_cd_error_cooldown', language=lang),
                ephemeral=True
            )
        else:
            raise error

    @give_exp.error
    async def on_user_command_error(self, inter: disnake.ApplicationCommandInteraction,
                                    error: disnake.ext.commands.CommandError):
        lang = await self.db.find_one(collection='setup', guild_id=inter.guild.id, component='language')
        if isinstance(error, commands.CommandOnCooldown):
            await inter.response.send_message(
                self.lang.get_text(key='level_system_give_exp_error_cooldown', language=lang),
                ephemeral=True
            )
        else:
            raise error


def setup(client):
    client.add_cog(Setting(client))
