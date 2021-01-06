import json

from .. import monitor


def print_columns(data):
    for k, v in data.items():
        print('{0:<15} {1:>20}'.format(k, v))


def print_json(data):
    print(json.dumps(data, indent=4))


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--format', choices=['columns', 'json'],
        help='How to format the output.', default='columns')
    args = parser.parse_args()

    printer = {
        'columns': print_columns,
        'json': print_json,
    }[args.format]

    data = monitor.latest()
    printer(data)

if __name__ == '__main__':
    main()
