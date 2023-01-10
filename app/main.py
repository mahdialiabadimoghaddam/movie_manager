import os
from fetch_scores import fetch_scores_html

import config


def scan_items(base: str, folder_name: str, files_list: list[str]):
    for path in files_list:
        absolute_path = base + "/" + path
        if os.path.isfile(absolute_path) and not path.endswith(".lnk"):
            print(path)

            with open(os.path.join(config.SAVE_TO, "films.html"), 'a', encoding="utf-8") as file:
                file.write(
                    generate_html(normalize_filename(path), folder_name, path)
                )
        elif os.path.isdir(absolute_path):
            scan_items(absolute_path, os.path.basename(absolute_path), os.listdir(absolute_path))


def generate_html(path: str, folder_name: str, file_name: str):
    return config.HTML_BOX_TEMPLATE.format(
        folder_name + "/ " + path, file_name, fetch_scores_html(path), path, path, path
    )


def normalize_filename(name: str):
    name = name.replace(".", " ").replace("-", " ").replace("_", " ").split(" ")

    for wordindex in range (len(name)):
        print(name[wordindex].lower())
        if name[wordindex].lower() in config.IGNORE_KEYWORDS:
            name = name[:wordindex]
            break

    return " ".join(name).replace('(', '').replace(')', '')


with open(os.path.join(config.SAVE_TO, "films.html"), 'w', encoding="utf-8") as f:
    f.write(config.HTML_FILE_TEMPLATE)

scan_items(config.LIBRARY_DIR, os.path.basename(config.LIBRARY_DIR), os.listdir(config.LIBRARY_DIR))

