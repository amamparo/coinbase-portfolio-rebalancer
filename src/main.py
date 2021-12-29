from typing import Dict, Any
from injector import inject, Injector
from src.rebalancer import Rebalancer


@inject
def main(rebalancer: Rebalancer) -> None:
  rebalancer.rebalance()


def lambda_handler(event: Dict = None, context: Any = None) -> None:
  Injector().call_with_injection(main)


if __name__ == '__main__':
  lambda_handler()
