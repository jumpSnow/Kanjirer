import requests
from bs4 import BeautifulSoup
from utils.decorator import clean


class Wanikani:

    def __init__(self, *args):
        self._login_url = "https://www.wanikani.com/login"
        self._url = "https://www.wanikani.com/kanji/{}"
        self._keyword = args if args else None
        self._current = None
        self._page = None
        self._content = None
        self._cookie = None
        self._header = None
        self._token = None
        self._level = None

    @property
    def token(self):
        login_page = requests.get(self._login_url)
        soup = BeautifulSoup(login_page.content, "lxml")
        res = soup.find("meta", {"name": "csrf-token"})
        self._token = res.getText()
        return self._token

    @property
    def cookie(self):
        params = {"authenticity_token": self.token,
                  "utf8": "✓",
                  "user[login]": "w651467780@gmail.com",
                  "user[password]": "WMD19970211",
                  "user[remember_me]": 0
                  }
        session = requests.Session()
        res = session.get(self._login_url, params=params)
        cookie_dict = session.cookies.get_dict()
        self._cookie = "_wanikani_session=" + cookie_dict["_wanikani_session"]
        return self._cookie

    @property
    def header(self):
        self._header = {"Cookie": self.cookie, "X-CSRF-Token": self.token,
                        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
        return self._header

    @property
    @clean
    def level(self):
        url = self._url.format(self._current)
        word_page = requests.get(url=url)
        soup = BeautifulSoup(word_page.content, "lxml")
        res = soup.find("a", {"class", "level-icon"})
        self._level = res.getText()
        return self._level

    @property
    def data(self):
        for keyword in self._keyword:
            cell = dict()
            self._current = keyword
            cell.update({"kanji": self._current})
            cell.update({"level": self.level})
            yield cell


if __name__ == '__main__':
    test = Wanikani()


