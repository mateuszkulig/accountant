from acc import Browser, Mail
import time
import fng_api
import requests

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

        # todo: temporary solution before rewriting steamapi to static class
        s = SteamApi()
        tradelink = "https://steamcommunity.com/tradeoffer/new/?partner=1424493025&token=" + s.new_tradelink()
        del s

        linkarea.send_keys(tradelink)
        self.wait_n_click('//input[@value="Wyślij"]')

class SteamApi(object): # todo: rewrite to static class
    """steam api to change the tradelink"""
    def __init__(self):
        self.cookies = {
            'browserid': '2391972979052299443',
            'steamMachineAuth76561198261851808': '9B45AD2A3A2AB248E6A76826DD8800F18830596C',
            'timezoneOffset': '7200,0',
            '_ga': 'GA1.2.1559007108.1656681720',
            'recentlyVisitedAppHubs': '730',
            'Steam_Language': 'polish',
            'sessionid': 'bc7255e87152f393f2a1f08e',
            'steamCountry': 'PL%7C2f524e73f2ec195cf92e98459c9c4672',
            'steamLoginSecure': '76561199384758753%7C%7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MEJEN18yMTM4OTk3M185MjI2NSIsICJzdWIiOiAiNzY1NjExOTkzODQ3NTg3NTMiLCAiYXVkIjogWyAid2ViIiBdLCAiZXhwIjogMTY2NjY1NTA5OCwgIm5iZiI6IDE2NTc5MjcwODksICJpYXQiOiAxNjY2NTY3MDg5LCAianRpIjogIjBDMEVfMjE3OEQ2QzhfNkNFNkYiLCAib2F0IjogMTY2MjMyNTEzOCwgInJ0X2V4cCI6IDE2ODAyODgzMzAsICJwZXIiOiAwLCAiaXBfc3ViamVjdCI6ICIzNy40Ny44My4xNjAiLCAiaXBfY29uZmlybWVyIjogIjM3LjQ3LjgzLjE2MCIgfQ.HmBKOZ2JP00fVxhIgy8OlbOgMCYKuRYx6nXbtAtbbgb_oEgjxOlmsP6fuoW69vFsHYXowWHrZlsRA018Q5ekAA',
            '_gid': 'GA1.2.1110810460.1666567090',
            'webTradeEligibility': '%7B%22allowed%22%3A0%2C%22reason%22%3A17448%2C%22allowed_at_time%22%3A1667173442%2C%22steamguard_required_days%22%3A15%2C%22new_device_cooldown_days%22%3A7%2C%22expiration%22%3A1666568942%2C%22time_checked%22%3A1666568642%7D',
            'tsTradeOffersLastRead': '1',
        }

        self.headers = {
            'Accept': '*/*',
            'Accept-Language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # Requests sorts cookies= alphabetically
            # 'Cookie': 'browserid=2391972979052299443; steamMachineAuth76561198261851808=9B45AD2A3A2AB248E6A76826DD8800F18830596C; timezoneOffset=7200,0; _ga=GA1.2.1559007108.1656681720; recentlyVisitedAppHubs=730; Steam_Language=polish; sessionid=bc7255e87152f393f2a1f08e; steamCountry=PL%7C2f524e73f2ec195cf92e98459c9c4672; steamLoginSecure=76561199384758753%7C%7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MEJEN18yMTM4OTk3M185MjI2NSIsICJzdWIiOiAiNzY1NjExOTkzODQ3NTg3NTMiLCAiYXVkIjogWyAid2ViIiBdLCAiZXhwIjogMTY2NjY1NTA5OCwgIm5iZiI6IDE2NTc5MjcwODksICJpYXQiOiAxNjY2NTY3MDg5LCAianRpIjogIjBDMEVfMjE3OEQ2QzhfNkNFNkYiLCAib2F0IjogMTY2MjMyNTEzOCwgInJ0X2V4cCI6IDE2ODAyODgzMzAsICJwZXIiOiAwLCAiaXBfc3ViamVjdCI6ICIzNy40Ny44My4xNjAiLCAiaXBfY29uZmlybWVyIjogIjM3LjQ3LjgzLjE2MCIgfQ.HmBKOZ2JP00fVxhIgy8OlbOgMCYKuRYx6nXbtAtbbgb_oEgjxOlmsP6fuoW69vFsHYXowWHrZlsRA018Q5ekAA; _gid=GA1.2.1110810460.1666567090; webTradeEligibility=%7B%22allowed%22%3A0%2C%22reason%22%3A17448%2C%22allowed_at_time%22%3A1667173442%2C%22steamguard_required_days%22%3A15%2C%22new_device_cooldown_days%22%3A7%2C%22expiration%22%3A1666568942%2C%22time_checked%22%3A1666568642%7D; tsTradeOffersLastRead=1',
            'Origin': 'https://steamcommunity.com',
            'Referer': 'https://steamcommunity.com/profiles/76561199384758753/tradeoffers/privacy',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        self.data = {
            'sessionid': 'bc7255e87152f393f2a1f08e',
        }

    def new_tradelink(self) -> str:
        response = requests.post("https://steamcommunity.com/profiles/76561199384758753/tradeoffers/newtradeurl", cookies=self.cookies, headers=self.headers, data=self.data)
        return response.text


if __name__ == "__main__":
    print("module loaded as main")