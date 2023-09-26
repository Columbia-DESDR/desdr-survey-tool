import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'dummy'

    JWT_SECRET_KEY = 'dummy'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=3)

    ADMIN_USER = 'dummy'
    ADMIN_PWD = 'dummy'

    POSTGRES_CREDS = {
        'user': 'dummy',
        'password': 'dummy',
        'host': 'dummy',
        'port': 'dummy',
        'database': 'dummy'
    }
    POSTGRES_URL = f'postgresql://{POSTGRES_CREDS["user"]}:{POSTGRES_CREDS["password"]}@{POSTGRES_CREDS["host"]}:\
                    {POSTGRES_CREDS["port"]}/{POSTGRES_CREDS["database"]}'
