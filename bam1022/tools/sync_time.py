from .. import monitor


def main():
    print('Syncing time...')
    monitor.update_datetime()
    print('...done.')

if __name__ == '__main__':
    main()
