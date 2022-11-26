from typing import List

import motor.motor_asyncio
import config


class DataBaseManager:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(config.MONGO_IP, config.MONGO_PORT)
        self.db = self.client[config.MONGO_DB_NAME]

        self.categories = self.db.categories

    async def create_category(self, category: str):
        await self.categories.insert_one({'category': category})

    async def check_category(self, category: str):
        return True if await self.categories.find_one({'category': category}) else False

    async def get_categories(self):
        categories = []
        async for doc in self.categories.find({}, {'category': 1}):
            categories.append(doc['category'])
        return categories

    async def get_content_subcategory(self, category: str, path: List[str], pole: str):
        path_str = ''
        for name in path:
            path_str += f'subcategories.{name}.'
        path_str += pole

        content = await self.categories.find_one({'category': category},
                                                 {path_str: 1})
        for name in path:
            content = content['subcategories'][name]

        return content[pole] if pole in content else None

    async def get_subcategories(self, category: str, path=None):
        if path is None:
            path = []

        content = await self.get_content_subcategory(category, path, 'subcategories')

        return list(content.keys()) if content else []

    async def get_data(self, category: str, path: List[str] = None):
        if path is None:
            path = []

        content = await self.get_content_subcategory(category, path, 'data')

        return content if content else {}

    ###########################################################################################
    #########################################ADMIN#############################################
    ###########################################################################################
    async def create_subcategory(self, category, path, subcategory, data=None):
        path_str = ''
        for name in path:
            path_str += f'subcategories.{name}.'
        path_str += f'subcategories.{subcategory}'

        await self.categories.update_one({'category': category},
                                         {'$set': {path_str: {} if data is None else {'data': data}}})

    async def edit_subcategory(self, category, path, old_name, new_name):
        path_str = ''
        for name in path:
            path_str += f'subcategories.{name}.'
        path_str += f'subcategories'

        await self.categories.update_one({'category': category},
                                         {'$rename': {f'{path_str}.{old_name}': f'{path_str}.{new_name}'}})

    async def delete_subcategory(self, category, path, subcategory):
        path_str = ''
        for name in path:
            path_str += f'subcategories.{name}.'
        path_str += f'subcategories.{subcategory}'

        await self.categories.update_one({'category': category},
                                         {'$unset': {path_str: 1}})

    async def set_data(self, category, path, data):
        path_str = ''
        for name in path:
            path_str += f'subcategories.{name}.'
        path_str += 'data'
        await self.categories.update_one({'category': category}, {'$set': {path_str: data}})

    async def add_data(self, category, path, key, data):
        path_str = ''
        for name in path:
            path_str += f'subcategories.{name}.'
        path_str += f'data.{key}'
        await self.categories.update_one({'category': category}, {'$push': {path_str: data}})
