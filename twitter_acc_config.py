import os
import sys

from pydantic import BaseSettings, SecretStr

bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))


class TwitterAccConfig(BaseSettings):
    user: SecretStr
    password: SecretStr

    class Config:
        env_file = os.path.abspath(os.path.join(bundle_dir, '.twitter_acc_config'))
        env_file_encoding = 'utf-8'


twitter_acc_config = TwitterAccConfig()
