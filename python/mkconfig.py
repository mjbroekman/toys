#!/usr/bin/env python
'''
Take command-line input and write out config files in various formats

Author: Maarten Broekman
'''
from __future__ import print_function
import json
import sys
import getopt
import os
import string
import socket

TYPES = ['host', 'service', 'svc', 'notification', 'contact', 'alert']

def usage(msg):
    """
    Usage function
    """
    print(msg)
    print('mkconfig.py [options]')
    print(' -T : config type', TYPES)
    print(' -H : hostname')
    print(' -C : check command')
    print(' -a : ip address')
    print(' -c : critical level')
    print(' -e : email address')
    print(' -g : group')
    print(' -p : port')
    print(' -s : object name')
    print(' -u : user name')
    print(' -v : vhost name')
    print(' -w : warning level')
    print('')
    print(' -j : JSON string containing configuration information')
    print(' -J : File containing JSON data of configuration information')


def init_config():
    """
    Initialize the configuration object
    """

    cfg = {}
    cfg['type'] = None          # -T
    cfg['hname'] = None         # -H
    cfg['check'] = None         # -C
    cfg['address'] = None       # -a
    cfg['crit'] = -1            # -c
    cfg['email'] = None         # -e
    cfg['group_name'] = None    # -g
    cfg['port'] = 0             # -p
    cfg['oname'] = None         # -s
    cfg['user_name'] = None     # -u
    cfg['vhost'] = None         # -v
    cfg['warn'] = -1            # -w

    return cfg


def test_type(objtype):
    """
    Check that the provided type is valid.
    """
    if objtype in TYPES:
        return objtype
    else:
        usage("Unknown configuration type: " + objtype)
        sys.exit(2)


def test_addr(addr):
    """
    Check to see if we have a valid IPv4 or IPv6 address.
    """
    try:
        socket.inet_pton(socket.AF_INET, addr)
    except socket.error:
        try:
            socket.inet_pton(socket.AF_INET6, addr)
        except socket.error:
            usage("Not a valid address: " + addr)
            sys.exit(3)

    return addr


def test_email(email):
    """
    Check / correct email address
    """
    isc_where = email.find('@iscinternal.com')
    int_where = email.find('@intersystems.com')
    at_where = email.find('@')
    if isc_where < 1 and int_where < 1 and at_where < 1:
        usage("Invalid email address: " + email)
        sys.exit(2)
    elif isc_where > 1 and int_where > 1:
        usage("Invalid email address: " + email)
        sys.exit(2)

    return email


def main(args):
    """
    Process options and figure out what we're creating
    """
    try:
        opts, args = getopt.getopt(args, "T:H:C:a:v:w:c:p:e:u:g:s:j:J:")
    except getopt.GetoptError:
        usage("Unknown option")
        sys.exit(2)

    config = init_config()

    for opt, arg in opts:
        if opt == "-T":
            config['type'] = test_type(arg)
        elif opt == "-H":
            config['hname'] = arg
        elif opt == "-C":
            config['check'] = arg
        elif opt == "-a":
            config['address'] = test_addr(arg)
        elif opt == "-c":
            config['check'] = arg
        elif opt == "-e":
            config['email'] = test_email(arg)


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('Exiting...')
