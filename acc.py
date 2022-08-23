import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import fng_api
import time
import threading


class Browser(webdriver.Chrome):
    """webdriver chrome browser to automate web"""

    def __init__(self, adp=False):
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

    def hover_mouse(self, xpath, timeout=15):
        """hover mouse at an element; calls wait_for_element and then hovers"""
        el = self.wait_for_element(xpath, timeout)
        if el is not None:
            ActionChains(self).move_to_element(el).perform()

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

    def wait_n_click(self, xpath, timeout=15):
        """call wait for element and click if possible"""
        el = self.wait_for_element(xpath, timeout)
        time.sleep(0.5)
        if el is not None:
            try:
                el.click()
                print(f"element (\"{xpath}\") clicked")
            except selenium.common.exceptions.ElementNotInteractableException:
                print(f"element (\"{xpath}\") not interactable; error")
                self.wait_n_click(xpath, timeout)

    def js_click(self, xpath:str):
        """click element using js"""
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

class Account(Browser):
    """bananatic account"""

    def __init__(self, mail:Mail):
        super(Account, self).__init__()
        self.TRADELINK = "https://steamcommunity.com/tradeoffer/new/?partner=489030525&token=Px3P0Diw"
        self.VERIFY_TOPIC = "Potwierdzenie rejestracji - Bananki.pl"
        self.passwd = ""
        self.login = ""
        self.mail = mail
        self.get_identity()

    def __str__(self):
        return "account browser"

    def get_identity(self):
        """get the identity of acc"""
        ident = fng_api.getIdentity()
        self.passwd = ident.password
        print(f"got password: \"{self.passwd}\"")
        self.login = ident.username
        print(f"got login: \"{self.login}\"")

    def verify(self):
        """verify the account"""
        temp_passwd = self.mail.confirm_mail(self.VERIFY_TOPIC)
        # self.wait_n_click('//i[@class="banicon banicon-settings"]')
        # time.sleep(1)
        # self.wait_n_click('//a[text()="Ustawienia konta"]')
        # time.sleep(2)
        self.get("https://www.bananki.pl/profile/settings/")
        self.wait_n_click('//strong[text()="Zmiana hasła"]')

        ipt_new_pass1 = self.wait_for_element('//input[@name="new_password"]')
        ipt_new_pass2 = self.wait_for_element('//input[@name="confirm_password"]')
        ipt_new_pass3 = self.wait_for_element('//input[@name="old_password"]')

        time.sleep(2)
        ipt_new_pass1.send_keys(self.passwd)
        ipt_new_pass2.send_keys(self.passwd)
        ipt_new_pass3.send_keys(temp_passwd)
        self.wait_n_click('//input[@name="old_password"]/../button')
        self.wait_for_element('//div[text()="Hasło zostało zmienione"]')    # todo: probably not needed
        time.sleep(2)
        self.execute_script("$('body').css('overflow','auto');$('#popup').remove()")
        # self.wait_for_element('//a[@class="close transition"]')
        # self.js_click('//a[@class="close transition"]')

        # steamlink_textarea = self.wait_for_element('//textarea')
        # steamlink_textarea.send_keys("https://steamcommunity.com/tradeoffer/new/?partner=301586080&token=ziKzOAPv")
        # self.wait_n_click('//textarea/../button')

    def save_logindata(self):
        """save mail and password to database.txt"""
        with open("database.txt", "a") as f:
            f.write(f"{self.mail.mail} {self.passwd}\n")
            f.close()

    def join_roulette(self, place:int):
        """get into operation phoenix case roulette"""
        # firstly searching for item and hovering to click
        # self.get("https://www.bananki.pl/sklep/cs-go/?o=4")
        # self.hover_mouse('//img[@src="https://bananki-15199.kxcdn.com/photos/shop/204.png"]')

        # direct lottery link
        self.get("https://www.bananki.pl/lottery/win/?item=csgo-204")
        self.wait_n_click('//b[text()="Sprawdź stół"]')
        # self.execute_script("$('#popup .info').hide();$('#popup .table').show()")   # instead of clicking run script that click does
        self.wait_for_element('//b[text()="Do stołu dołączyli:"]')
        self.execute_script(
            "$('#place-%d a').click();$('#popup > div').animate({scrollTop: '150px'})" % place) # run script to take a seat with place instead for searching for div
        self.wait_n_click('//input[@value="TAK"]')
        linkarea = self.wait_for_element('//textarea[@name="exchange-link"]')
        tradelink = input("enter tradelink")
        linkarea.send_keys(tradelink)
        # linkarea.send_keys(self.TRADELINK)
        self.wait_n_click('//input[@value="Wyślij"]')

if __name__ == "__main__":
    print("module loaded as main")