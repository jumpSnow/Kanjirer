import pandas as pd
from web.jisho import Jisho
from web.wanikani import Wanikani
import time
from func.func import write_csv


def run(web, path, list_length):
    cur = 1
    for cell in web.data:
        print(str(int(cur/list_length * 100)) + '%', cell["kanji"])
        write_csv(cell, path)
        # print(cell)
        cur += 1
    end = time.time()


if __name__ == '__main__':
    content = pd.read_csv("./input_file/kanji_list.csv")
    kanji_list = content["kanji"]
    jisho = Jisho(*kanji_list)
    wanikani = Wanikani(*kanji_list)
    start = time.time()
    wanikani_path = "./result/wanikani_result.csv"
    run(web=wanikani, path=wanikani_path, list_length=len(kanji_list))
    end = time.time()
    print("time_cost", end - start)





