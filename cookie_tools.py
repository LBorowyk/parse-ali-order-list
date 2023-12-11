import pickle
from os.path import isfile


def dump_cookies(driver, cookie_file_name):
    pickle.dump(driver.get_cookies(), open(cookie_file_name, 'wb'))
    print('Cookie were saving')


def load_cookies(driver, cookie_file_name):
    for cookie in pickle.load(open(cookie_file_name, 'rb')):
        driver.add_cookie(cookie)
    print('Cookie were loading')


def auth(driver, cookie_file_name):
    if isfile(cookie_file_name):
        print('Cookie file was found. start loading cookie')
        load_cookies(driver, cookie_file_name)
    else:
        input('Did you have sign in?')
        print('Start cookie saving')
        dump_cookies(driver, cookie_file_name)
    driver.refresh()
    print('Page was refreshing')
