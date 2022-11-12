import requests
import json
from bs4 import BeautifulSoup


class GazetaMailApi(object):
    """gazeta.pl mail api"""
    HEADERS = {
        'authority': 'poczta.gazeta.pl',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    }
    cookies = {}

    def __init__(self, cookies:list[dict]):
        for cookie in cookies:
            self.__class__.cookies[cookie['name']] = cookie['value']

    def get_messages(self) -> list:
        """get and parse all of recieved emails"""
        messages = []
        response = requests.get('https://poczta.gazeta.pl/webmailapi/mail/', cookies=self.cookies, headers=self.HEADERS)
        json_response = json.loads(response.text)
        for mess in json_response:
            mess_id = mess["mid"]
            sender = mess["from"]
            date = mess["received_date"]
            subject = mess["subject"]
            messages.append(RecievedEmail(mess_id, sender, date, subject))
        return messages

    def find_message_by_topic(self, topic:str):
        """return recievedEmail object that matches subject propety with topic"""
        for mail in self.get_messages():
            if mail.subject == topic: return mail


class RecievedEmail(object):
    """one mail object"""
    def __init__(self, mess_id:int, sender:str, date:str, subject:str):
        self.id = mess_id
        self.sender = sender
        self.date = date
        self.subject = subject
        self.content_type = ""
        self.content = self.get_message_content()


    def get_message_content(self) -> str:
        """get message html content"""
        response = requests.get(f'https://poczta.gazeta.pl/webmailapi/mail/{self.id}', cookies=GazetaMailApi.cookies, headers=GazetaMailApi.HEADERS).text
        json_response = json.loads(response)
        if json_response["html"] != "":
            self.content_type = "html"
        else:
            self.content_type = "text"
        return json_response[self.content_type]

    def get_closest_href(self, pattern:str) -> str:
        """parse the content and search for best match for link"""
        if self.content_type == "text":
            start = self.content.find(pattern)
            end = self.content[start:].find(" ")
            return self.content[start:start+end]
        else:
            soup = BeautifulSoup(self.content, "html.parser")
            for a in soup.find_all('a', href=True):
                if a['href'][:len(pattern)] == pattern:
                    return a["href"]
            return ""