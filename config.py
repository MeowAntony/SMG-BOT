import os

TOKEN = os.getenv('SMG_TOKEN')

MONGO_IP = os.getenv('SMG_MONGO_IP')
MONGO_PORT = int(os.getenv('SMG_MONGO_PORT'))
MONGO_DB_NAME = os.getenv('SMG_MONGO_DB_NAME')

ADMINS = list(map(int, os.getenv('SMG_ADMINS').split(',')))

MAIN_ADMIN = int(os.getenv('SMG_MAIN_ADMIN'))
