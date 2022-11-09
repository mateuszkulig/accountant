import requests
import json


class RecievedEmail(object):
    """one mail object"""
    def __init__(self, mess_id:int, sender:str, date:str, subject:str):
        self.id = mess_id
        self.sender = sender
        self.date = date
        self.subject = subject


class GazetaMailApi(object):
    """gazeta.pl mail api"""
    def __init__(self, cookies:dict):
        self.cookies = cookies
        self.headers = {
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

    def get_messages(self) -> list[RecievedEmail]:
        """get and parse all of recieved emails"""
        messages = []
        response = requests.get('https://poczta.gazeta.pl/webmailapi/mail/', cookies=self.cookies, headers=self.headers)
        json_response = json.loads(response.text)
        for mess in json_response:
            mess_id = mess["mid"]
            sender = mess["from"]
            date = mess["recieved_date"]
            subject = mess["subject"]
            messages.append(RecievedEmail(mess_id, sender, date, subject))
        return messages





