from injector import inject, singleton

from src.environment import Environment
from coinbase.wallet.client import Client

USDC = 'USDC'


@singleton
class Coinbase:
  @inject
  def __init__(self, env: Environment):
    self.__coinbase = Client(api_key=env.coinbase_key, api_secret=env.coinbase_secret)

  def transfer_usdc(self, wallet_address: str):
    print(wallet_address)
    usdc_balance = self.__coinbase.get_account(USDC)['native_balance']
    usdc_amount = float(usdc_balance['amount'])
    if not usdc_amount:
      return
    self.__coinbase.send_money(USDC, to=wallet_address, amount=usdc_amount, currency=usdc_balance['currency'])
