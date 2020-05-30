import json
import os
import shutil


def make_folder_if_not_exists(path):
    """ creates a folder if it doesn't exist already """
    if not os.path.exists(path):
        os.makedirs(path)


def main():
    local_path = os.path.dirname(os.path.abspath(__file__))
    f = open(os.path.join(local_path, "lake_to_stage.json"))
    two_up = os.path.abspath(os.path.join(local_path, "../.."))

    data = json.load(f)
    source_dir = os.path.join(two_up, data['source'])  # should work in both mac and windows
    target_dir = os.path.join(two_up, data['target'])

    for file in data['keep_files']:
        source = os.path.join(source_dir, file['folder'], file['file'])
        target_folder = os.path.join(target_dir, file['folder'] + data["target_suffix"])
        target = os.path.join(target_folder, file['file'])
        make_folder_if_not_exists(target_folder)
        shutil.copyfile(source, target)


main()