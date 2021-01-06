import os

from datetime import datetime

import pytz

from .. import monitor
from ..sjvair_api import sjvair


def main():
    print('Syncing time...')

    # Fetch the time from the SJVAir API. If we can reach it, we confirm
    # network access and can be reasonably sure that local time is correct.
    try:
        print('Fetching server time...')
        server_time = datetime.fromtimestamp(sjvair.request('time').body, tz=pytz.utc)
    except Exception as err:
        print(f'...Error:')
        print(err)
        return

    print('Comparing local time...')
    local_time = datetime.utcnow().replace(tzinfo=pytz.utc)
    diff = abs((server_time - local_time).total_seconds())

    # If time is more than 5 minutes off from server, shortcut early.
    # We don't want to set an incorrect time...
    if diff > 60:
        print('...Error: Time difference too great.')
        return

    print('Updating BAM1022 time...')
    monitor.update_datetime()
    print('...done!')

if __name__ == '__main__':
    main()
