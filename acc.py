import selenium.common.exceptions
import urllib3.exceptions
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import time
import pyautogui
import functools


class Browser(webdriver.Chrome):
    """webdriver chrome browser to automate web"""

    def __init__(self, adp=False):
        self.REFRESH_COORDS = (105, 65)

        opt = Options()
        opt.add_argument("start-maximized")
        opt.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1,
                                              "credentials_enable_service": False,
                                              "profile.password_manager_enabled": False})
        opt.add_experimental_option('useAutomationExtension', False)
        opt.add_argument('--disable-blink-features=AutomationControlled')
        opt.add_experimental_option("excludeSwitches", ["enable-automation"])

        if adp:
            opt.add_extension("./adp.crx")

        super(Browser, self).__init__(chrome_options=opt, executable_path="./chromedriver.exe")

        self.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.command_executor.set_timeout(15)  # to throw exception so script wont hang

        if adp:
            self.adblock_install()

        print(f"initialized browser: {self.__str__()}")

    def __str__(self):
        return "main browser class"

    def adblock_install(self):
        """add adblock and close starting site"""
        for i in range(5):
            try:
                self.switch_to.window(self.window_handles[1])
                break
            except IndexError:
                time.sleep(1)
                continue
        self.wait_for_element('//body[@class="page-loaded"]', 30)
        self.close()
        self.switch_to.window(self.window_handles[0])  # kill the adblock tab and get back to main tab

    @staticmethod   # this is done so pycharm wont freak out, decorator should be probably moved out of class
    def safe_interact(func):
        """decorator for interact functions to handle errors that hang selenium process"""
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            self:Browser
            try:
                # use one or two arguments depending on given arguments
                if len(args) == 1 and len(kwargs) == 1:   # one arg and one kwarg is always funtions with elements
                    res = func(self, args[0], kwargs["timeout"])
                elif len(args) == 2:    # last arg fills keyword argument
                    res = func(self, args[0], args[1])
                else:  # use only one argument for both self.get and element funtions
                    res = func(self, args[0])
                print("action succesful")
                return res

            except (TimeoutError, urllib3.exceptions.ReadTimeoutError) as e:
                print("action failed, refreshing and retrying")
                pyautogui.click(x=self.REFRESH_COORDS[0], y=self.REFRESH_COORDS[1])  # todo: webdriver hanging
                # due to hanging while waiting for response from its own server,
                # it is needed to manually click refresh button on chrome
                return wrapper(self, *args, **kwargs)

        return wrapper

    @safe_interact
    def get(self, url:str):
        """overrides webdrivers get to add safe decorator"""
        super(Browser, self).get(url)

    @safe_interact
    def hover_mouse(self, xpath, timeout=15):
        """hover mouse at an element; calls wait_for_element and then hovers"""
        el = self.wait_for_element(xpath, timeout)
        if el is not None:
            ActionChains(self).move_to_element(el).perform()

    @safe_interact
    def wait_for_element(self, xpath, timeout=15):
        """wait for element and return it or return none after reaching timeout"""
        try:
            el = WebDriverWait(self, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        except selenium.common.exceptions.TimeoutException:
            print(f"element not found, reached timeout (\"{xpath}\")")
            return None
        el: WebElement
        print(f"found element \"{xpath}\"")
        return el

    @safe_interact
    def wait_n_click(self, xpath, timeout=15):
        """call wait for element and click if possible"""
        el = self.wait_for_element(xpath, timeout)
        if el is not None:
            try:
                el.click()
                print(f"element (\"{xpath}\") clicked")
            except selenium.common.exceptions.ElementNotInteractableException:
                print(f"element (\"{xpath}\") not interactable; error")
                self.wait_n_click(xpath, timeout)

    def safe_click(self, xpath, timeout=15):
        """call wait_n_click while watching for errors that hang selenium process"""
        try:
            self.wait_n_click(xpath, timeout)
            print("click succesful")
        except (TimeoutError, urllib3.exceptions.ReadTimeoutError) as e:
            print("click failed, refreshing and retrying")
            pyautogui.click(x=self.REFRESH_COORDS[0], y=self.REFRESH_COORDS[1])  # todo: webdriver hanging
            # due to hanging while waiting for response from its own server,
            # it is needed to manually click refresh button on chrome
            self.safe_click(xpath, timeout)

    @safe_interact
    def js_click(self, xpath:str, timeout=15):
        """click element using js"""
        el = self.wait_for_element(xpath, timeout)
        if el is not None:
            self.execute_script("a = document.evaluate('%s', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; a.click();" % xpath)

class Mail(Browser):
    """10minutemail.net control"""
    def __init__(self):
        super(Mail, self).__init__(adp=True)
        self.mail = ""
        self.get("https://10minutemail.net/")
        self.get_mail()

    def __str__(self):
        return "mail browser"

    def get_mail(self):
        """get fresh mail adress"""
        el_mailinput = self.wait_for_element('//*[@id="fe_text"]')
        self.mail = el_mailinput.get_attribute("value")
        print(f"got email adress: \"{self.mail}\"")

    def get_messages(self):
        """get and return all messages recieved"""
        mailtable = self.wait_for_element('//*[@id="maillist"]/tbody')
        items = len(mailtable.find_elements(By.XPATH, "./tr")) - 1
        print(f"found {items} messages")
        topics = []
        for i in range(items):
            singlemailtable = mailtable.find_elements(By.XPATH, "./tr")[i + 1]
            sender = singlemailtable.find_element(By.XPATH, "./td[1]")
            topic = singlemailtable.find_element(By.XPATH, "./td[2]")
            date = singlemailtable.find_element(By.XPATH, "./td[3]")
            topics.append(topic.text)
            print(f"\t{i}\t-\tfrom: \"{sender.text}\"\ttopic: \"{topic.text}\"\tdate: \"{date.text}\"")
        return topics

    def confirm_mail(self, mailtopic:str):
        """opens and reads message recieved + clicks the link"""
        idx = -1
        while idx == -1:
            msg_topics = self.get_messages()
            for t in msg_topics:
                if t == mailtopic:
                    idx = msg_topics.index(mailtopic)
            time.sleep(1)
        self.wait_n_click(f'//*[@id="maillist"]/tbody/tr[{idx+2}]', timeout=120)
        self.wait_for_element('//h1[text()="Witamy w świecie bananków!"]')
        passwd_line = self.wait_for_element('//*[@id="tab1"]/div[1]/div/div[2]/div[2]/h2[1]').text  # todo: shitty xpath
        temp_passwd = passwd_line.split(" ")[-1]
        self.wait_n_click('//a[text()="POTWIERDŹ EMAIL"]')
        return temp_passwd


if __name__ == "__main__":
    print("module loaded as main")