import csv
import os


def write_csv(cell):
    csv_file = "./result/jisho_result.csv"
    csv_columns = cell.keys()
    if_csv_exists = os.path.exists(csv_file)
    with open(csv_file, 'a+') as f:
        writer = csv.DictWriter(f, fieldnames=csv_columns)
        if not if_csv_exists:
            writer.writeheader()
        writer.writerow(cell)
