import streamlit as st
from PIL import Image, UnidentifiedImageError
import base64
from io import BytesIO
import requests


st.set_page_config(layout= 'wide', page_title = 'Miuultainment',page_icon="🤖")

# PNG dosyasının yolu
image_path = '2.png'
# Görüntüyü yükle ve göster
image = Image.open(image_path)

######################################## HOME ANA BANNER BASLIK ########################################

st.markdown("""
    <style>
    .banner {
        position: relative;
        width: 100%;
        max-width: 100%;  # Maksimum genişlik olarak %100 ayarlandı
        overflow: hidden;  # Taşmayı gizlemek için eklendi
        border-radius: 10px;
        text-align: center;
        display: block;  # Blok olarak ayarlandı
        margin: 0 auto;  # Ortaya hizalama
    }
    .banner img {
        width: 100%;  # Genişliği %100 ayarlandı
        height: auto;
        border-radius: 10px;
    }
    .banner .text {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: #FFD700;  # Metin rengini beyaz olarak ayarlandı
        background-color: rgba(0, 0, 0, 0.5);  # Yarı saydam siyah bir arka plan
        padding: 20px;  # Dolgu miktarı artırıldı
        border-radius: 10px;  # Kenar yuvarlama eklendi
        text-align: center;  # Metin hizalaması ortalandı
    }
    .banner .text h1 {
        margin: 0;  # Başlık için varsayılan margin sıfırlandı
        font-size: 2em;  # Başlık boyutu ayarlandı
        color: #FFD700;  # Başlık rengini pastel sarı olarak ayarlandı
    }
    .banner .text p {
        margin-top: 10px;  # Paragraf üstüne boşluk eklendi
        font-size: 1.2em;  # Paragraf boyutu ayarlandı
    }
    </style>
    """, unsafe_allow_html=True)

def create_banner(banner_image_path, title, text):
    banner_html = f"""
    <div class="banner">
        <img src="data:image/png;base64,{banner_image_path}" />
        <div class="text">
            <h1>{title}</h1>
            <p>{text}</p>
        </div>
    </div>
    """
    st.markdown(banner_html, unsafe_allow_html=True)

def get_image_base64(image_path=None, image_url=None):
    try:
        if image_path:
            image = Image.open(image_path)
        else:
            if not image_url:
                raise ValueError("Invalid image URL provided.")
            response = requests.get(image_url)
            response.raise_for_status()  # Bu satır, istek başarısız olursa bir hata fırlatır
            image = Image.open(BytesIO(response.content))

        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return img_str
    except UnidentifiedImageError:
        st.error(f"Could not identify image from URL: {image_url}")
        return None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

######################################## marka banner ########################################

# Başlık ve içerik
title = "MIUUL ENTERTAINMENT"
text = ('At Miuultainment, we believe that every experience should be extraordinary. ' '<br>'
        'From beloved anime series and captivating films to adrenaline-pumping games, engrossing books, and perfect Airbnb options for unforgettable vacations, we have it all!'
        ' Our platform curates personalized recommendations based on your preferences, ensuring you find the perfect match every time.''<br>'
        'Experience new thrills with every discovery and add color to your life. ''<br>'
        'Are you ready to embark on this adventure filled with the best recommendations? ''<br>'
        'Start exploring now! 🚀 ')
# Tek resim dosyası veya URL
image_path = '2.png'  # Eğer dosya yolu kullanmak istiyorsanız buraya dosya yolunu girin
image_url = None  # Eğer URL kullanmak istiyorsanız buraya URL'yi girin

# Resmi base64 formatına dönüştürme
banner_img_str = get_image_base64(image_path=image_path, image_url=image_url)

# Banner oluşturma
if banner_img_str:
    create_banner(banner_img_str, title, text)
else:
    st.error("Banner resmi yüklenemedi.")

st.markdown("<br>", unsafe_allow_html=True)

######################################## home_tab yatay cizgi ########################################


# Daha kalın ve farklı renkte bir yatay çizgi
st.markdown(
    """
    <hr style="border: none; height: 2px; background-color: #FFD700;" />
    """,
    unsafe_allow_html=True
)

######################################## HOME ANA BANNER BASLIK_komple duzen ########################################

# URLs for the activity images
airbnb_image_url = "https://a0.muscache.com/im/pictures/8fa80ff2-07bf-4be3-94c2-fc7b52fb2006.jpg?im_w=1200"
movie_image_url = "https://www.themoviedb.org/t/p/w600_and_h900_bestv2/or06FN3Dka5tukK1e9sl16pB3iy.jpg"
book_image_url = "https://i.pinimg.com/564x/92/f6/15/92f6158366098335581d7e286d930bdb.jpg"
game_image_url = 'https://i.pinimg.com/originals/b4/37/91/b437916b126871403558fc35944d6981.jpg'
anime_image_url = 'https://cdn.myanimelist.net/images/anime/1764/109632l.jpg'

# Load images from URLs
def load_image(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

airbnb_image = load_image(airbnb_image_url)
movie_image = load_image(movie_image_url)
book_image = load_image(book_image_url)
game_image = load_image(game_image_url)
anime_image = load_image(anime_image_url)

# Custom CSS for buttons and images
custom_css = """
<style>
    .stButton > button {
        display: block;
        margin: 0 auto;
        width: 100%;
        padding: 10px 20px;
        font-size: 16px;
        color: #FFD700;
        background-color: #FFD700;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }
    .stButton > button:hover {
        background-color: #FFD700;
    }
    .activity-card {
        text-align: center;
    }
    .activity-card img {
        width: 500px;
        height: 570px;
        object-fit: cover;
        margin-bottom: 10px;
    }
</style>
"""

# Apply custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

import streamlit as st

# Create columns for the activity cards
col1, col2, col3, col4, col5 = st.columns(5)

def display_activity_card(column, image, title, description, url):
    with column:
        st.markdown(f"""
        <style>
        .activity-card h4 {{
            color: #FFD700; /* Rengi burada değiştirin */
            font-size: 24px; /* Boyutu burada değiştirin */
        }}
        </style>
        <div class='activity-card'>
            <img src='{image}' alt='{title}'>
            <h4>{title}</h4>
            <p>{description}</p>
            <a href='{url}'><button>Explore</button></a>
        </div>
        """, unsafe_allow_html=True)

# Example usage
display_activity_card(col1, airbnb_image_url, "Airbnb", "Find the best options to make your stay unforgettable.", "https://airbnbrecommendations.streamlit.app/")
display_activity_card(col2, movie_image_url, "Movie", "Enjoy a cinematic experience with our movie suggestions.", "https://miuulmovierecommender.streamlit.app/")
display_activity_card(col3, book_image_url, "Book", "Find the perfect read to captivate your mind and spirit.", "https://book-recomendations.streamlit.app/")
display_activity_card(col4, game_image_url, "Game", "Find the perfect game to keep you entertained for hours.", "https://gamerecommendations.streamlit.app/")
display_activity_card(col5, anime_image_url, "Anime", "Here to guide you to your next favorite anime series.", "https://animerecommendations.streamlit.app/")


st.markdown("<br>", unsafe_allow_html=True)
# Footer
# CSS stilini tanımlıyoruz
st.markdown(
    """
    <style>
    .centered-text {
        text-align: center;
        color: #FFD700; /* Rengi buradan değiştirebilirsiniz */
        font-size: 40px; /* Boyutu buradan değiştirebilirsiniz */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Stili kullanarak HTML içeriği ekliyoruz
st.markdown("<h3 class='centered-text'>Join us to discover!</h3>", unsafe_allow_html=True)
