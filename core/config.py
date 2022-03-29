from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class DbConfig:
    login: str
    password: str
    server: str
    port: int
    db_name: str

    @property
    def db_connection_string(self) -> str:
        return f'postgresql://{self.login}:{self.password}@{self.server}:{self.port}/{self.db_name}'


@dataclass
class Config:
    db: 'DbConfig'

    def __init__(self):
        with Path(__file__, '../..', 'config.yaml').resolve().open() as config_file:
            raw_config: dict = yaml.safe_load(config_file.read())
            self.db = DbConfig(**raw_config['db'])
