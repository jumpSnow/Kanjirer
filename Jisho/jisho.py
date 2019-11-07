import requests
from bs4 import BeautifulSoup
from utils.decorator import clean


class Jisho:

    def __init__(self, *args):
        self._jisho_url = "https://jisho.org/search/{}%20%23kanji"
        self._keyword = args if args else None
        self._page = None
        self._content = None
        self._soup = None
        self._strokes = None
        self._on_readings_compounds = None
        self._kun_readings_compounds = None
        self._on_readings = None
        self._kun_readings = None
        self._radicals = None
        self._parts = None
        self._grade = None
        self._jlpt = None
        self._frequency = None

    @property
    @clean
    def strokes(self):
        res = self._soup.find("div", {"class": "kanji-details__stroke_count"})
        self._strokes = res.getText()
        return self._strokes

    @property
    @clean
    def kun_readings(self):
        parent = self._soup.find("div", {"class": "kanji-details__main-readings"})
        res = parent.findChildren("dd", {"class": "kanji-details__main-readings-list"})
        self._kun_readings = res[0].getText()
        return self._kun_readings

    @property
    @clean
    def on_readings(self):
        parent = self._soup.find("div", {"class": "kanji-details__main-readings"})
        res = parent.findChildren("dd", {"class": "kanji-details__main-readings-list"})
        self._on_readings = res[1].getText()
        return self._on_readings

    @property
    @clean
    def on_readings_compounds(self):
        parent = self._soup.find("div", {"class": "row compounds"})
        res = parent.findChildren("div", {"class": "small-12 large-6 columns"})
        self._on_readings_compounds = res[0].getText().split("\n\n\n")
        return self._on_readings_compounds

    @property
    @clean
    def kun_readings_compounds(self):
        parent = self._soup.find("div", {"class": "row compounds"})
        res = parent.findChildren("div", {"class": "small-12 large-6 columns"})
        self._kun_readings_compounds = res[1].getText().split("\n\n\n")
        return self._kun_readings_compounds

    @property
    @clean
    def radicals(self):
        res = self._soup.findAll("dl", {"class": "dictionary_entry on_yomi"})[0]
        self._radicals = res.getText()
        return self._radicals

    @property
    @clean
    def parts(self):
        res = self._soup.findAll("dl", {"class": "dictionary_entry on_yomi"})[1]
        self._parts = res.getText()
        return self._parts

    @property
    @clean
    def grade(self):
        res = self._soup.find("div", {"class": "grade"})
        self._grade = res.getText()
        return self._grade

    @property
    @clean
    def jlpt(self):
        res = self._soup.find("div", {"class": "jlpt"})
        self._jlpt = res.getText()
        return self._jlpt

    @property
    @clean
    def frequency(self):
        res = self._soup.find("div", {"class": "frequency"})
        self._frequency = res.getText()
        return self._frequency

    @property
    def data(self):
        for keyword in self._keyword:
            url = self._jisho_url.format(keyword)
            self._page = requests.get(url)
            self._soup = BeautifulSoup(self._page.content, 'lxml')
            yield self.strokes, self.frequency, self.grade, self.jlpt, self.parts, self.radicals, self.on_readings,\
                  self.kun_readings, self.on_readings_compounds, self.kun_readings_compounds


if __name__ == '__main__':
    test = Jisho("男")
    # print(test.on_readings_compounds)
    for i in test.data:
        print(i)
