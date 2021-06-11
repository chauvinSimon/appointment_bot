"""
- poll a website (based on 'onlinetermine.zollsoft.de') that references available doses of vaccination
- if one slot is available, fill the registration form very quickly (faster that humans) and let the user validate
"""

import datetime
import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def apply_keys(link, sleep_time=0.2):
    """ the sequence of keys is of course specific to this page. But it can be easily adapted """
    with webdriver.Chrome(ChromeDriverManager().install()) as driver:
        driver.get(link)
        time.sleep(1)
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.common.action_chains import ActionChains

        def tab(t):
            ActionChains(driver).send_keys(Keys.TAB).perform()
            time.sleep(t)

        def space(t):
            ActionChains(driver).send_keys(Keys.SPACE).perform()
            time.sleep(t)

        def shift_tab(t):
            a = ActionChains(driver)
            a.key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT)
            a.perform()
            time.sleep(t)

        # first page
        tab(sleep_time)
        tab(sleep_time)
        # tab(sleep_time)  # for Johnson
        space(sleep_time)
        tab(sleep_time)
        space(sleep_time)
        tab(sleep_time)
        space(sleep_time)

        # second page
        shift_tab(sleep_time)
        shift_tab(sleep_time)
        space(sleep_time)
        tab(sleep_time)
        tab(sleep_time)
        space(sleep_time)

        # third page
        shift_tab(sleep_time)
        shift_tab(sleep_time)
        shift_tab(sleep_time)

        space(sleep_time)
        for _ in range(6):
            shift_tab(sleep_time / 10)
        for string in [
            "firstname",
            "lastname",
            "dd.mm.yyyy",
            "0123456789",
            "my_address@gmail.com"
        ]:
            ActionChains(driver).send_keys(string).perform()
            time.sleep(sleep_time)
            tab(sleep_time)

        for _ in range(4):
            tab(sleep_time)

        # at the point the form is filled. The user should make final 'ENTER' or 'SPACE'
        # space(sleep_time)
        while True:
            pass


def main():
    link = "https://onlinetermine.zollsoft.de/patientenTermine.php?uniqueident=6087dd08bd763"

    i = 0
    while True:
        # adapt the frequency
        time.sleep(10)

        print(i)
        print(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
        i += 1

        chrome_options = Options()
        chrome_options.headless = True
        try:
            with webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options) as driver:
                driver.get(link)
                time.sleep(1)

                # check the content
                content = driver.page_source
                # in this particular case, a first option for AstraZeneca is always present
                if "Impfung mit AstraZeneca" not in content:
                    print('error: no [Impfung mit AstraZeneca]')
                    continue

                # trigger: in this particular case, I am looking for the J&J option
                if "Johnson" in content:
                    apply_keys(link=link)
        except Exception as e:
            print(e)
        time.sleep(1)


if __name__ == '__main__':
    main()
