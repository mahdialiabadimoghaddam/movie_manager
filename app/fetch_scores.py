from bs4 import BeautifulSoup
import requests
import re

session = requests.Session()

def fetch_scores_html(movie_name: str):
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

    return textresult
