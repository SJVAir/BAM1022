from .. import monitor


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', choices=['all', 'new', 'last'],
        help='Which data report to run', default='all')
    args = parser.parse_args()

    command = {
        'all': monitor.CMD_DATA_ALL,
        'new': monitor.CMD_DATA_NEW,
        'last': monitor.CMD_DATA_LAST,
    }[args.data]

    data = monitor.get_data(command)

if __name__ == '__main__':
    main()
