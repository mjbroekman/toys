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

CONF_DIR = "/etc/icinga2/repository.d/hosts"
ADD_HOST = "/usr/sbin/icinga2 repository host add"
ADD_SVC = "/usr/sbin/icinga2 repository service add"
COMMIT = "/usr/sbin/icinga2 repository commit"

def usage(msg):
    """
    Usage function
    """
    print(msg)
    print('mkconfig.py [options]')
    print(' -H : hostname')
    print(' -S : service to modify')
    print(' -V : variable setting to change')
    print('')
    print(' Format for -V:')
    print('   Scalar variables -> variable_name:value')
    print('   Hash variables   -> variable_name["key"]:{subvariable:value^subvariable:value^...}')
    print('')
    print(' If -S is not used, variables will be modified within the host object')
    print(' If variable_name is not set, it will be added.')
    print(' If variable_name is already set, it will be modified')
    print(' If value is empty, variable_name will be set to an empty string')
    print(' To remove a variable, prepend the variable_name with -')
    print('')
    print('Example 1: Simple override of the SSH check to use a different command')
    print(' mkconfig.py -H nismaster.iscinternal.com -S ssh -V', end='')
    print(' check_command:tcp -V vars.tcp_port:22')
    print('')
    print('Example 2: More complex setting of HTTP checks on the host')
    print(' mkconfig.py -H login-us.mimecast.com', end='')
    print(' -V vars.http_vhosts["login"]:{http_vhost:login-us.mimecast.com^http_uri:/logon}')
    print('')


def init_config():
    """
    Initialize the configuration object
    """

    cfg = {}
    cfg['host'] = None          # -H
    cfg['svc'] = None           # -S
    cfg['vars'] = []            # -V

    return cfg


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


def create_host(host_name):
    """
    Create a new host object
    """
    cmd = ADD_HOST + " name=" + host_name + " address=" + host_name + " check_command=hostalive"
    print('Do you wish to create a new host object? (y/N) ', end='')
    ans = sys.stdin.read(1)
    if ans != "y" and ans != "Y":
        print('Create the host first using:')
        print(cmd)
        sys.exit(1)

    try:
        os.system(cmd)
    except OSError as err:
        print('An error occurred while trying to run:\n' + cmd + '\n' + COMMIT)
        print(err)
        sys.exit(2)
    except Warning:
        print('Warning occurred: ' + sys.exc_info()[0])
    else:
        os.system(COMMIT)


def check_config(config):
    """
    Validate that all the config settings are 'okay'
    """
    host_conf = CONF_DIR + "/" + config['host'] + ".conf"

    try:
        host_file = open(host_conf, 'r')
    except IOError:
        first_dot = config['host'].find('.')
        short_host = config['host'][:first_dot]
        short_conf = CONF_DIR + "/" + short_host + ".conf"
        print('Short hostname = ' + short_host)
        try:
            host_file = open(short_conf, 'r')
        except IOError:
            print('No such host file (' + host_conf + ' or ' + short_conf + ') found.')
            print('')
            create_host(config['host'])
            # sys.exit(3)
        else:
            host_file.close()
            config['host'] = short_host
            host_conf = short_conf
    else:
        host_file.close()

    # host_file exists, so we know the host's service directory _might_ exist


def main(args):
    """
    Process options and figure out what we're creating
    """
    try:
        opts, args = getopt.getopt(args, "H:S:V:")
    except getopt.GetoptError:
        usage("Unknown option")
        sys.exit(2)

    config = init_config()

    for opt, arg in opts:
        if opt == "-H":
            config['host'] = arg
        elif opt == "-S":
            config['svc'] = arg
        elif opt == "-V":
            config['vars'].append(arg)

    print(config)
    check_config(config)

if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('Exiting...')
