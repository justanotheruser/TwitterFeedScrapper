import os

from pydantic import BaseSettings, SecretStr


class TwitterAccConfig(BaseSettings):
    user: SecretStr
    password: SecretStr

    class Config:
        env_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.twitter_acc_config')
        env_file_encoding = 'utf-8'


twitter_acc_config = TwitterAccConfig()
