import os

from .. import monitor
from ..sjvair import SJVAirAPI


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', choices=['all', 'new', 'last'],
        help='Which data report to send', default='all')
    args = parser.parse_args()

    sjvair = SJVAirAPI(monitor_id=os.environ['SJVAIR_MONITOR_ID'])

    command = {
        'all': monitor.CMD_DATA_ALL,
        'new': monitor.CMD_DATA_NEW,
        'last': monitor.CMD_DATA_LAST,
    }[args.type]

    data = monitor.get_data(command)
    for entry in data:
        print(f"Sending [{entry['ConcRT(ug/m3)']}] on [{entry['Time']}]")
        response = sjvair.add_entry(entry)
        import code
        code.interact(local=locals())
        break


if __name__ == '__main__':
    main()
