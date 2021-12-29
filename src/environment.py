from typing import Optional

from dotenv import load_dotenv
from os import environ

load_dotenv()


class Environment:
  @staticmethod
  def get_coinbase_pro_key() -> Optional[str]:
    return environ.get('COINBASE_PRO_KEY')

  @staticmethod
  def get_coinbase_pro_secret() -> Optional[str]:
    return environ.get('COINBASE_PRO_SECRET')

  @staticmethod
  def get_coinbase_pro_passphrase() -> Optional[str]:
    return environ.get('COINBASE_PRO_PASSPHRASE')

