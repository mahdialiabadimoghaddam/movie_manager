from bs4 import BeautifulSoup
import requests

session = requests.Session()

def fetch_scores_html(movie_name: str):
    url = f"https://www.google.com/search?q={movie_name}"
    html_result = session.get(url).text
    soup = BeautifulSoup(html_result, 'html.parser').find('div', attrs={'class': 'Ap5OSd'}, recursive=True)
    return soup.get_text().replace("\n", "\n<br>") if not soup==None else ""
