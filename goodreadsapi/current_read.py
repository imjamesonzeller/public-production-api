import requests
from bs4 import BeautifulSoup

def get_current_read() -> str:
    url = 'https://www.goodreads.com/jamesonzeller'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html_content = response.content

        soup = BeautifulSoup(html_content, "html.parser")
        meta_tag = soup.find('meta', {'name': 'description'})

        if meta_tag and 'content' in meta_tag.attrs:
            content = meta_tag['content']
            return content
    else:
        print("Failed to retrieve the webpage:", response.status_code)

def parse_string(cr: str) -> str:
    try: 
        to_return = cr.split("currently reading")[1].strip()
    except IndexError: 
        to_return = "Tuesdays with Morrie by Mitch Album"

    return to_return

class CurrentRead():
    def __init__(self):
        self.attrs = parse_string(get_current_read())