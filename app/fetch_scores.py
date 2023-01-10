import os
from bs4 import BeautifulSoup
import requests
import re

session = requests.Session()
files = os.listdir('htmls')

def fetchdatafromgoogle(movie_name: str):
    if movie_name in files:
        with open(os.path.join('htmls', movie_name), 'r', encoding='UTF-8') as htmlfile:
            return htmlfile.read()

    url = f"https://www.google.com/search?q={movie_name}"
    html_result = session.get(url).text
    soup = BeautifulSoup(html_result, 'html.parser').body

    soups = soup.find_all("div", attrs={"class": "kCrYT"}, recursive=True)
    if len(soups) < 2:
        return ""

    headings = soups[0].get_text().split("‧")
    textresult = ""
    if len(headings) == 3:
        textresult = "‧".join(headings[1:]) + "\n"
    textresult += soups[1].get_text()

    textresult = re.sub("  +", "", textresult)
    textresult = "".join([line.strip()+"\n<br>\n" for line in textresult.split("\n") if not line==''])
    
    with open(os.path.join('htmls', movie_name), 'w', encoding='UTF-8') as htmlfile:
        htmlfile.write(textresult)
    
    return textresult
