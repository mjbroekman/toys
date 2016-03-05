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

def display_host(scan_id, host, details):
    """
    Display details for a specific host
    """
    print('', end='\t')
    print('Score: ', host['score'], end='\t')
    print('Critical: ', host['critical'], end='\t')
    print('High: ', host['high'], end='\t')
    print('Medium: ', host['medium'], end='\t')
    print('Low: ', host['low'], end='\t')
    print('Info: ', host['info'], end='\t')
    print('Host: ', host['hostname'])

    if details != 0:
        hostdata = connect('GET', '/scans/'+format(scan_id)+'/hosts/'+format(host['host_id']))
        print('\t\tGeneral Information', end='\n\t\t\t')
        hostinfo = hostdata['info']

        for key in 'mac-address', 'operating-system', 'host-ip', 'host-fqdn':
            try:
                print(key, ': ', format(hostinfo[key]).replace('\n', ', '), end='\n\t\t\t')
            except KeyError:
                print('', end='')

        print('')

        if len(hostdata['compliance']) > 0:
            print('\t\tCompliance Results:', end='\n\t\t\t')

            for compdata in hostdata['compliance']:
                for key in 'count', 'severity', 'plugin_id', 'plugin_family':
                    try:
                        print(key, ': ', format(compdata[key]).replace('\n', ', '), end='\t')
                    except KeyError:
                        print('', end='')

                print('', end='\n\t\t\t')

            print('')

        if len(hostdata['vulnerabilities']) > 0:
            print('\t\tVulnerability Results:', end='\n\t\t\t')

            for vulndata in hostdata['vulnerabilities']:
                if vulndata['severity'] > 0:
                    for key in 'count', 'severity', 'plugin_family', 'plugin_name':
                        try:
                            print(key, ': ', format(vulndata[key]).replace('\n', ', '), end='\t')
                        except KeyError:
                            print('', end='')

                    print('', end='\n\t\t\t')

            print('')

        print('')



def display_scan(scan, summary, details):
    """
    Show the details of a completed scan
    """
    scandata = connect('GET', '/scans/'+format(scan['id']))
    print('{:<50}'.format(scan['name']), end='  ')

    if scan['starttime'] is None:
        print('{0:^15}'.format('On Demand'), end='  ')
        print('{0:^12}'.format(' '), end='  ')
    else:
        print('{0:<15}'.format(scan['starttime']), end='  ')
        print('{0:<12}'.format(scan['timezone']), end='  ')

    print('{:^5}'.format(scandata['info']['hostcount']))

    if summary != 0:
        for host in scandata['hosts']:
            display_host(scan['id'], host, details)



def get_scans(status=None, summary=0, details=0):
    """
    Login to nessus.
    """

    # login = {'username': usr, 'password': pwd}
    data = connect('GET', '/scans')
    print('{0:^6}  {1:^9}  {2:^50}  {3:^15}  {4:^12}  {5:^5}'.
          format('ID', 'State', 'Scan Name', 'Start Time', 'Timezone', 'Hosts'))
    print('{0}  {1}  {2}  {3}  {4}  {5}'.format('-'*6, '-'*9, '-'*50, '-'*15, '-'*12, '-'*5))

    for scan in data['scans']:
        if status is None or scan['status'] == status:
            # print(scan)
            # We want scan['rrules'] for displaying the schedule
            # scaninfo = connect('GET', '/scans/'+format(scan['id']))
            # print(scaninfo)

            print('{:<6}'.format(scan['id']), end='  ')
            if scan['status'] == 'empty' and scan['starttime'] is not None:
                scan['status'] = 'scheduled'

            print('{:^9}'.format(scan['status']), end='  ')

            if scan['status'] != 'completed':

                print('{:<50}'.format(scan['name']), end='  ')

                if scan['starttime'] is None:
                    print('{0:^15}'.format('On Demand'))
                else:
                    print('{0:<15}'.format(scan['starttime']), end='  ')
                    print('{0:<12}'.format(scan['timezone']))
            else:
                display_scan(scan, summary, details)

if __name__ == '__main__':
    # refresh_scans()
    try:
        get_scans()
    except KeyboardInterrupt:
        print('Exiting...')
