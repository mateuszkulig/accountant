import requests

class SteamApi(object):
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