from accountantCore.acc import Browser
from accounts.tenminutemail import Mail
import time
import fng_api
from apis.steam import SteamApi

class BananaticAcc(Browser):
    """bananatic account"""
    def __init__(self, mail:Mail):
        super(BananaticAcc, self).__init__()
        self.VERIFY_TOPIC = "Potwierdzenie rejestracji - Bananki.pl"
        self.passwd = ""
        self.login = ""
        self.mail = mail
        self.get_identity()

    def __str__(self):
        return "account browser"

    def register(self):
        self.get("https://www.bananki.pl/#register")
        ipt_em1 = self.wait_for_element('//*[@id="form-register"]/input[1]')
        ipt_em2 = self.wait_for_element('//*[@id="form-register"]/input[2]')
        ipt_em1.send_keys(self.mail.mail)
        ipt_em2.send_keys(self.mail.mail)
        self.safe_click('//*[@id="form-register"]/input[3]')

        # wait for adblock
        # self.wait_for_element('//*[@id="abm"]')
        # self.execute_script("$('#abm').remove()")

        self.safe_click('//label[@class="sex male"]')
        ipt_login = self.wait_for_element('//input[@name="user_name"]')
        ipt_login.send_keys(self.login)
        self.safe_click('//button[@class="btn submit"]')
        self.safe_click('//a[@id="accept-cookies-checkbox"]')

        self.safe_click('//button[text()="Ruszamy! "]')
        self.safe_click('//button[text()="Dalej "]')
        # self.safe_click('//span[text()="1x Losowy klucz Steam"]')
        self.wait_for_element('//*[@id="skip"]')
        self.js_click('//*[@id="skip"]')
        # self.execute_script("a = document.getElementById('skip'); a.click()")
        # self.safe_click('//*[@id="skip"]')
        self.safe_click('//button[text()="Super !"]')

        self.safe_click('//label[text()="Chcę otrzymywać informacje o nowościach i promocjach od Sedoc LLC."]')
        self.safe_click('//label[text()="Chcę otrzymywać powiadomienia"]')
        self.safe_click('//button[text()="Dalej "]')
        self.safe_click('//button[text()="Super !"]')

        # self.execute_script('a = document.querySelector("#instruction > div > form > button"); a.click();')
        self.safe_click('//*[@id="instruction"]/div/form/button')
        # self.safe_click('//button[text()="Do dzieła!"]')
        self.safe_click('//span[@class="play"]')
        # kill popup window
        for _ in range(5):
            try:
                self.switch_to.window(self.window_handles[1])
                break
            except IndexError:
                time.sleep(1)
                continue
        self.close()
        self.switch_to.window(self.window_handles[0])

        time.sleep(4)
        self.safe_click('//*[@id="onesignal-bell-launcher"]')
        time.sleep(10)  # wait for bell to activate

    # this function is not really working that great with 10minmail temporary mail, it is meant to be used with
    # relogable mail that you can retrieve information from after initially creating it
    def sign_in(self):
        """sign in to an account using parameter email and password"""
        self.get("https://www.bananki.pl/")
        self.wait_n_click("//*[@id='login-btn']")
        ipt_login = self.wait_for_element("//input[@name='user_mail']")
        ipt_passwd = self.wait_for_element("//input[@name='user_pass']")
        ipt_login.send_keys(self.mail.mail)
        ipt_passwd.send_keys(self.passwd)
        self.wait_n_click("//input[@value='Zaloguj się']")


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

    def save_logindata(self):
        """save mail and password to database.txt"""
        with open("database.txt", "a") as f:
            f.write(f"{self.mail.mail} {self.passwd}\n")
            f.close()

    def join_roulette(self, place:int):
        """get into operation phoenix case roulette"""
        # direct lottery link
        self.get("https://www.bananki.pl/lottery/win/?item=csgo-204")
        self.wait_n_click('//b[text()="Sprawdź stół"]')
        self.wait_for_element('//b[text()="Do stołu dołączyli:"]')
        self.execute_script(
            "$('#place-%d a').click();$('#popup > div').animate({scrollTop: '150px'})" % place) # run script to take a seat with place instead for searching for div
        self.wait_n_click('//input[@value="TAK"]')
        linkarea = self.wait_for_element('//textarea[@name="exchange-link"]')

        # todo: temporary solution before rewriting steamapi to static class
        s = SteamApi()
        tradelink = "https://steamcommunity.com/tradeoffer/new/?partner=1424493025&token=" + s.new_tradelink()
        del s

        linkarea.send_keys(tradelink)
        self.wait_n_click('//input[@value="Wyślij"]')