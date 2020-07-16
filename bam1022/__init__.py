import os

from .driver import BAM1022
from .sjvair import SJVAirClient

monitor = BAM1022(
    port=os.environ.get('BAM1022_PORT'),
    password=os.environ.get('BAM1022_PASSWORD'),
)

sjvair_api = SJVAirAPI(monitor_id=os.environ['SJVAIR_MONITOR_ID'])
