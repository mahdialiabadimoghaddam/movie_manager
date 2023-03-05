import config

import os
import math
import threading
from fetch_scores import fetchdatafromgoogle

ignoredextensions = []

def scan_items(files_list: list[tuple]):
    for filename, path in files_list:
        normalized_filename = normalize_filename(filename)
        generated_html = generate_html(normalized_filename, path)
        writeHTML(generated_html)
        print("\n\n")


def generate_html(filename: str, path: str):
    if filename in cachedHTMLs:
        print("=== reding from cach ===")
        with open(f'htmls/{filename}', 'r', encoding='UTF-8') as htmlfile:
            return htmlfile.read()
    else:
        print("=== googling... ===")
        generated_html = config.HTML_BOX_TEMPLATE.format(
            filename, path, fetchdatafromgoogle(filename), filename, filename, filename
        )
        with open(f'htmls/{filename}', 'w', encoding='UTF-8') as htmlfile:
            htmlfile.write(generated_html)
        return generated_html


def normalize_filename(name: str):
    name = name.replace(".", " ").replace("-", " ").replace("_", " ").replace('(', '').replace(')', '').split(" ")

    for wordindex in range (len(name)):
        print(name[wordindex].lower())
        if name[wordindex].lower() in config.IGNORE_KEYWORDS:
            name = name[:wordindex]
            break

    return " ".join(name)

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


################################################ main() ################################################
def scaninparallel(allmovies):
    threadworkload = math.ceil(len(allmovies)/4)
    threads = [
        threading.Thread(target=scan_items, args=[allmovies[:threadworkload]]),
        threading.Thread(target=scan_items, args=[allmovies[threadworkload:threadworkload*2]]),
        threading.Thread(target=scan_items, args=[allmovies[threadworkload*2:threadworkload*3]]),
        threading.Thread(target=scan_items, args=[allmovies[threadworkload*3:len(allmovies)]])
    ]
    
    for singlethread in threads:
        singlethread.start()

    for singlethread in threads:
        singlethread.join()


cachedHTMLs = os.listdir('htmls')
writeHTML(config.HTML_FILE_TEMPLATE, 'w')
scaninparallel(listmovies(config.LIBRARY_DIR))

print(ignoredextensions)
