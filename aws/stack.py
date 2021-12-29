from os import environ, getcwd

from aws_cdk.aws_events import Rule, Schedule
from aws_cdk.aws_lambda import DockerImageFunction, DockerImageCode
from aws_cdk.core import Stack, Construct, App, Duration


class MyStack(Stack):
  def __init__(self, scope: Construct, _id: str, **kwargs) -> None:
    super().__init__(scope, _id, **kwargs)
    Rule(
      self, 'HourlyRule', schedule=Schedule.rate(Duration.hours(1))
    ).add_target(
      DockerImageFunction(
        self,
        'Function',
        function_name='rebalance-coinbase-portfolio',
        code=DockerImageCode.from_image_asset(
          directory=getcwd(),
          file='Dockerfile',
          exclude=['cdk.out']
        ),
        timeout=Duration.minutes(1),
        allow_public_subnet=True,
        environment={
          'COINBASE_PRO_KEY': environ.get('COINBASE_PRO_KEY'),
          'COINBASE_PRO_SECRET': environ.get('COINBASE_PRO_SECRET'),
          'COINBASE_PRO_PASSPHRASE': environ.get('COINBASE_PRO_PASSPHRASE')
        }
      )
    )


if __name__ == '__main__':
  app = App()
  MyStack(app, 'coinbase-portfolio-rebalancer')
  app.synth()
