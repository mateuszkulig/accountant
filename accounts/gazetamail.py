from acc import Browser
import random

class GazetaMailAcc(Browser):
    """Mail account for poczta.gazeta.pl"""
    def __init__(self, login:str, password:str):
        super(GazetaMailAcc, self).__init__(captcha=True, adblock=True)

        self.LOGIN = login.lower()
        self.PASSWORD = password
        self.MAIL = f"{self.LOGIN}@gazeta.pl"

    def register(self):
        """register an account"""
        self.get("https://konto.gazeta.pl/konto/rejestracja.do")

        # cookies popup
        self.wait_n_click('//span[@tabindex="0"][@style="display: block; font-weight: 600; padding: 12px 36px; text-align: center"]')

        el_input_login = self.wait_for_element('//input[@id="login"]')
        el_input_password = self.wait_for_element('//input[@id="pass"]')
        el_inputs_birthday = (self.wait_for_element('//input[@type="text"][@id="date-input-day"]'),
                              self.wait_for_element('//input[@type="text"][@id="date-input-month"]'),
                              self.wait_for_element('//input[@type="text"][@id="date-input-year"]'))

        el_input_login.send_keys(self.LOGIN)
        el_input_password.send_keys(self.PASSWORD)

        DAY, MONTH, YEAR = self.generate_date()
        el_inputs_birthday[0].send_keys(DAY)
        el_inputs_birthday[1].send_keys(MONTH)
        el_inputs_birthday[2].send_keys(YEAR)

        # checkboxes
        self.wait_n_click('//input[@id="sex2"]')
        self.wait_n_click('//input[@id="acceptEmailAccountTerms"]')

        self.wait_for_captcha()
        # create account button
        self.wait_n_click('//input[@type="submit"][@class="accountRegister__btn"][@value="Zakładam konto"]')

        self.get("about:blank")

    def log_in(self):
        """log into email account"""
        self.get("https://oauth.gazeta.pl/poczta/auth")

        self.wait_n_click('//button[@id="onetrust-accept-btn-handler"]')    # cookies popup

        el_input_login = self.wait_for_element('//input[@type="text"][@name="username"][@class="t"][@id="username"][@data-lowercase="true"][@value=""]')
        el_input_password = self.wait_for_element('//input[@type="password"][@name="password"][@class="t"][@id="password"]')

        el_input_login.send_keys(self.LOGIN)
        el_input_password.send_keys(self.PASSWORD)

        # doubleclick is required for gazeta to understand input
        for _ in range(2): self.wait_n_click('//input[@type="submit"][@id="mainSubmitLink"][@value="Zaloguj się"][@class="submit-button"]')    # log in button

    @staticmethod
    def generate_date():
        """generate the date of birth above 18yo"""
        DAY = random.randint(1, 28) # avoid the february buisness
        MONTH = random.randint(1, 12)
        YEAR = random.randint(1980, 2000)
        return DAY, MONTH, YEAR

    def __str__(self):
        return "gazeta.pl mail account"


if __name__ == "__main__":
    print("module loaded as main")
