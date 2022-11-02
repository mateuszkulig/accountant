from acc import Browser
import time
from selenium.webdriver.common.by import By

class Mail(Browser):
    """10minutemail.net control"""
    def __init__(self):
        super(Mail, self).__init__(adblock=True)
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