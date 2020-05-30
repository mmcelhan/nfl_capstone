import json
import os
import glob


f = open("lake_to_stage.json")
two_up = os.path.abspath(os.path.join(os.getcwd(),"../.."))

data = json.load(f)
source = data['source']
target = data['target']

source_dir = os.path.join(two_up, source)  # should work in both mac and windows
target_dir = os.path.join(two_up, target)
print(source_dir)
print(target_dir)
print(two_up)

for file in data['keep_files']

print(glob.glob(target_dir + "//*"))


