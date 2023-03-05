from bs4 import BeautifulSoup
import requests
import re

session = requests.Session()
sessionTTL = 10


def refreshsession():
    global session, sessionTTL
    if sessionTTL == 0:
        session = requests.Session()
        sessionTTL = 10

    sessionTTL -= 1


def fetchdatafromgoogle(movie_name: str):
    refreshsession()

    url = f"https://www.google.com/search?q={movie_name}"
    html_result = session.get(url).text
    soup = BeautifulSoup(html_result, 'html.parser').body

    soups = soup.find_all("div", attrs={"class": "kCrYT"}, recursive=True)
    if len(soups) < 2:
        return ""

    textresult = ""
    headings = soups[0].get_text().split("‧")
    if len(headings) == 3:
        textresult = "‧".join(headings[1:]) + "\n"
    textresult += "\n" + soups[1].get_text().replace(' · ', '')

    textresult = re.sub("  +", "", textresult)
    return textresult.replace ('\n', '\n<br>\n')
    