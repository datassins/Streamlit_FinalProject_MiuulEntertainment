######################################## import data ########################################

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from anime_scrape import get_anime_image
import xgboost as xgb

######################################## home_tab information ########################################

st.set_page_config(layout= 'wide', page_title = ' Anime Recommender', page_icon="🍜")

######################################## read_csv########################################
@st.cache_data
def get_data():
    df = pd.read_csv('anime_filtered.csv')
    return df

anime_data = get_data()

######################################## read_csv########################################
# st.cache_data
@st.cache_data
def get_data():
    df = pd.read_csv('rating_complete_filtered.csv')
    return df

rating_complete_data = get_data()

######################################## anime model base recommendation hazirlik ########################################
# Özellikler ve hedef değişkeni ayırma
@st.cache_data
def model_calculate(dataframe):
    X = dataframe[['user_id', 'anime_id']]
    y = dataframe['rating']
    # XGBoost modelini oluşturma ve eğitme
    model_final = xgb.XGBRegressor(objective='reg:squarederror', random_state=42)
    model_final.fit(X, y)
    return model_final

model_final = model_calculate(rating_complete_data)

######################################## anime model base recommendation fonksiyon ########################################
def get_svd_recommendations_anime(user_id, n_recommendations=5):
    # Kullanıcının puanladığı anime'leri al
    user_ratings = rating_complete_data[rating_complete_data['user_id'] == user_id]
    anime_ids = user_ratings['anime_id'].tolist()

    # Tüm anime id'lerini al
    all_anime_ids = anime_data['MAL_ID'].tolist()

    recommendations = []

    # Tüm anime id'leri üzerinden geç ve kullanıcıya tahmin edilen puanı hesapla
    for anime_id in all_anime_ids:
        if anime_id not in anime_ids:
            # Tahmin yapmak için uygun veri yapısını oluştur
            pred = model_final.predict([[user_id, anime_id]])
            clipped_predictions = np.clip(pred, 1, 10)  # Ölçeklendirme burada yapılır
            recommendations.append((anime_id, clipped_predictions[0]))

    # Tahmin edilen puanlara göre sıralama yap
    recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)[:n_recommendations]

    # Önerilen anime id'leri ve puanları ayır
    recommended_anime_ids = [r[0] for r in recommendations]
    recommended_ratings = [r[1] for r in recommendations]

    # Önerilen anime bilgilerini al ve tahmin edilen puanı ekle
    recommended_animes = anime_data[anime_data['MAL_ID'].isin(recommended_anime_ids)][
        ['MAL_ID', 'Name']]
    recommended_animes['Predicted_Rating'] = recommended_ratings

    return recommended_animes[['MAL_ID', 'Name', 'Predicted_Rating']]


 ######################################## ANIME CONTENT BASED RECOMMENDATION########################################
