#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3
'''
MWO Stats retrieval scrapper

Requirements:
- python3
- selenium python module
- Firefox browser
- geckodriver from Mozilla
- a desire to see math on your stats

Usage:
$ mwo_stats.py

This will write out your stats along with some additional calculated stuff to mwo_stats.csv

You can then open that in your spreadsheet application of choice and see all the pretty data

'''

from getpass import getpass
from selenium import webdriver

BASE_URL = "https://mwomercs.com/"
PROF_URL = BASE_URL + "profile"
STATS_URL = PROF_URL + "/stats"
MECH_DATA = STATS_URL + "?type=mech"
WEAP_DATA = STATS_URL + "?type=weapon"
MAPS_DATA = STATS_URL + "?type=map"
MODE_DATA = STATS_URL + "?type=mode"

def login_to_mwo():
    '''
    Prompt for username / passwd
    Open the selenium-driven browser
    Log in
    Return the browser object
    '''
    print("Enter user email: ", end='')
    email = input()

    passwd = getpass("Enter user password: ")
    print()

    ffox = webdriver.Firefox()
    ffox.get(PROF_URL)

    login_link = ffox.find_element_by_link_text('LOGIN')
    login_link.click()

    email_input = ffox.find_element_by_id('email')
    email_input.send_keys(email)

    psswd_input = ffox.find_element_by_id('password')
    psswd_input.send_keys(passwd)
    psswd_input.submit()

    return ffox

def get_mechbays(ffox):
    '''
    Retrieve the profile page
    Iterate over mechBay classed tags and return the dictionary of owned my_mechs
    '''
    ffox.get(PROF_URL)
    mech_bays = ffox.find_elements_by_class_name('mechBay')
    mech_bay = {}
    for bay in mech_bays:
        try:
            mech_bay[bay.text.strip()] += 1
        except KeyError:
            mech_bay[bay.text.strip()] = 1

    return mech_bay

def get_stat_data(url, ffox):
    '''
    Retrieve the specific stats page
    Find the table of stats and store each row as a dictionary entry under the first column
    Return the dictionary of stats
    '''
    ffox.get(url)
    my_stats = {}
    stat_list = [x.text.strip() for x in ffox.find_elements_by_xpath('//thead/tr/th')]
    for obj in ffox.find_elements_by_xpath('//tbody/tr'):
        idx = 0
        obj_name = ''
        for stat in obj.find_elements_by_tag_name('td'):
            if idx == 0:
                obj_name = stat.text.strip()
                my_stats[obj_name] = {}
            else:
                my_stats[obj_name][stat_list[idx]] = stat.text.strip()
            idx += 1

    return my_stats

def main():
    '''
    Main processing
    '''

    try:
        browser = login_to_mwo()
        my_mechs = get_mechbays(browser)
        my_mech_stats = get_stat_data(MECH_DATA, browser)
        my_weap_stats = get_stat_data(WEAP_DATA, browser)
        my_maps_stats = get_stat_data(MAPS_DATA, browser)
        my_mode_stats = get_stat_data(MODE_DATA, browser)
    finally:
        browser.close()

    print(str(my_mechs))
    print(str(my_mech_stats))
    print(str(my_weap_stats))
    print(str(my_maps_stats))
    print(str(my_mode_stats))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Aborting...")
