import os

import config


def scan_items(base: str, folder_name: str, files_list: list[str]):
    f = open(config.save_to + r"\films.html", 'a', encoding="utf-8")
    for path in files_list:
        absolute_path = base + "/" + path
        if os.path.isfile(absolute_path) and not path.endswith(".lnk"):
            print(path)
            f.write(
                generate_html(normalize_filename(path), folder_name, path)
            )
        elif os.path.isdir(absolute_path):
            scan_items(absolute_path, os.path.basename(absolute_path), os.listdir(absolute_path))


def generate_html(path: str, folder_name: str, file_name: str):
    return '''<h2>{}</h2>
                {}<br>
                <a target=\"_blank\" href=\"https://www.google.com/search?q={}\">google</a><br>
                <a target=\"_blank\" href=\"https://www.google.com/search?q={}\">زیرنویس فارسی</a><br>
                <a target=\"_blank\" href=\"https://www.google.com/search?q={} subtitle\">زیرنویس انگلیسی</a><br>
                <svg height="10" width="1000">
                    <line x1="0" y1="0" x2="1000" y2="0" style="stroke:rgb(0, 0, 0);stroke-width:2" />
                </svg><br>'''.format(path + "[{}]".format(folder_name), file_name, path, path + "زیرنویس فارسی ", path)


def normalize_filename(name: str):
    split_start_index = 500
    for keyword in config.ignore_keywords:
        keyword_start_index = None
        if (keyword_start_index := name.lower().find(keyword)) != -1:
            split_start_index = min(keyword_start_index, split_start_index)

    return name[:split_start_index].replace(".", " ").replace("_", " ")


if os.path.exists(os.path.join(config.save_to, "films.html")):
    os.remove(os.path.join(config.save_to, "films.html"))
scan_items(config.library_dir, os.path.basename(config.library_dir), os.listdir(config.library_dir))
