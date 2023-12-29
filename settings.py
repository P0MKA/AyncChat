import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
USER = os.getenv('USER')
AMQP_URL = os.getenv('AMQP_URL')

BYTES_LENGTH = 2048

HOST = '0.0.0.0'
PORT = 8888

BOT_QUEUE = 'bot'
SERVER_QUEUE = 'server'
