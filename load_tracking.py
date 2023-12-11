from create_browser import ChromeDriver


tracking_url = 'https://global.cainiao.com/newDetail.htm'


def form_tracking_url(track_codes):
    return tracking_url + '?mailNoList=' + '%252C'.join(track_codes) + '&otherMailNoList='


def load_tracking(driver, track_codes):
    driver.get(form_tracking_url(track_codes))


def track(track_codes):
    with ChromeDriver() as driver:
        load_tracking(driver, track_codes)
