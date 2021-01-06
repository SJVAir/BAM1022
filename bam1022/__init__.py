import dotenv
dotenv.load_dotenv()

import os

from .driver import BAM1022
from .sjvair_api import SJVAirAPI

monitor = BAM1022(
    port=os.environ.get('BAM1022_PORT'),
    password=os.environ.get('BAM1022_PASSWORD'),
    debug=bool(int(os.environ.get('BAM1022_DEBUG', 0))),
)

sjvair = SJVAirAPI()
