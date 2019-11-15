import pandas as pd
from Jisho.jisho import Jisho
import time
from func.func import write_csv

content = pd.read_csv("./input_file/kanji_list.csv")
kanji_list = content["kanji"]
test = Jisho(*kanji_list)

start = time.time()
cur = 1
all = len(kanji_list)
for cell in test.data:
    print(str(int(cur/all * 100)) + '%', cell["kanji"])
    write_csv(cell)
    cur += 1
end = time.time()
print("time_cost", end - start)



