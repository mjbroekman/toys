"""
Basic Nessus Cloud API retrieval
"""
from __future__ import print_function
import json
import sys
import requests

# Disable Warning when not verifying SSL certs.
requests.packages.urllib3.disable_warnings()


URL = 'https://cloud.tenable.com:443'
VERIFY = False
TOKEN = ''
ACCESSKEY = '0b9cd9b09892cb7eb96b6ead2e3749120c75d0d9fe566cc03c1b5474052cf226'
SECRETKEY = '7748944b447811bc7b3129ebc45fc6bbf4b06f9e8b8e45227fb8a126bff98bab'

def build_url(resource):
    """
    Build the URL properly
    """
    return '{0}{1}'.format(URL, resource)


def connect(method, resource, data=None, params=None):
    """
    Send a request

    Send a request to Nessus based on the specified data. If the session token
    is available add it to the request. Specify the content type as JSON and
    convert the data to JSON format.
    """
    headers = {'X-ApiKeys': 'accessKey={0}; secretKey={1}'.format(ACCESSKEY, SECRETKEY),
               'content-type': 'application/json'}

    data = json.dumps(data)

    if method == 'POST':
        req = requests.post(build_url(resource), data=data, headers=headers, verify=VERIFY)
    elif method == 'PUT':
        req = requests.put(build_url(resource), data=data, headers=headers, verify=VERIFY)
    elif method == 'DELETE':
        req = requests.delete(build_url(resource), data=data, headers=headers, verify=VERIFY)
    else:
        req = requests.get(build_url(resource), params=params, headers=headers, verify=VERIFY)

    # Exit if there is an error.
    if req.status_code != 200:
        err = req.json()
        print(err['error'])
        sys.exit()

    # When downloading a scan we need the raw contents not the JSON data.
    if 'download' in resource:
        return req.content

    # All other responses should be JSON data. Return raw content if they are
    # not.
    try:
        return req.json()
    except ValueError:
        return req.content


def get_scans():
    """
    Login to nessus.
    """

    # login = {'username': usr, 'password': pwd}
    data = connect('GET', '/scans')
    for scan in data['scans']:
        if scan['status'] != 'completed':
            print('State: ', scan['status'], end="\t")
            print('Name: ', scan['name'])
        else:
            scandata = connect('GET', '/scans/'+format(scan['id']))
            print('State: ', scan['status'], end='\t')
            print('Name: ', scan['name'], end='\t')
            print('Hosts: ', len(scandata['hosts']))

            for host in scandata['hosts']:
                print('', end='\t')
                print('Score: ', host['score'], end='\t')
                print('Critical: ', host['critical'], end='\t')
                print('High: ', host['high'], end='\t')
                print('Medium: ', host['medium'], end='\t')
                print('Low: ', host['low'], end='\t')
                print('Info: ', host['info'], end='\t')
                print('Host: ', host['hostname'])

def get_groups():
    """
    Get the list of groups from Nessus
    """

    data = connect('GET', '/groups')
    for group in data['groups']:
        print('Group: ', group['name'], end='\t')
        print('ID: ', group['id'])

# def logout():
#     """
#     Logout of nessus.
#     """
#
#     connect('DELETE', '/session')


if __name__ == '__main__':
    get_scans()
    # print 'Logout'
    # logout()
