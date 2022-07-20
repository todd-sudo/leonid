import json
import os


def save_data_username_in_file_bird(data: dict, username: str):
    root_path = "src/data/bird/"
    with open(f"{root_path}{username}.json", "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def delete_all_files_in_folder_bird():
    root_path = "src/data/bird/"
    files_in_folder = os.listdir(root_path)
    if files_in_folder:
        for file in files_in_folder:
            os.remove(f"{root_path}{file}")


def get_data_in_file_bird():
    data = None
    root_path = "src/data/bird/"
    files_in_folder = os.listdir(root_path)
    if files_in_folder:
        filename = files_in_folder[0]
        with open(root_path + filename, "r") as f:
            data = json.load(f)
            return data
    else:
        return data
