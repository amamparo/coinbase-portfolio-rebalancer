from injector import inject
from src.coinbase_pro import CoinbasePro

BTC = 'BTC'
ETH = 'ETH'
rebalance_threshold = 0.10


class Rebalancer:
  @inject
  def __init__(self, coinbase_pro: CoinbasePro):
    self.__cbp = coinbase_pro

  def rebalance(self) -> None:
    self.__liquidate_irrelevant_currencies_to_btc()
    self.__rebalance()

  def __liquidate_irrelevant_currencies_to_btc(self) -> None:
    for account in self.__cbp.get_accounts():
      balance = float(account['balance'])
      currency = account['currency']
      if not balance or currency in ['USD', BTC, ETH]:
        continue
      self.__cbp.liquidate(currency, BTC)

  def __rebalance(self) -> None:
    currencies = [BTC, ETH]
    balances_by_currency = {x: self.__cbp.get_usd_balance(x) for x in currencies}
    total_balance = sum(balances_by_currency.values())
    current_weights_by_currency = {
      currency: balance / total_balance
      for currency, balance in balances_by_currency.items()
    }
    target_weight = 1 / len(currencies)
    should_rebalance = any(
      (abs(weight - target_weight) / target_weight) >= rebalance_threshold
      for currency, weight in current_weights_by_currency.items()
    )
    if not should_rebalance:
      print(
        f'\nWeights are close enough to balanced (threshold={rebalance_threshold}). Doing nothing.'
      )
      return
    btc_balance = self.__cbp.get_usd_balance(BTC)
    eth_balance = self.__cbp.get_usd_balance(ETH)
    half_the_difference_usd = abs(btc_balance - eth_balance) / 2
    overbought_currency, underbought_currency = [BTC, ETH] if btc_balance > eth_balance else [ETH, BTC]
    self.__cbp.convert(overbought_currency, underbought_currency,
                       self.__cbp.get_quantity_for_usd(overbought_currency, half_the_difference_usd))
