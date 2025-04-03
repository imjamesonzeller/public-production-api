import requests
from bs4 import BeautifulSoup

class CurrentRead():
    def __init__(self):
        current_read: str = self._get_current_read()
        self.attrs: str = self._parse_title_and_author(current_read)

    def _parse_title_and_author(self, cr: str) -> str:
        try: 
            title_and_author = cr.split("currently reading")[1].strip()
        except IndexError: 
            # If fails, return some plaseholder
            title_and_author = "Tuesdays with Morrie by Mitch Album"

        return title_and_author
    
    def _get_current_read(self) -> str:
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
            
            # Return some placeholder text
            return "Jameson is currently reading Tuesdays with Morrie by Mitch Album"
        