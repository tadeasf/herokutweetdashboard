import os
from dotenv import load_dotenv
load_dotenv()

class TwitterConfig:
    CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
    CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
    ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')


class DBConfig:
    db_user = os.environ.get('DB_USER')
    db_pass = os.environ.get('DB_PASS')
    db_name = os.environ.get('DB_NAME')
    db_host = os.environ.get('DB_HOST')
    db_port = os.environ.get('DB_PORT')


if __name__ == '__main__':
    print(type(os.environ.get('CONSUMER_KEY')))
