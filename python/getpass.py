#!/usr/bin/env python3.12

from subprocess import Popen, PIPE, STDOUT
import argparse
import sys
import codecs
import os
import yaml


def load_vault(src_vault="~/.vault.yml"):
    vault = os.path.expanduser(src_vault)
    proc = Popen(["/opt/homebrew/bin/ansible-vault","view",vault],
                 stdout=PIPE,
                 stdin=PIPE,
                 stderr=STDOUT)
    output = ''

    for line in proc.stdout.readlines():
        output += codecs.getdecoder("unicode_escape")(line)[0]

    return yaml.safe_load(output)


def _get_passwd(vault={},category=None,type=None,subtype=None,list=False):
    if category == None and list:
        return vault.keys()
    if category in vault:
        if type == None and list:
            return vault[category].keys()
        if type in vault[category]:
            if subtype == None and list:
                return vault[category][type].keys()
            if subtype in vault[category][type]:
                return vault[category][type][subtype]


def retrieve(vault={},category=None,type=None,subtype=None,pspec=[],list=False):
    if len(pspec) > 0:
        plist = []
        for spec in pspec:
            category, type, subtype = spec.split(':')
            plist.append( _get_passwd(vault,category, type, subtype) )
        return plist
    
    else:
        return _get_passwd(vault,category, type, subtype, list)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract password from an Ansible vault")
    parser.add_argument("--vault","-v",action="store",required=False, default="~/.vault.yml")
    parser.add_argument("--list","-l",action="store_true",required=False, default=False)
    parser.add_argument("--category","-c",action="store",required=False,default=None)
    parser.add_argument("--type","-t",action="store",required=False,default=None)
    parser.add_argument("--subtype","-s",action="store",required=False,default=None)
    parser.add_argument("--passwd","-p",action="append",required=False,default=[])
    args = parser.parse_args(sys.argv[1:])

    vault = load_vault(args.vault)
    for pw in retrieve(vault,args.category,args.type,args.subtype,args.passwd,args.list):
        print(pw)

