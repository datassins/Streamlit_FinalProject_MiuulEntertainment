from bs4 import BeautifulSoup
import requests

import requests
from bs4 import BeautifulSoup

def get_image_from_imdb(imdb_id):
    url = f"https://www.imdb.com/title/{imdb_id}/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to retrieve page for {imdb_id}, Status Code: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.content, "html.parser")
    image_tag = soup.find("img", {"class": "ipc-image"})
    
    if image_tag is not None:
        return image_tag["src"]
    else:
        print(f"Image not found for {imdb_id}")
        return None


if __name__ == "__main__":
    pass
