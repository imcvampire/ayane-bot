import requests


BILAC = 'https://bilac.theanht1.me/api/v2'


def member_info(mem):
    return "%s: %s" % (mem['username'], mem['elo'])


class Bilac:
    def __init__(self, url=BILAC):
        self.url = url

    def elo(self):
        r = requests.get("%s/members?sort=-elo" % self.url)
        res= r.json()
        return map(member_info, res)
