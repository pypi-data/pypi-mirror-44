#!/usr/bin/env python3

# Copyright (c) 2019 Sergey Barskov
# This code is licensed under MIT License (see LICENSE for details)

import getopt
from os import lstat, path, stat, walk
from os.path import getsize, isdir, isfile, islink
from sys import argv, exit

__version__ = '1.1.7'


class GetSize:
    def getSize(self, arg, unit=None):
        '''
        Get and display the value and size of arg 
        arg: list
        Optional argument:
        unit: Bytes, KiB, MiB, GiB, TiB, PiB, EiB, ZiB, YiB 
        '''
        sf = "{0:.3f} {1} {2}"
        for f in arg:
            for f, s in self.getArgSize(f):
                if unit is None:
                    print(sf.format(*self.convSize(s), f))
                else:
                    print(sf.format(*self.convSize(s, unit), f))

    def getArgSize(self, arg):
        ''' 
        Get value and size in bytes of arg
        arg: string
        '''
        total_dir_size = 0
        try:
            stat(arg)
        except Exception as e:
            print("{} '{}'".format(e.strerror, e.filename))

        if isdir(arg):
            for root, dirs, files in walk(arg):
                p = [path.join(root, ph) for ph in files]
                total_dir_size += getsize(root)
                for f in p:
                    try:
                        if islink(f):
                            total = [(f, lstat(f).st_size)]
                        else:
                            total = [(f, getsize(f))]
                    except Exception as e:
                        print("{} '{}'".format(e.strerror, e.filename))
                        continue
                    for f, s in total:
                        total_dir_size += s
                        yield f, s
            yield arg, total_dir_size
        elif isfile(arg):
            if islink(arg):
                yield arg, lstat(arg).st_size
            else:
                yield arg, getsize(arg)

    def convSize(self, value, unit=None):
        ''' 
        Converting bytes to binary prefix
        value: size in bytes 
        Optional argument:
        unit: Bytes, KiB, MiB, GiB, TiB, PiB, EiB, ZiB, YiB
        '''
        units = {'Bytes': 0, 'KiB': 2**10, 'MiB': 2**20, 'GiB': 2**30,
                 'TiB': 2**40, 'PiB': 2**50, 'EiB': 2**60, 'ZiB': 2**70, 'YiB': 2**80}
        for k, v in units.items():
            if unit == k:
                if v < 1024:
                    break
                value /= v
                break
            if unit is None:
                if value < 1024:
                    break
                value /= 1024
        return value, k


def help():
    print(
        'Usage: ' + path.basename(__file__) + ' [OPTION] FILE...\n\n'
        'Options:\n\
    -h - Show this help\n\
    -v - Show version information\n\
    -b - Bytes\n\
    -k - KiB\n\
    -m - MiB\n\
    -g - GiB\n\
    -t - TiB\n\
    -p - PiB\n\
    -e - EiB\n\
    -z - ZiB\n\
    -y - YiB')


def main():
    g = GetSize()
    try:
        opts, args = getopt.getopt(argv[1:], "hvb:k:m:g:t:p:e:z:y:")
    except getopt.GetoptError as err:
        print(err)
        help()
        exit(2)

    if opts == [] and args == []:
        print('Usage: ' + path.basename(__file__) + ' [OPTION] FILE...')
        print('Type \'' + path.basename(__file__) + ' -h\' for help')
        exit(1)
    elif opts == []:
        g.getSize(argv[1:])

    for opt, arg in opts:
        if opt == "-h":
            help()
            exit(0)
        elif opt == "-v":
            print(path.basename(__file__) + ' version ' + __version__)
            exit(0)
        elif opt in "-b":
            g.getSize(argv[2:], 'Bytes')
        elif opt in "-k":
            g.getSize(argv[2:], 'KiB')
        elif opt in "-m":
            g.getSize(argv[2:], 'MiB')
        elif opt in "-g":
            g.getSize(argv[2:], 'GiB')
        elif opt in "-t":
            g.getSize(argv[2:], 'TiB')
        elif opt in "-p":
            g.getSize(argv[2:], 'PiB')
        elif opt in "-e":
            g.getSize(argv[2:], 'EiB')
        elif opt in "-z":
            g.getSize(argv[2:], 'ZiB')
        elif opt in "-y":
            g.getSize(argv[2:], 'YiB')


if __name__ == '__main__':
    main()
