import os
from fetch_scores import fetch_scores_html

import config


def scan_items(base: str, folder_name: str, files_list: list[str]):
    for path in files_list:
        absolute_path = base + "/" + path
        if os.path.isfile(absolute_path) and not path.endswith(".lnk"):
            print(path)

            with open(os.path.join(config.save_to, "films.html"), 'a', encoding="utf-8") as file:
                file.write(
                    generate_html(normalize_filename(path), folder_name, path)
                )
        elif os.path.isdir(absolute_path):
            scan_items(absolute_path, os.path.basename(absolute_path), os.listdir(absolute_path))


def generate_html(path: str, folder_name: str, file_name: str):
    return '''
<div class="container">
    <h1>{}</h1>
    <div class="innerContainer">
        <p>{}</p>
        <p>{}</p>
        <a target=\"_blank\" href=\"https://www.google.com/search?q={}\">google</a>
        <i class="material-icons" style="font-size: 18px;" >search</i>
        <br>
        <a target=\"_blank\" href=\"https://www.google.com/search?q={}\">زیرنویس فارسی</a>
        <i class="material-icons" style="font-size: 18px;" >subtitles</i>
        <br>
        <a target=\"_blank\" href=\"https://www.google.com/search?q={} subtitle\">زیرنویس انگلیسی</a>
        <i class="material-icons" style="font-size: 18px;" >subtitles</i>
        <br>
    </div>
</div>'''.format(
        folder_name + "/ " + path, file_name, fetch_scores_html(path), path, path + "زیرنویس فارسی ", path
    )


def normalize_filename(name: str):
    name = name.replace(".", " ").replace("-", " ").replace("_", " ").split(" ")

    for wordindex in range (len(name)):
        print(name[wordindex].lower())
        if name[wordindex].lower() in config.ignore_keywords:
            name = name[:wordindex]
            break

    return " ".join(name).replace('(', '').replace(')', '')


with open(os.path.join(config.save_to, "films.html"), 'w', encoding="utf-8") as f:
    f.write('''
<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
<style>
    *{font-family: 'Tahoma', monospace;}
    .container{
        padding-left: 50px;
        padding-bottom: 20px;
        padding-top: 10px;
        border: 1px solid;
        border-radius: 25px;
        margin-left: 10px;
        margin-right: 300px;
    }
    .innerContainer {}
    a {
        text-decoration:none;
        font-size: 1rem;
    }
    a:visited {
        color: blue;
    }
</style>
''')

scan_items(config.library_dir, os.path.basename(config.library_dir), os.listdir(config.library_dir))

