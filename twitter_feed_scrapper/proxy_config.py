import os

from pydantic import BaseSettings, SecretStr


class ProxyConfig(BaseSettings):
    host: str
    port: str
    user: SecretStr
    password: SecretStr

    class Config:
        env_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.proxy_config')
        env_file_encoding = 'utf-8'


proxy_config = ProxyConfig()
