import os

import config


def scan_items(base: str, files_list: list[str]):
    f = open("films.html", "a", encoding="utf-8")
    for path in files_list:
        absolute_path = base + "/" + path
        if os.path.isfile(absolute_path) and not path.endswith(".lnk"):
            # print(path)
            path = normalize_filename(path)
            print(path)
            f.write(
                "<p>{}</p>".format(path) +
                "<a target=\"_blank\" href=\"https://www.google.com/search?q={}\">google</a><br>".format(path) +
                "<a target=\"_blank\" href=\"https://www.google.com/search?q={}\">زیرنویس فارسی</a><br>\r\n".format(path + "زیرنویس فارسی ") +
                "<a target=\"_blank\" href=\"https://www.google.com/search?q={} subtitle\">زیرنویس انگلیسی</a><br>\r\n".format(path)
            )
        elif os.path.isdir(absolute_path):
            scan_items(absolute_path, os.listdir(absolute_path))

def normalize_filename(name: str):
    split_start_index = 500
    for keyword in config.ignore_keywords:
        keyword_start_index = None
        if (keyword_start_index := name.lower().find(keyword)) != -1:
            split_start_index = min(keyword_start_index, split_start_index)

    return name[:split_start_index].replace(".", " ").replace("_", " ")


scan_items(config.library_dir, os.listdir(config.library_dir))
