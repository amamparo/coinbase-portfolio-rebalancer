from dataclasses import dataclass

from dotenv import load_dotenv
from os import environ

from injector import singleton

load_dotenv()


@dataclass
@singleton
class Environment:
  coinbase_pro_key: str = environ['COINBASE_PRO_KEY']
  coinbase_pro_secret: str = environ['COINBASE_PRO_SECRET']
  coinbase_pro_passphrase: str = environ['COINBASE_PRO_PASSPHRASE']
  coinbase_key: str = environ['COINBASE_KEY']
  coinbase_secret: str = environ['COINBASE_SECRET']
