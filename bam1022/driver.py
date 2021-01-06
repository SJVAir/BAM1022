import csv
import os
import sys
import time

from datetime import datetime
from io import StringIO

import requests
import serial as serial


class BAM1022:
    CR = '\r\n'
    CMD_INIT = f'{CR}{CR}' # Technically 3 CR's, but .run() appends one.
    CMD_PASSWORD = 'PW'
    CMD_SETTINGS = '1'
    CMD_DATA_ALL = '2'
    CMD_DATA_NEW = '3'
    CMD_DATA_LAST = '4'
    CMD_DATE = 'D'
    CMD_TIME = 'T'

    def __init__(self, port=None, password=None, debug=False):
        self.port = port
        self.password = password or '0'
        self.debug = debug

        self.serial = serial.Serial(
            port=self.port,
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            stopbits=serial.STOPBITS_ONE,
            timeout=1,
        )

        assert self.serial.is_open
        assert self.run(self.CMD_INIT) == '*'

    @property
    def port(self):
        if getattr(self, '_port', None) is None:
            if sys.platform.startswith('darwin'):
                return '/dev/cu.SLAB_USBtoUART'
            return '/dev/ttyUSB0'  # Reasonable default for Linux
        return self._port

    @port.setter
    def port(self, value):
        self._port = value

    def log(self, message):
        if self.debug:
            print(message)

    def readlines(self):
        '''
            Read multiple lines from the serial connection
            and join them into a single decoded string with
            whitespace stripped away.
        '''
        output = self.serial.readlines()
        output = ''.join([b.decode('utf-8') for b in output])
        return output.strip()

    def run(self, command):
        '''
            Send a command to the monitor and return the response.
        '''
        self.log(f'>> {command}')
        command = f'{command}{self.CR}'.encode('utf-8')
        self.serial.write(command)
        time.sleep(1)  # Allow the monitor a second to respond
        output = self.readlines()
        self.log(f'<< {output}')
        return output

    def unlock(self):
        '''
            Send the password to the monitor, unlocking
            it for subsequent commands.
        '''
        return self.run(f'{self.CMD_PASSWORD} {self.password}')

    def lock(self):
        '''
            Send an empty PW command. If the monitor has
            a password. this will lock it. If it doesn't,
            this is effectively a no-op.
        '''
        return self.run(f'{self.CMD_PASSWORD}')

    def get_settings(self):
        return self.run(self.CMD_SETTINGS)

    def get_data(self, cmd):
        '''
            Get a report and parse the CSV data, filtering
            out bad data and yielding each row.
        '''
        data = self.run(cmd)

        data = '\n'.join(data.splitlines()[6:])  # Don't need the first few lines
        file = StringIO(data)
        reader = csv.DictReader(file)

        for row in reader:
            try:
                if int(row['Time'][:4]) < 2020:
                    # If the datetime is pre-2020, consider the row bad.
                    continue
            except Exception:
                # If the year couldn't be parsed out, consider the row bad.
                continue

            yield dict(row)

    def latest(self):
        return next(self.get_data(self.CMD_DATA_LAST))

    def update_datetime(self):
        ''' Set the date/time (UTC) on the BAM. '''
        self.unlock()
        self.run(self.CMD_DATE)
        self.run(datetime.utcnow().strftime('%Y-%m-%d'))
        self.run(self.CMD_TIME)
        self.run(datetime.utcnow().strftime('%H:%M:%S'))
        self.lock()
