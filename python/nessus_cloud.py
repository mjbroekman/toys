"""
Basic Nessus Cloud API interactions

Based on python scripts from https://github.com/averagesecurityguy/Nessus6.git
"""
from __future__ import print_function
import json
import sys
import getopt
import requests

# Disable Warning when not verifying SSL certs.
requests.packages.urllib3.disable_warnings()


def build_url(url, resource):
    """
    Build the URL properly
    """
    return '{0}{1}'.format(url, resource)



def connect(method, resource, userdata, data=None, params=None):
    """
    Send a request

    Send a request to Nessus based on the specified data. API keys are required
    and added to the request. Specify the content type as JSON and convert the
    data to JSON format.
    """
    verify = False

    headers = {'X-ApiKeys':
               'accessKey={0}; secretKey={1}'.format(userdata['access'], userdata['secret']),
               'content-type': 'application/json'}

    data = json.dumps(data)

    if method == 'POST':
        req = requests.post(build_url(userdata['url'], resource),
                            data=data, headers=headers, verify=verify)
    elif method == 'PUT':
        req = requests.put(build_url(userdata['url'], resource),
                           data=data, headers=headers, verify=verify)
    elif method == 'DELETE':
        req = requests.delete(build_url(userdata['url'], resource),
                              data=data, headers=headers, verify=verify)
    else:
        req = requests.get(build_url(userdata['url'], resource),
                           params=params, headers=headers, verify=verify)

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



def display_host(userdata, scan_id, host):
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

    if userdata['details'] != 0:
        hostdata = connect('GET',
                           '/scans/'+format(scan_id)+'/hosts/'+format(host['host_id']),
                           userdata)
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



def display_scan(userdata, scan):
    """
    Show the details of a completed scan
    """
    scandata = connect('GET', '/scans/'+format(scan['id']), userdata)
    print('{:<50}'.format(scan['name']), end='  ')

    if scan['starttime'] is None:
        print('{0:^15}'.format('On Demand'), end='  ')
        print('{0:^12}'.format(' '), end='  ')
    else:
        print('{0:<15}'.format(scan['starttime']), end='  ')
        print('{0:<12}'.format(scan['timezone']), end='  ')

    print('{:^5}'.format(scandata['info']['hostcount']))

    if userdata['summary'] != 0:
        for host in scandata['hosts']:
            display_host(userdata, scan['id'], host)



def get_scans(userdata):
    """
    Login to nessus.
    """

    # login = {'username': usr, 'password': pwd}
    data = connect('GET', '/scans', userdata)
    print('{0:^6}  {1:^9}  {2:^50}  {3:^15}  {4:^12}  {5:^5}'.
          format('ID', 'State', 'Scan Name', 'Start Time', 'Timezone', 'Hosts'))
    print('{0}  {1}  {2}  {3}  {4}  {5}'.format('-'*6, '-'*9, '-'*50, '-'*15, '-'*12, '-'*5))

    for scan in data['scans']:
        if userdata['mode'] is None or scan['status'] == userdata['mode']:
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
                display_scan(userdata, scan)



def user_help():
    """
    Basic help
    """
    print('nessus_cloud.py --akey <access_key> --skey <secret_key>', end=' ')
    print('[-S|--scan_id <scan id>] [-H|--host_id <host id>]', end=' ')
    print('[-m|--mode <report mode>]', end=' ')
    print('[-s|--summary] [-D|--details] [-d|--debug] [-h|--help]')
    sys.exit(2)



def main(args):
    """
    Main processing of command line args
    """

    try:
        optlist, args = getopt.getopt(args, 'S:H:m:Dsd',
                                      ['scan_id=', 'host_id=', 'mode=',
                                       'akey=', 'skey=',
                                       'summary', 'details', 'debug'])
    except getopt.GetoptError:
        user_help()

    user = {}
    user['url'] = 'https://cloud.tenable.com:443'
    user['access'] = None
    user['secret'] = None
    user['debug'] = 0
    user['scan_id'] = None
    user['host_id'] = None
    user['summary'] = 0
    user['details'] = 0
    user['mode'] = None

    for opt, arg in optlist:
        if opt == "-m" or opt == '--mode':
            user['mode'] = arg
        elif opt == "-S" or opt == '--scan_id':
            user['scan_id'] = arg
        elif opt == "-H" or opt == '--host_id':
            user['host_id'] = arg
        elif opt == "-s" or opt == '--summary':
            user['summary'] = 1
        elif opt == "-D" or opt == '--details':
            user['details'] = 1
        elif opt == "-d" or opt == '--debug':
            user['debug'] += 1
        elif opt == "--akey":
            user['access'] = arg
        elif opt == "--skey":
            user['secret'] = arg

    if user['access'] is None or user['secret'] is None:
        print('Access and Secret key arguments are mandatory.')
        user_help()

    if user['scan_id'] is None and user['host_id'] is None:
        get_scans(user)


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('Exiting...')
