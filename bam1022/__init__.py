import os

from .driver import BAM1022

monitor = BAM1022(
    port=os.environ.get('BAM1022_PORT'),
    password=os.environ.get('BAM1022_PASSWORD'),
)
