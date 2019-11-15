import requests
from bs4 import BeautifulSoup
from utils.decorator import clean
import re
import asyncio


class Jisho:

    def __init__(self, *args):
        self._jisho_url = "https://jisho.org/search/{}%20%23kanji"
        self._keyword = args if args else None
        self._current = None
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
    def current(self):
        return self._current

    @property
    @clean
    def strokes(self) -> str:
        res = self._soup.find("div", {"class": "kanji-details__stroke_count"})
        self._strokes = re.search(r'(\d+)', res.getText()).group(1)
        return self._strokes

    @property
    @clean
    def frequency(self) -> str:
        res = self._soup.find("div", {"class": "frequency"})
        self._frequency = re.search(r'(\d+)', res.getText()).group(1)
        return self._frequency

    @property
    @clean
    def grade(self) -> str:
        res = self._soup.find("div", {"class": "grade"})
        self._grade = re.search(r'taught in (.*)', res.getText()).group(1)
        return self._grade

    @property
    @clean
    def jlpt(self) -> str:
        res = self._soup.find("div", {"class": "jlpt"})
        self._jlpt = re.search(r'JLPT level (.*)', res.getText()).group(1)
        return self._jlpt

    @property
    @clean
    def parts(self) -> dict:
        parent = self._soup.findAll("dl", {"class": "dictionary_entry on_yomi"})[1]
        child = parent.findChildren("a")
        self._parts = {s.getText(): "http://{}".format(s.get("href")) for s in child}
        return self._parts

    @property
    @clean
    def radicals(self) -> dict:
        parent = self._soup.findAll("dl", {"class": "dictionary_entry on_yomi"})[0]
        child = parent.findChildren("span")
        self._radicals = {child[0].getText().replace(child[1].getText(), ""):  child[1].getText()}
        return self._radicals

    @property
    @clean
    def on_readings(self) -> dict:
        parent = self._soup.findAll("dd", {"class": "kanji-details__main-readings-list"})[1]
        child = parent.findChildren("a")
        self._on_readings = {s.getText(): "http://{}".format(s.get("href")) for s in child}
        return self._on_readings

    @property
    @clean
    def kun_readings(self) -> dict:  # todo: integrate kun_readings with on_readings
        parent = self._soup.findAll("dd", {"class": "kanji-details__main-readings-list"})[0]
        child = parent.findChildren("a")
        self._on_readings = {s.getText(): "http://{}".format(s.get("href")) for s in child}
        return self._on_readings

    @property
    @clean
    def on_readings_compounds(self) -> list:  # todo: integrate on_readings_compounds with kun_readings_compounds
        parent = self._soup.find("div", {"class": "row compounds"})
        child = parent.findChildren("div", {"class": "small-12 large-6 columns"})[0]
        res = child.findChildren("li")
        self._on_readings_compounds = [s.getText() for s in res]
        return self._on_readings_compounds

    @property
    @clean
    def kun_readings_compounds(self) -> list:
        parent = self._soup.find("div", {"class": "row compounds"})
        child = parent.findChildren("div", {"class": "small-12 large-6 columns"})[1]
        res = child.findChildren("li")
        self._on_readings_compounds = [s.getText() for s in res]
        return self._on_readings_compounds

    @property
    def data(self):
        for keyword in self._keyword:
            self._current = keyword
            url = self._jisho_url.format(keyword)
            self._page = requests.get(url)
            self._soup = BeautifulSoup(self._page.content, 'lxml')
            cell = dict()
            cell.update({"kanji": self.current})
            cell.update({"strokes": self.strokes})
            cell.update({"frequency": self.frequency})
            cell.update({"grade": self.grade})
            cell.update({"jlpt": self.jlpt})
            cell.update({"parts": self.parts})
            cell.update({"radicals": self.radicals})
            cell.update({"on_readings": self.on_readings})
            cell.update({"kun_readings": self.kun_readings})
            cell.update({"on_readings_compounds": self.on_readings_compounds})
            cell.update({"kun_readings_compounds": self.kun_readings_compounds})
            yield cell


