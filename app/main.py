import os

import config


def scan_items(base: str, folder_name: str, files_list: list[str]):
    for path in files_list:
        absolute_path = base + "/" + path
        if os.path.isfile(absolute_path) and not path.endswith(".lnk"):
            print(path)

            file = open(config.save_to + r"\films.html", 'a', encoding="utf-8")
            file.write(
                generate_html(normalize_filename(path), folder_name, path)
            )
            file.close()
        elif os.path.isdir(absolute_path):
            scan_items(absolute_path, os.path.basename(absolute_path), os.listdir(absolute_path))


def generate_html(path: str, folder_name: str, file_name: str):
    return '''
<div class="container">
    <h1>{}</h1>
    <div class="innerContainer">
        <p>{}</p>
        <br>
        <a target=\"_blank\" href=\"https://www.google.com/search?q={}\">google</a>
        <i class="material-icons" style="font-size: 18px;" >download</i>
        <br>
        <a target=\"_blank\" href=\"https://www.google.com/search?q={}\">زیرنویس فارسی</a>
        <i class="material-icons" style="font-size: 18px;" >download</i>
        <br>
        <a target=\"_blank\" href=\"https://www.google.com/search?q={} subtitle\">زیرنویس انگلیسی</a>
        <i class="material-icons" style="font-size: 18px;" >download</i>
        <br>
    </div>
</div>'''.format(
        path + "[{}]".format(folder_name), file_name, path, path + "زیرنویس فارسی ", path
    )


def normalize_filename(name: str):
    split_start_index = 500
    for keyword in config.ignore_keywords:
        if (keyword_start_index := name.lower().find(keyword)) != -1:
            split_start_index = min(keyword_start_index, split_start_index)

    return name[:split_start_index].replace(".", " ").replace("_", " ")


f = open(config.save_to + r"\films.html", 'w', encoding="utf-8")
f.write('''
<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
<style>
    *{font-family: 'Times New Roman', monospace;}
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
f.close()

scan_items(config.library_dir, os.path.basename(config.library_dir), os.listdir(config.library_dir))

