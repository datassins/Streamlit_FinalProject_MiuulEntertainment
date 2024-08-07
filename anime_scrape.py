import requests
from bs4 import BeautifulSoup
import streamlit as st


######################################## anime image scraping ########################################
def get_anime_image(mal_id):
    URL = f'https://myanimelist.net/anime/{mal_id}'
    response = requests.get(URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        image_tag = soup.find('img', {'itemprop': 'image'})
        if image_tag:
            return image_tag['data-src']
    return None


def main():
    st.title('Anime Görseli')

    mal_id = st.text_input('MAL ID girin:', '')

    if mal_id:
        image_url = get_anime_image(mal_id)

        if image_url:
            st.image(image_url)
        else:
            st.write("Görsel bulunamadı.")

    # Örnek olarak önceden tanımlı birkaç MAL ID
    example_ids = ['1', '5114', '40028']
    st.write("Örnek MAL ID'ler:")
    for example_id in example_ids:
        if st.button(f"Show image for MAL ID {example_id}"):
            image_url = get_anime_image(example_id)
            if image_url:
                st.image(image_url)
            else:
                st.write(f"Görsel bulunamadı. MAL ID: {example_id}")


if __name__ == "__main__":
    main()