@st.cache_data
def calculate_cosine_sim(dataframe):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(dataframe['Features'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cosine_sim


cosine_sim = calculate_cosine_sim(anime_data)

def content_based_recommender_anime(anime_name, cosine_sim, dataframe):
    # Anime isimlerinden oluşan indeks serisi oluştur
    indices = pd.Series(dataframe.index, index=dataframe['Name'])
    # Yinelenen indeksleri kaldır
    indices = indices[~indices.index.duplicated(keep='last')]
    # Anime isminin indeksini bul
    anime_index = indices[anime_name]
    # Kosinüs benzerlik skorlarını al
    sim_scores = pd.DataFrame(cosine_sim[anime_index], columns=['score'])
    # Benzerlik skorlarına göre sıralama ve ilk 10 öneri (ilk eleman kendisi olduğundan hariç)
    anime_indices = sim_scores.sort_values('score', ascending=False).index[1:8]
    # Önerilen anime isimlerini döndür
    last_df = dataframe[['MAL_ID','Name','Score']].iloc[anime_indices].sort_values('Score',ascending = False)[0:5]
    return last_df[['MAL_ID','Name','Score']]

def content_based_recommender_anime_10(anime_name, cosine_sim, dataframe):
    # Anime isimlerinden oluşan indeks serisi oluştur
    indices = pd.Series(dataframe.index, index=dataframe['Name'])
    # Yinelenen indeksleri kaldır
    indices = indices[~indices.index.duplicated(keep='last')]
    # Anime isminin indeksini bul
    anime_index = indices[anime_name]
    # Kosinüs benzerlik skorlarını al
    sim_scores = pd.DataFrame(cosine_sim[anime_index], columns=['score'])
    # Benzerlik skorlarına göre sıralama ve ilk 10 öneri (ilk eleman kendisi olduğundan hariç)
    anime_indices = sim_scores.sort_values('score', ascending=False).index[1:12]
    # Önerilen anime isimlerini döndür
    last_df = dataframe[['MAL_ID','Name','Score']].iloc[anime_indices].sort_values('Score',ascending = False)[0:10]
    return last_df[['MAL_ID','Name','Score']]


######################################## home_tab image info ########################################

st.markdown(
    """
    <style>
    .resizable-image img {
        width: 360px;
        height: 320px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="resizable-image" style="display: flex; justify-content: center; gap: 0px;">
        <img src="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExcmJtano5cG4zN3F0OHozZjRjZDJqeDh4dDBtdXI5czV4MHNwYTExOCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/4Ev0Ari2Nd9io/giphy.webp" alt="Resim">
        <img src="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExamprNDI0NWVxdWtrdnRkMzFrOTU1anA5OGZzdmhhaTdpdXUyY3hkeSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/JVeNlfprxQlVe/giphy.webp" alt="Resim">
        <img src="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExOW5yaWU0OHQwNTBmcWxxZWszMTB3MnRpeHM5bnNqb3BtNzVkdGxnYyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xUA7b9BGCRbVlYnnLq/giphy.webp" alt="Resim">
        <img src="https://media1.tenor.com/m/IaMF4HUM1CcAAAAC/anime-durarara.gif" alt="Resim">
        <img src="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExaXkzcWx4ZmI4dm81MDF3cm83ZmJqMjl6MjAyOHN5dWJ1ajNxdTdseiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/cVPcABKys8dHy/giphy.webp" alt="Resim">      
    </div>
    """,
    unsafe_allow_html=True,
)

######################################## home_tab title info ########################################

# CSS stilini ekliyoruz
st.markdown(
    """
    <style>
    .title-background {
        background-color: #800020;  /* Bordo renk */
        padding: 5px;  /* Çerçeve içindeki boşluk miktarını artırdık */
        border-radius: 10px;
        display: flex;
        justify-content: center;  /* Yatayda ortalamak için */
        align-items: center;  /* Dikeyde ortalamak için */
        height: 60px;  /* Çerçeve yüksekliğini ayarlayın, isteğinize göre düzenleyin */
    }
    .title-background h1 {
        color: #fdfd96;
        font-size: 24px;  /* Yazı boyutunu küçültün */
        margin: 0;  /* Başlık etrafındaki varsayılan boşlukları kaldırın */
        text-align: center;  /* Metni ortalayın */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Başlığı özel bir div ile sarıyoruz
st.markdown('<div class="title-background"><h1>Anime Universe : '
            'Discover, Watch, and Love Anime</h1></div>', unsafe_allow_html=True)

# Bir alt satıra geçmek için boşluk ekliyoruz
st.markdown("<br>", unsafe_allow_html=True)

st.write("""Dive into a world of captivating stories, breathtaking animation, and unforgettable characters! Whether you’re a seasoned otaku or a curious newcomer, our curated anime recommendations are here to guide you to your next favorite series. """)
st.write("""Ready to explore new realms and meet heroes you’ll love?""")
st.write("""Your next binge-worthy anime awaits! 🍀""")

home_tab, anime_tab = st.tabs(["Home","Anime Recommendation"])

######################################## anime_tab button info ########################################

st.markdown(
    """
    <style>
    .stButton > button {
        background-color: #fdfd96;
        color: black;
        border: 2px solid black; /* Varsayılan çerçeve rengi */
        transition: color 0.3s, border-color 0.3s; /* Renk değişiminin daha yumuşak olması için */
    }
    .stButton > button:hover {
        color: #800020; /* Mouse üzerine gelindiğinde yazı rengi */
        border-color: #800020; /* Mouse üzerine gelindiğinde çerçeve rengi bordo */
    }
    </style>
    """,
    unsafe_allow_html=True
)

######################################## home_page sayfa duzenlemesi ########################################

############## home page anime onerisi ile ilgili secenekler icin  ##############

# CSS stilini ekliyoruz
st.markdown(
    """
    <style>
    .home-background {
        background-color: #800020;  /* Bordo renk */
        padding: 5px;  /* Çerçeve içindeki boşluk miktarını artırdık */
        border-radius: 10px;
        display: flex;
        justify-content: center;  /* Yatayda ortalamak için */
        align-items: center;  /* Dikeyde ortalamak için */
        height: 40px;  /* Çerçeve yüksekliğini ayarlayın, isteğinize göre düzenleyin */
    }
    .home-background h1 {
        color: white;
        font-size: 20px;  /* Yazı boyutunu küçültün */
        margin: 0;  /* Başlık etrafındaki varsayılan boşlukları kaldırın */
        text-align: center;  /* Metni ortalayın */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Ana başlık için bir container oluşturun
with home_tab.container():
    home_tab.markdown('<div class="home-background"><h1>The Best Animes</h1></div>', unsafe_allow_html=True)

home_tab.markdown("<br>", unsafe_allow_html=True)

############## home page anime onerisi ile ilgili popularity icin  ##############

# Anime listesi ve linkleri
popularity_anime_dict = {
    "Death Note": "https://www.crunchyroll.com/",
    "Shingeki no Kyojin": "https://www.crunchyroll.com/series/GR751KNZY/attack-on-titan",
    "Fullmetal Alchemist: Brotherhood": "https://www.crunchyroll.com/series/GRGGPG93R/fullmetal-alchemist-brotherhood",
    "Sword Art Online": "https://www.crunchyroll.com/series/GR49G9VP6/sword-art-online",
    "One Punch Man": "https://www.crunchyroll.com/series/G63K98PZ6/one-punch-man",
    "Boku no Hero Academia": "https://www.crunchyroll.com/series/G6NQ5DWZ6/my-hero-academia",
    "Tokyo Ghoul": "https://www.crunchyroll.com/series/G6NV7Z50Y/tokyo-ghoul",
    "Naruto": "https://www.crunchyroll.com/series/GY9PJ5KWR/naruto",
    "Steins;Gate": "https://www.crunchyroll.com/series/GYWE7W5GY/steinsgate",
    "Kimi no Na wa.": "https://www.crunchyroll.com/series/G9VHN9PK3/your-name"
}

# Dataframe oluşturma
popularity = pd.DataFrame(list(popularity_anime_dict.items()), columns=["Popular Animes", "Link"])

# İsimleri tıklanabilir hale getirme
def make_clickable(anime, link):
    return f'<a target="_blank" href="{link}">{anime}</a>'

popularity['Popular Animes'] = popularity.apply(lambda row: make_clickable(row['Popular Animes'], row['Link']), axis=1)
popularity.drop(columns=['Link'], inplace=True)  # Link kolonunu kaldır

# İndeksi 1'den başlatma
popularity.index = popularity.index + 1

# CSS stilini belirleme
css = '''
<style>
    th {
        text-align: left !important;
    }
    table {
        width: 100%;
    }
</style>
'''

############## home page anime onerisi ile ilgili favorites icin  ##############

# Favori anime listesi ve linkleri
favorites_anime_dict = {
    "Cowboy Bebop": "https://www.crunchyroll.com/series/GYVNXMVP6/cowboy-bebop",
    "Kimetsu no Yaiba": "https://crunchyroll.com/series/GY5P48XEY/demon-slayer-kimetsu-no-yaiba",
    "Steins;Gate": "https://www.crunchyroll.com/series/GYWE7W5GY/steinsgate",
    "Death Note": "https://www.crunchyroll.com/",
    "Code Geass: Hangyaku no Lelouch": "https://www.crunchyroll.com/series/GY2P9ED0Y/code-geass",
    "Haikyuu!!": "https://www.crunchyroll.com/series/GY8VM8MWY/haikyu",
    "One Punch Man": "https://www.crunchyroll.com/series/G63K98PZ6/one-punch-man",
    "Mahou Shoujo Madoka★Magica": "https://www.crunchyroll.com/series/GRDQK39GY/puella-magi-madoka-magica",
    "Shingeki no Kyojin": "https://www.crunchyroll.com/series/GR751KNZY/attack-on-titan",
    "Tengen Toppa Gurren Lagann": "https://www.crunchyroll.com/series/GR097JN7R/gurren-lagann"
}


# Dataframe oluşturma
favorites = pd.DataFrame(list(favorites_anime_dict.items()), columns=["Favorite Anime Series", "Link"])

# İsimleri tıklanabilir hale getirme
def make_clickable(anime, link):
    return f'<a target="_blank" href="{link}">{anime}</a>'

favorites['Favorite Anime Series'] = favorites.apply(lambda row: make_clickable(row['Favorite Anime Series'], row['Link']), axis=1)
favorites.drop(columns=['Link'], inplace=True)  # Link kolonunu kaldır

# İndeksi 1'den başlatma
favorites.index = favorites.index + 1

# CSS stilini belirleme
css = '''
<style>
    th {
        text-align: left !important;
    }
    table {
        width: 100%;
    }
</style>
'''

############## home page anime onerisi ile ilgili ranked icin  ##############

ranked_anime_dict = {
    "Bronze: Zetsuai Since 1989": "https://www.crunchyroll.com/",
    "Saigo no Door wo Shimero!": "https://www.crunchyroll.com/series/GXJHM3NW5/higehiro-after-being-rejected-i-shaved-and-took-in-a-high-school-runaway",
    "Yebisu Celebrities 1st": "https://www.crunchyroll.com/",
    "Haru wo Daite Ita": "https://www.crunchyroll.com/",
    "Papa to Kiss in the Dark": "https://www.crunchyroll.com/",
    "Koisuru Boukun": "https://www.crunchyroll.com/series/G6NQ59GG6/love-tyrant",
    "Kizuna: Koi no kara Sawagi": "https://www.crunchyroll.com/series/G0XHWM577/kizuna-no-allele",
    "Saezuru Tori wa Habatakanai: The Clouds Gather": "https://www.crunchyroll.com/news/latest/2019/12/26/bl-anime-film-saezuru-tori-wa-habatakanai-1st-trailer-introduces-its-main-yakuza-characters",
    "Hyakujitsu no Bara: Jinginaki Nikukyuu-hen": "https://www.crunchyroll.com/series/G5PHNM7J2/the-magical-revolution-of-the-reincarnated-princess-and-the-genius-young-lady",
    "Yarichin☆Bitch-bu": "https://www.crunchyroll.com/"
}

# Dataframe oluşturma
ranked = pd.DataFrame(list(ranked_anime_dict.items()), columns=["Top-Rated Animes", "Link"])

# İsimleri tıklanabilir hale getirme
def make_clickable(anime, link):
    return f'<a target="_blank" href="{link}">{anime}</a>'

ranked['Top-Rated Animes'] = ranked.apply(lambda row: make_clickable(row['Top-Rated Animes'], row['Link']), axis=1)
ranked.drop(columns=['Link'], inplace=True)  # Link kolonunu kaldır

# İndeksi 1'den başlatma
ranked.index = ranked.index + 1

# CSS stilini belirleme
css = '''
<style>
    th {
        text-align: left !important;
    }
    table {
        width: 100%;
    }
</style>
'''

############## home page anime onerisi ile ilgili popularity,favorites,ranked yanyana yazmak icin  ##############

# Kolonlar oluşturma
col1, col2, col3 = home_tab.columns(3)

with col1:
    col1.write(css + popularity.to_html(escape=False, index=False), unsafe_allow_html=True)

with col2:
    col2.write(css + favorites.to_html(escape=False, index=False), unsafe_allow_html=True)

with col2:
    col3.write(css + ranked.to_html(escape=False, index=False), unsafe_allow_html=True)

############## home page ana title diger secenekler icin  ##############

# CSS stilini ekliyoruz
st.markdown(
    """
    <style>
    .discover-background {
        background-color: #800020;  /* Bordo renk */
        padding: 5px;  /* Çerçeve içindeki boşluk miktarını artırdık */
        border-radius: 10px;
        display: flex;
        justify-content: center;  /* Yatayda ortalamak için */
        align-items: center;  /* Dikeyde ortalamak için */
        height: 40px;  /* Çerçeve yüksekliğini ayarlayın, isteğinize göre düzenleyin */
    }
    .discover-background h1 {
        color: white;
        font-size: 20px;  /* Yazı boyutunu küçültün */
        margin: 0;  /* Başlık etrafındaki varsayılan boşlukları kaldırın */
        text-align: center;  /* Metni ortalayın */
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Ana başlık için bir container oluşturun
with home_tab.container():
    home_tab.markdown('<div class="discover-background"><h1>Discover More!</h1></div>', unsafe_allow_html=True)

home_tab.markdown("<br>", unsafe_allow_html=True)

############## home page diger seceneklerin gosterimi  ##############

with home_tab.container():  # 'home_tab' yerine st.container kullanın

    col1, col2, col3, col4, col5, col6 = st.columns([1, 0.45, 0.45, 0.45, 1,0.5], gap='large')

    # ! anime column
    image_airbnb = "https://media1.tenor.com/m/rsSIoLjds9UAAAAC/airbnb-door.gif"
    redirect_airbnb = "https://airbnbrecommendations.streamlit.app/"

    html_airbnb = f"""
    <div style="position: relative; width: 150px; height: 150px;">
        <a href="{redirect_airbnb}" target="_blank">
            <img src="{image_airbnb}" style="width:150px;height:150px;">
            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; background: rgba(0, 0, 0, 0.5); color: white; font-size: 15px; font-weight: bold;">AIRBNB</div>
        </a>
    </div>
    """

    col2.markdown(html_airbnb, unsafe_allow_html=True)


    # ! imdb column
    image_movie = 'https://media.tenor.com/HJTXKCtOYwgAAAAM/perfect-popcorn.gif'
    redirect_movie = "https://miuulmovierecommender.streamlit.app/"

    html_movie = f"""
    <div style="position: relative; width: 150px; height: 150px;">
        <a href="{redirect_movie}" target="_blank">
            <img src="{image_movie}" style="width:150px;height:150px;">
            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; background: rgba(0, 0, 0, 0.5); color: white; font-size: 15px; font-weight: bold;">MOVIE</div>
        </a>
    </div>
    """

    col3.markdown(html_movie, unsafe_allow_html=True)


    # ! amazon column
    image_amazon = "https://c.tenor.com/xrld-zE_4IAAAAAd/tenor.gif"
    redirect_amazon = "https://book-recomendations.streamlit.app/"
    html_amazon = f"""
    <div style="position: relative; width: 150px; height: 150px;">
        <a href="{redirect_amazon}" target="_blank">
            <img src="{image_amazon}" style="width:150px;height:150px;">
            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; background: rgba(0, 0, 0, 0.5); color: white; font-size: 15px; font-weight: bold;">BOOK</div>
        </a>
    </div>
    """

    col4.markdown(html_amazon, unsafe_allow_html=True)

    # ! steam column
    image_steam = "https://media1.tenor.com/m/zjbXreUb5_YAAAAd/steam.gif"
    redirect_steam = "https://gamerecommendations.streamlit.app/"

    html_steam = f"""
    <div style="position: relative; width: 150px; height: 150px;">
        <a href="{redirect_steam}" target="_blank">
            <img src="{image_steam}" style="width:150px;height:150px;">
            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; background: rgba(0, 0, 0, 0.5); color: white; font-size: 15px; font-weight: bold;">GAME</div>
        </a>
    </div>
    """

    col5.markdown(html_steam, unsafe_allow_html=True)



######################################## ANIME MODEL BASED RECOMMENDATION ########################################


######################################## anime recommandation sayfa duzenlemesi ########################################

# Kullanıcı bazlı ayrıştırma sorusu
user_response = anime_tab.radio("Would you like us to provide you with personalized recommendations?", ("Sure", "Just a recommendation based on my favorite anime, please."))

if user_response == "Sure":
    with anime_tab:
        anime_col1, anime_col2, anime_col3 = anime_tab.columns([1, 2, 1])
        anime_col2.write("""Embark on a delightful adventure!""")
        selected_user = anime_col2.selectbox('User ID:',options=["👉Please choose your user id"] + rating_complete_data['user_id'].unique().tolist())
        selected_anime = anime_col2.selectbox('Anime List:', options=["👉Please choose your favorite anime"] + anime_data['Name'].unique().tolist())

        if selected_anime not in ["👉Please choose your favorite anime"] and selected_user not in ["👉Please choose your user id"]:

            recommendations_df = content_based_recommender_anime(anime_name=selected_anime, cosine_sim=cosine_sim, dataframe=anime_data)
            recommendations_df_user = get_svd_recommendations_anime(user_id = selected_user, n_recommendations=5)

            anime_1, anime_2, anime_3, anime_4, anime_5 = anime_tab.columns(5)
            anime_6, anime_7, anime_8, anime_9, anime_10 = anime_tab.columns(5)

            animecol1, animecol2, animecol3 = anime_tab.columns([1, 0.5, 1], gap='large')
            recommend_button = animecol2.button('Discover Your Next Favorite Anime')
            if recommend_button:
                # Önerilen animeleri göster
                total_anime = [anime_1, anime_2, anime_3, anime_4, anime_5, anime_6, anime_7, anime_8, anime_9,anime_10]
                num_recommendations = len(total_anime)

                # İlk 5 anime için content-based öneriler
                # Önerilen animeleri göster
                for index, anime_col in enumerate(total_anime):
                    if index in range(5):
                        # `recommendations_df` DataFrame'inden MAL ID'sini ve başlığını al
                        if index < len(recommendations_df):
                            ############# anime content based 5 items ############
                            anime_col.markdown("<br>", unsafe_allow_html=True)
                            anime_col.write("""Recommendation Based on Your Favorite Anime""")
                            anime_col.markdown("<br>", unsafe_allow_html=True)

                            # Bu indeksleri kullanarak DataFrame'den satırları seçmek
                            anime_row = recommendations_df.iloc[index]

                            anime_id = anime_row['MAL_ID']
                            anime_title = anime_row['Name']
                            anime_score = anime_row['Score']

                            # `anime` DataFrame'inde anime ID'sine göre arama yap
                            anime = anime_data.loc[anime_data['MAL_ID'] == anime_id]  # Anime DataFrame'inde id sütununa göre arama yap

                            if anime.empty:
                                continue  # Anime bulunamadıysa bir sonraki animeye geç

                            anime_id = anime['MAL_ID'].values[0]  # Numpy array'den str'e dönüştürme

                            # Resim URL'sini alma ve kontrol etme
                            image_url = get_anime_image(anime_id)

                            if image_url:
                                html_anime = f"""<img src="{image_url}" style="width:350px;height:500px;"></a>"""
                                anime_col.markdown(html_anime, unsafe_allow_html=True)

                            # Anime title in one line and score on the next line
                            anime_col.markdown(
                                f"<div style='font-size:14px; white-space:nowrap;'>{anime_title}</div>",
                                unsafe_allow_html=True
                            )
                            anime_col.markdown(
                                f"<div style='font-size:14x;'>Users’ Anime Rating: {anime_score}</div>",
                                unsafe_allow_html=True
                            )

                            anime_col.markdown("<br>", unsafe_allow_html=True)


                            ############# anime model based 5 items ############
                    if index in range(5, num_recommendations):
                            index = index - 5
                            anime_col.write("""Your Personalized Anime Recommendation""")
                            anime_col.markdown("<br>", unsafe_allow_html=True)

                            # Bu indeksleri kullanarak DataFrame'den satırları seçmek
                            anime_row_user = recommendations_df_user.iloc[index]

                            anime_id_user = anime_row_user['MAL_ID']
                            anime_title_user = anime_row_user['Name']
                            anime_score_user = anime_row_user['Predicted_Rating']

                            # `anime` DataFrame'inde anime ID'sine göre arama yap
                            anime_user = anime_data.loc[anime_data['MAL_ID'] == anime_id_user]  # Anime DataFrame'inde id sütununa göre arama yap

                            if anime_user.empty:
                                continue  # Anime bulunamadıysa bir sonraki animeye geç

                            anime_id_user = anime_user['MAL_ID'].values[0]  # Numpy array'den str'e dönüştürme

                            # Resim URL'sini alma ve kontrol etme
                            image_url_user = get_anime_image(anime_id_user)

                            if image_url:
                                html_anime_user = f"""<img src="{image_url_user}" style="width:350px;height:500px;"></a>"""
                                anime_col.markdown(html_anime_user, unsafe_allow_html=True)

                            # Anime title in one line and score on the next line
                            anime_col.markdown(
                                f"<div style='font-size:14px; white-space:nowrap;'>{anime_title_user}</div>",
                                unsafe_allow_html=True
                            )
                            anime_col.markdown(
                                f"<div style='font-size:14x;'>Your Estimated Anime Rating: {anime_score_user:.2f}</div>",
                                unsafe_allow_html=True
                            )
                            anime_col.markdown("<br>", unsafe_allow_html=True)

        else:
            anime_1, anime_2, anime_3, anime_4, anime_5 = anime_tab.columns(5)
            animecol1, animecol2, animecol3 = anime_tab.columns([1, 0.5, 1], gap='large')
            recommend_button = animecol2.button('Discover Your Next Favorite Anime')
            if recommend_button:
                animecol1, animecol2, animecol3, animecol4, animecol5 = anime_tab.columns([1, 0.3, 1, 0.38, 1])
                animecol3.markdown(
                    """
                    <style>
                    .resizable-image img {
                        width: 350px;
                        height: 320px;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )

                animecol3.markdown(
                    """
                    <div class="resizable-image" style="display: flex; justify-content: center; gap: 0px;">
                        <img src="https://media1.tenor.com/m/MN7AADxIRkgAAAAC/the-simpsons-lisa.gif" alt="Resim">
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
else:
    anime_col1, anime_col2, anime_col3 = anime_tab.columns([1, 2, 1])
    anime_col2.write("""Embark on a delightful adventure!""")
    selected_anime = anime_col2.selectbox('Anime List:', options=["👉Please choose your favorite anime"] + anime_data['Name'].unique().tolist())
    with anime_tab:
        if selected_anime not in ["👉Please choose your favorite anime"]:
            recommendations_df_10 = content_based_recommender_anime_10(anime_name = selected_anime, cosine_sim = cosine_sim, dataframe = anime_data)
            anime_1, anime_2, anime_3, anime_4, anime_5 = anime_tab.columns(5)
            anime_6, anime_7, anime_8, anime_9, anime_10 = anime_tab.columns(5)

            animecol1, animecol2, animecol3 = anime_tab.columns([1, 0.5, 1], gap='large')
            recommend_button = animecol2.button('Discover Your Next Favorite Anime')
            if recommend_button:
                # Önerilen animeleri göster
                for index, anime_col in enumerate([anime_1, anime_2, anime_3, anime_4, anime_5,anime_6, anime_7, anime_8, anime_9, anime_10]):
                    # `recommendations_df` DataFrame'inden MAL ID'sini ve başlığını al
                    if index < len(recommendations_df_10):
                        anime_row = recommendations_df_10.iloc[index]
                        anime_id = anime_row['MAL_ID']
                        anime_title = anime_row['Name']
                        anime_score = anime_row['Score']

                        # `anime` DataFrame'inde anime ID'sine göre arama yap
                        anime = anime_data.loc[
                            anime_data['MAL_ID'] == anime_id]  # Anime DataFrame'inde id sütununa göre arama yap

                        st.markdown("<br>", unsafe_allow_html=True)

                        if anime.empty:
                            continue  # Anime bulunamadıysa bir sonraki animeye geç

                        anime_id = anime['MAL_ID'].values[0]  # Numpy array'den str'e dönüştürme

                        # Resim URL'sini alma ve kontrol etme
                        image_url = get_anime_image(anime_id)

                        if image_url:
                            html_anime = f"""<img src="{image_url}" style="width:350px;height:500px;"></a>"""
                            anime_col.markdown(html_anime, unsafe_allow_html=True)

                        # Anime title in one line and score on the next line
                        anime_col.markdown(
                            f"<div style='font-size:14px; white-space:nowrap;'>{anime_title}</div>",
                            unsafe_allow_html=True
                        )
                        anime_col.markdown(
                            f"<div style='font-size:14x;'>Users’ Anime Rating: {anime_score}</div>",
                            unsafe_allow_html=True
                        )
                        anime_col.markdown("<br>", unsafe_allow_html=True)
        else:
            anime_1, anime_2, anime_3, anime_4, anime_5 = anime_tab.columns(5)
            animecol1, animecol2, animecol3 = anime_tab.columns([1, 0.5, 1], gap='large')
            recommend_button = animecol2.button('Discover Your Next Favorite Anime')
            if recommend_button:
                animecol1, animecol2, animecol3, animecol4, animecol5 = anime_tab.columns([1, 0.3, 1, 0.38, 1])
                animecol3.markdown(
                    """
                    <style>
                    .resizable-image img {
                        width: 350px;
                        height: 320px;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )

                animecol3.markdown(
                    """
                    <div class="resizable-image" style="display: flex; justify-content: center; gap: 0px;">
                        <img src="https://media1.tenor.com/m/MN7AADxIRkgAAAAC/the-simpsons-lisa.gif" alt="Resim">
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
