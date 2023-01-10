import os
from fetch_scores import fetch_scores_html

import config

ignoredextensions = []

def scan_items(files_list: list[tuple]):
    for filename, path in files_list:
        normalized_filename = normalize_filename(filename)
        generated_html = generate_html(normalized_filename, path)
        writeHTML(generated_html)
        print("\n\n")


def generate_html(filename: str, path: str):
    return config.HTML_BOX_TEMPLATE.format(
        filename, path, fetch_scores_html(filename), filename, filename, filename
    )


def normalize_filename(name: str):
    name = name.replace(".", " ").replace("-", " ").replace("_", " ").split(" ")

    for wordindex in range (len(name)):
        print(name[wordindex].lower())
        if name[wordindex].lower() in config.IGNORE_KEYWORDS:
            name = name[:wordindex]
            break

    return " ".join(name).replace('(', '').replace(')', '')

def listmovies(dir):
    r = []
    for root, _, files in os.walk(dir):
        for name in files:
            name, ext = os.path.splitext(name)
            ext = ext.lower()
            if ext in config.FILE_TYPES:
                r.append((name, os.path.join(root, name)))
            elif not ext in ignoredextensions:
                # global ignoredextensions
                ignoredextensions.append(ext)
    return r

def writeHTML(text, mode='a'):
    with open(f"{config.SAVE_TO}/films.html", mode, encoding="utf-8") as f:
        f.write(text)


writeHTML(config.HTML_FILE_TEMPLATE, 'w')
scan_items(listmovies(config.LIBRARY_DIR))

print(ignoredextensions)