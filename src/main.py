from typing import Dict, Any

from injector import inject, Injector

from src.portfolio_optimizer import PortfolioOptimizer


@inject
def main(portfolio_optimizer: PortfolioOptimizer) -> None:
  portfolio_optimizer.optimize_portfolio()


def lambda_handler(event: Dict = None, context: Any = None) -> None:
  Injector().call_with_injection(main)


if __name__ == '__main__':
  lambda_handler()
