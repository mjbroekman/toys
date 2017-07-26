#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3
'''
docstring
'''

import requests
import bs4

BASE_URL = "https://mwomercs.com/"
LOGIN_URL = BASE_URL + "login"
PROF_URL = BASE_URL + "profile"
STATS_URL = PROF_URL + "/stats"
MECH_DATA = STATS_URL + "?type=mech"
WEAP_DATA = STATS_URL + "?type=weapon"
MAPS_DATA = STATS_URL + "?type=map"
MODE_DATA = STATS_URL + "?type=mode"

def parse_data(url, tag):
    '''docstring'''
    soup = get_data(url)
    print(soup.prettify().encode('utf-8').strip())

def get_data(url):
    '''docstring'''
    try:
        res = session.get(url)
        res.raise_for_status()
    except requests.exceptions.SSLError:
        print("SSL Error occurred")

    return bs4.BeautifulSoup(res.text, "html.parser")

def check_login(soup):
    '''docstring'''
    links = soup.select('a[href=/login]')

    if links:
        return False

    return True

def get_login_cookie(url):
    '''docstring'''
    from getpass import getpass

    print("Enter user email: ", end='')
    email = input()
    print("Enter user password: ", end='')
    passwd = getpass()
    print()
    payload = {'email':email, 'password':passwd}

    r = session.post(url, payload)
    print(r.text.encode('utf-8').strip())

if __name__ == '__main__':
    try:
        session = requests.Session()
        get_login_cookie(LOGIN_URL)
        if check_login(get_data(STATS_URL)):
            print("Logged in successfully")
#            parse_data(PROF_URL, 'div')

    except KeyboardInterrupt:
        print('Exiting...')
