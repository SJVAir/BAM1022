import os

from .. import monitor, sjvair


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', choices=['all', 'new', 'last'],
        help='Which data report to send', default='all')
    args = parser.parse_args()

    command = {
        'all': monitor.CMD_DATA_ALL,
        'new': monitor.CMD_DATA_NEW,
        'last': monitor.CMD_DATA_LAST,
    }[args.type]

    data = monitor.get_data(command)
    for entry in data:
        if entry['ConcRT(ug/m3)'] == '+99999.0':
            print(f"Skipping [{entry['ConcRT(ug/m3)']}] on [{entry['Time']}]")
            continue
        print(f"Sending [{entry['ConcRT(ug/m3)']}] on [{entry['Time']}]")
        response = sjvair.add_entry(entry)


if __name__ == '__main__':
    main()
