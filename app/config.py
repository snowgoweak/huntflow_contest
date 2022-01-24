from functools import lru_cache

from pydantic import BaseSettings

env_file = {'_env_file': '.env',
            '_env_file_encoding': 'utf-8'}


class Logging(BaseSettings):
    level: str = 'DEBUG'
    format: str = '[%(asctime)s] [%(funcName)s] [%(levelname)s] %(message)s'

    class Config:
        env_prefix = 'LOGGING_'


class HuntFlow(BaseSettings):
    host: str
    token: str
    account_id: int
    work_dir: str
    database_name: str

    class Config:
        env_prefix = 'HF_'


class Settings(BaseSettings):
    logging: Logging = Logging()
    hunt_flow: HuntFlow = HuntFlow(**env_file)


settings = Settings()


@lru_cache()
def get_config():
    return settings
