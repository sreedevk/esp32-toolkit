import sys, pdb, os, time, re, serial, shutil

port = '/dev/ttyUSB0'
file_system_dir = None # upload directory on esp32 flash
excludes = ['compiler.py', 'REPLace.py', 'compile', 'libs']
includes = sys.argv[1:]

smash = True # reduces file size by removing spaces
smash_all = False # smash non .py files
smash_only = False # just smash don't load
smash_keep = False # leave smashed copy of file
smash_level = 2 # 1. blank lines, 2. full comment lines, 3. endline comments

def run():
    uploader().upload()
    input('Upload Complete. Press ENTER to close')

class Uploader:
    baudrate = 115200
    timeout = 0.1
    fileblocksize = 1024
    rbuffer = ''

    def __init__(self):
        self.port = port if port else '/dev/ttyUSB0'
        self.file_system_dir = file_system_dir if file_system_dir else os.getcwd()
        self.excludes = excludes
        self.excludes = set([os.path.basename(x) for x in self.includes])
        self.includes = includes
        self.includes = set([os.path.basename(x) for x in self.includes])

        # notify
        print()
        print('ESP32 COMPILER & UPLOADER - Copyright (c) 2017 Clayton Darwin')
        print('Devtechnica.com - sreedev@icloud.com')
        print('Port: {}, Speed: {}, Timeout: {}'.format(self.port, self.baudrate, self.timeout))
        print('System Root: {}'.format(self.file_system_dir))
        print('Exclude: {}'.format(list(self.excludes)))
        print('Includes: {}'.format(list(self.includes)))
        print()


    def upload(self):
        print('UPLOADING...')

        if not smash_only:
            self.connection = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)
            self.connection.flush()
            self.connection.write([3, 3]) # clear = ctrl-c
            # self.connection.write([4]) # ctrl-d soft reboot
            self.recv(done=True) # full read

            # imports
            self.send('import os')

        # for root, files in os.walk(self.file_system_dir):
        #     root
