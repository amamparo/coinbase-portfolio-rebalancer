import decimal
from math import floor, log, log10, exp
from time import sleep
from typing import Optional, List, cast

from cbpro import AuthenticatedClient
from injector import inject, singleton

from src.environment import Environment


@singleton
class CoinbasePro:
  @inject
  def __init__(self, env: Environment):
    self.__client = AuthenticatedClient(env.get_coinbase_pro_key(), env.get_coinbase_pro_secret(),
                                        env.get_coinbase_pro_passphrase())
    self.__products_cache: Optional[List[dict]] = None

  def get_accounts(self) -> List[dict]:
    return self.__client.get_accounts()

  def get_products(self) -> List[dict]:
    if not self.__products_cache:
      self.__products_cache = self.__client.get_products()
    return cast(List[dict], self.__products_cache)

  def get_usd_balance(self, currency: str) -> float:
    price = float(self.__client.get_product_ticker(f'{currency}-USD').get('price', 0))
    quantity = self.__get_balance(currency)
    return price * quantity

  def get_quantity_for_usd(self, currency: str, usd: float) -> float:
    price = float(self.__client.get_product_ticker(f'{currency}-USD').get('price', 0))
    return usd / price

  def liquidate(self, from_currency: str, to_currency: str) -> None:
    self.convert(from_currency, to_currency, self.__get_balance(from_currency))

  def convert(self, from_currency: str, to_currency: str, from_amount: float) -> None:
    print(f'\nConverting {from_amount} {from_currency} to {to_currency}')
    product = next((
      x for x in self.get_products()
      if not list({x['base_currency'], x['quote_currency']} - {from_currency, to_currency})
    ), None)
    if not product:
      raise Exception(f'Product not found for {from_currency}, {to_currency}')
    base_currency = product['base_currency']
    quote_currency = product['quote_currency']
    if from_currency == base_currency:
      print(f'Selling {from_amount} {base_currency} with {quote_currency}')
      self.__order(base_currency, quote_currency, 'sell',
                   size=self.__adjust_quantity(from_amount, float(product['base_increment'])))
    else:
      print(f'Buying {base_currency} with {from_amount} {quote_currency}')
      self.__order(base_currency, quote_currency, 'buy',
                   funds=self.__adjust_quantity(from_amount, float(product['quote_increment'])))

  def __order(self, base_currency: str, quote_currency: str, side: str, size: Optional[float] = None,
              funds: Optional[float] = None) -> None:
    if size is not None and funds is not None:
      raise Exception('Cannot specify both `size` and `funds`')
    if size is None and funds is None:
      raise Exception('Must specify `size` or `funds`')
    order = self.__client.place_market_order(
      product_id=f'{base_currency}-{quote_currency}',
      side=side,
      size=size,
      funds=funds
    )
    if 'id' in order:
      order_id = order['id']
      while True:
        order = self.__client.get_order(order_id)
        if order.get('status') != 'pending':
          break
        sleep(0.1)
    print(order)

  def __get_balance(self, currency: str) -> float:
    account = next((x for x in self.__client.get_accounts() if x['currency'] == currency))
    return float(account['balance'] if account and 'balance' in account else 0)

  @staticmethod
  def __adjust_quantity(quantity: float, increment: float) -> float:
    decimal_places = round(log10(round(1 / increment)))
    factor = pow(10, decimal_places)
    return floor(quantity * factor) / factor
