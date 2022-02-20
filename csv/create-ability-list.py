import os
import glob
import pandas as pd
from csv import reader

sln_dir = "C:/Users/ryanw/Documents/GitHub/rotation-helper/csv"
in_dir = f"{sln_dir}/in"
out_dir = f"{sln_dir}/out"
filename = "combined"
extension = 'csv'

os.chdir(in_dir)
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
combined_csv.drop('Unnamed: 2', inplace=True, axis=1)
combined_csv.to_csv( f"{out_dir}/{filename}.csv", index=False, encoding='utf-8-sig')

actions = []

matches = ["prepare", "attack", "Tick"]
seperator = "Erichthonios"

with open(f"{out_dir}/{filename}.csv", 'r') as read_obj:
    csv_reader = reader(read_obj)
    header = next(csv_reader)
    for row in csv_reader:
        if any(x in row[1] for x in matches):
            pass
        else:
            text = row[1]
            stripped = text.split(seperator, 1)[0]
            stripped2 = stripped.replace("Lemme At'em ", '')
            actions.append(stripped2)

with open(f"{out_dir}/ability-list.txt", 'w') as f:
    f.write('\n'.join(actions))