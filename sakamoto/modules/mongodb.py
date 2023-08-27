from motor.motor_asyncio import AsyncIOMotorClient
from config import mongodb_key, default_setup_guild, default_setup_user


def setup_search(func):
    async def wrapper(self, *args, **kwargs):
        if kwargs['collection'] == 'setup':
            result = await self.discord[kwargs['collection']].find_one({'guild_id': kwargs['guild_id']})
            if result is None:
                new_setup = default_setup_guild.copy()
                new_setup['guild_id'] = kwargs['guild_id']

                await self.discord[kwargs['collection']].insert_one(new_setup)

            elif len(result)-1 != len(default_setup_guild):
                new_setup = default_setup_guild.copy()
                for component in default_setup_guild:
                    new_setup[component] = result[component] if component in result else new_setup[component]

                await self.discord[kwargs['collection']].replace_one({'guild_id': kwargs['guild_id']}, new_setup)

        return await func(self, *args, **kwargs)
    return wrapper

def members_search(func):
    async def wrapper(self, *args, **kwargs):
        if kwargs['collection'] == 'members':
            result = await self.discord[kwargs['collection']].find_one({'guild_id': kwargs['guild_id']})
            if result is None:
                await self.discord[kwargs['collection']].insert_one({'guild_id': kwargs['guild_id']})

            if kwargs['component']:
                document = await self.discord[kwargs['collection']].find_one({'guild_id': kwargs['guild_id']}, {'_id': 0,kwargs['component']: 1})
                if not document:
                    await self.discord[kwargs['collection']].update_one({'guild_id': kwargs['guild_id']}, {'$set': {kwargs['component']: default_setup_user}})

                elif len(document[kwargs['component']]) != len(default_setup_user):
                    new_setup = default_setup_user.copy()
                    for component in default_setup_user:
                        new_setup[component] = document[kwargs['component']][component] if component in document[kwargs['component']] else new_setup[component]

                    await self.discord[kwargs['collection']].update_one({'guild_id': kwargs['guild_id']}, {'$set': {kwargs['component']: new_setup}})

        return await func(self, *args, **kwargs)
    return wrapper

def connection_success_check(client):
    print("Database: ", end="")
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as error:
        print(error)


class Database():
    def __init__(self):
        self.client = AsyncIOMotorClient(mongodb_key)
        self.discord = self.client.discord
        connection_success_check(self.client)

    @setup_search
    @members_search
    async def find_one(self, collection: str, guild_id: int, component: str = None) -> any:
        result = await self.discord[collection].find_one({'guild_id': guild_id})
        return result[component] if result and component else result

    async def update_one(self, collection: str, guild_id: int, key: str, value: any) -> int:
        result = await self.discord[collection].update_one({'guild_id': guild_id}, {'$set': {key: value}})
        return result.modified_count
