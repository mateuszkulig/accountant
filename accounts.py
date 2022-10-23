from acc import Browser, Mail
import time
import fng_api

class Bananatic(Browser):
    """bananatic account"""
    def __init__(self, mail:Mail):
        super(Bananatic, self).__init__()
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
        # direct lottery link
        self.get("https://www.bananki.pl/lottery/win/?item=csgo-204")
        self.wait_n_click('//b[text()="Sprawdź stół"]')
        self.wait_for_element('//b[text()="Do stołu dołączyli:"]')
        self.execute_script(
            "$('#place-%d a').click();$('#popup > div').animate({scrollTop: '150px'})" % place) # run script to take a seat with place instead for searching for div
        self.wait_n_click('//input[@value="TAK"]')
        linkarea = self.wait_for_element('//textarea[@name="exchange-link"]')
        tradelink = input("enter tradelink")
        linkarea.send_keys(tradelink)
        self.wait_n_click('//input[@value="Wyślij"]')


if __name__ == "__main__":
    print("module loaded as main")