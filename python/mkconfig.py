#!/usr/bin/env python
'''
Take command-line input and write out config files in various formats

Author: Maarten Broekman
'''
from __future__ import print_function
import getopt
import json
import os
import socket
import string
import sys

CONF_DIR = "/etc/icinga2/repository.d/hosts/"
ADD_HOST = "/usr/sbin/icinga2 repository host add"
ADD_SVC = "/usr/sbin/icinga2 repository service add"
COMMIT = "/usr/sbin/icinga2 repository commit"

CMD_DBG = "echo "

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
    print(' mkconfig.py -H host.domain.com -S ssh -V', end='')
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
    cfg['host_conf'] = None     # initialize host config file location
    cfg['svc_conf'] = None      # initialize service config file location
    cfg['svc_dir'] = None       # initialize service config directory location
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
    e1_where = email.find('@domain1.com')
    e2_where = email.find('@domain2.com')
    at_where = email.find('@')
    if e1_where < 1 and e2_where < 1 and at_where < 1:
        usage("Invalid email address: " + email)
        sys.exit(2)
    elif e1_where > 1 and e2_where > 1:
        usage("Invalid email address: " + email)
        sys.exit(2)

    return email


def create_host(host_name):
    """
    Create a new host object
    """
    cmd = ADD_HOST + " name=" + host_name + " address=" + host_name + " check_command=hostalive"
    print('Do you wish to create a new host object? (y/N) ', end='')
    ans = sys.stdin.readline()
    if ans[:1] != "y" and ans[:1] != "Y":
        print('Create the host first using:')
        print(cmd)
        sys.exit(1)

    try:
        os.system(cmd)
    except OSError as err:
        print('An error occurred while trying to run:\n' + cmd)
        print(err)
        sys.exit(2)
    except Warning:
        print('Warning occurred: ' + sys.exc_info()[0])
    else:
        os.system(COMMIT)


def create_svc(config):
    """
    Create a new host object
    """
    svc_name = config['svc']
    print(config)
    host_name = config['host']
    chk_cmd = ''

    for var in config['vars']:
        if var.find("check_command") == 0:
            chk_cmd = (var.split(':'))[1]

    if chk_cmd == '':
        chk_cmd = svc_name

    cmd = ADD_SVC + " name=" + svc_name + " host_name=" + host_name + " check_command=" + chk_cmd
    print('Do you wish to create a new service object? (y/N) ', end='')
    ans = sys.stdin.readline()
    if ans[:1] != "y" and ans[:1] != "Y":
        print('Create the service first using:')
        print(cmd)
        sys.exit(1)

    try:
        os.system(cmd)
    except OSError as err:
        print('An error occurred while trying to run:\n' + cmd)
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
    if not os.path.isdir(CONF_DIR):
        usage('This should be run on the Icinga2 server. Unable to find ' + CONF_DIR)
        sys.exit(5)

    if config['host'] is None:
        usage('Please specify a host to modify')
        sys.exit(2)

    config['host_conf'] = CONF_DIR + config['host'] + ".conf"

    if not os.path.isfile(config['host_conf']):
        first_dot = config['host'].find('.')
        if first_dot > 0:
            short_host = config['host'][:first_dot]
            short_conf = CONF_DIR + short_host + ".conf"
        else:
            short_host = config['host']
            short_conf = CONF_DIR + short_host + ".conf"

        print('Short hostname = ' + short_host)
        if os.path.isfile(short_conf):
            config['host'] = short_host
            config['host_conf'] = short_conf
        else:
            print('No such host file (' + config['host_conf'] + ' or ' + short_conf + ') found.')
            print('')
            create_host(config['host'])

    print(config)

    if config['svc'] is not None:
        config['svc_dir'] = CONF_DIR + config['host']
        if not os.path.isdir(config['svc_dir']):
            os.system(CMD_DBG + "mkdir " + config['svc_dir'])

        config['svc_conf'] = config['svc_dir'] + "/" + config['svc'] + ".conf"
        if not os.path.isfile(config['svc_conf']):
            print('No such service file (' + config['svc_conf'] + ') found. Creating it.')
            print('')
            create_svc(config)

    return config


def parse_conf(cfgfile):
    """
    Parse a configuration file into a dictionary that we can manipulate
    """
    new_conf = {}
    # parse the current config into a dictionary
    new_conf['dicts'] = []
    new_conf['import'] = []
    current_dict = None
    for line in cfgfile:
        line = line.strip()
        if line.find('object') == 0:
            new_conf['object'] = line
        elif line.find('{') > 0:
            new_conf['dicts'].append(line)
            current_dict = line
            new_conf[line] = {}
        elif line.find('import') >= 0:
            new_conf['import'].append(line)
        elif line.find('=') >= 0:
            vname = (line.split(' = '))[0]
            vval = (line.split(' = '))[1]
            if current_dict is None:
                new_conf[vname] = vval
            else:
                new_conf[current_dict][vname] = vval
        elif line.find('}') >= 0:
            if current_dict is not None:
                current_dict = None

    return new_conf

def update_conf(config):
    """
    Update a configuration object
    """

    if config['svc'] is None:
        ifile = open(config['host_conf'], 'r')
    else:
        ifile = open(config['svc_conf'], 'r')

    icontent = ifile.readlines()

    if len(config['vars']) == 0:
        for line in icontent:
            print(line)
    else:
        new_conf = parse_conf(icontent)

        for var in config['vars']:
            vname = (var.split(':'))[0]
            vval = (var.split(':', 1))[1]
            # check if a key exists for vname
            # set the config dictionary to new value
            new_conf[vname] = vval

    # print(icontent.replace('\n  ', '\n\t'))


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

    config = check_config(config)
    # Now we have a config that has been confirmed to have all the necessary
    # files and directories.
    update_conf(config)


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('Exiting...')
