######################################## import data ########################################

import pandas as pd
from streamlit_folium import folium_static, st_folium
from sklearn.neighbors import NearestNeighbors
import folium
from folium.plugins import MarkerCluster
from sklearn.preprocessing import StandardScaler
import streamlit.components.v1 as components
import streamlit as st

st.set_page_config(layout= 'wide', page_title = ' Airbnb Recommender', page_icon= "🏡")

######################################## read_csv########################################
# st.cache_data
@st.cache_data
def get_data():
    meta = pd.read_csv('airbnb_data_son.csv')
    return meta

airbnb_data = get_data()

######################################## home_tab information ########################################


st.markdown(
    """
    <style>
    .resizable-image img {
        width: 320px;
        height: 320px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="resizable-image" style="display: flex; justify-content: center; gap: 0px;">
        <img src="https://a0.muscache.com/im/pictures/hosting/Hosting-1019299865555116257/original/90b8ccdd-627d-4081-bea2-cf5dca87ed8f.jpeg?im_w=720" alt="Resim">
        <img src="https://a0.muscache.com/im/pictures/hosting/Hosting-U3RheVN1cHBseUxpc3Rpbmc6NDM1MTQ1NDA%3D/original/765b1175-fbf6-4920-81da-4dca99e6972c.jpeg?im_w=720"" alt="Resim">
        <img src="https://a0.muscache.com/im/pictures/2ce2f829-7965-479a-af98-c5a84824ce06.jpg?im_w=720" alt="Resim">
        <img src="https://a0.muscache.com/im/pictures/ba068000-9f61-459c-9ecb-6edc11169604.jpg?im_w=720" alt="Resim">
        <img src="https://a0.muscache.com/im/pictures/9e10ac8b-903d-4e54-9a23-74935f14b4a6.jpg?im_w=720" alt="Resim">
        <img src="https://a0.muscache.com/im/pictures/e636f3b7-20f1-4056-815c-6634ee3a5753.jpg?im_w=720" alt="Resim">      
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
        background-color: #B0FF92;  /* Bordo renk */
        padding: 5px;  /* Çerçeve içindeki boşluk miktarını artırdık */
        border-radius: 10px;
        display: flex;
        justify-content: center;  /* Yatayda ortalamak için */
        align-items: center;  /* Dikeyde ortalamak için */
        height: 60px;  /* Çerçeve yüksekliğini ayarlayın, isteğinize göre düzenleyin */
    }
    .title-background h1 {
        color: black;
        font-size: 24px;  /* Yazı boyutunu küçültün */
        margin: 0;  /* Başlık etrafındaki varsayılan boşlukları kaldırın */
        text-align: center;  /* Metni ortalayın */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Başlığı özel bir div ile sarıyoruz
st.markdown('<div class="title-background"><h1>Travel Escapes: Explore, Stay, and Cherish Every Moment</h1></div>', unsafe_allow_html=True)

# Bir alt satıra geçmek için boşluk ekliyoruz
st.markdown("<br>", unsafe_allow_html=True)

st.write("""Dive into a world of captivating stories, breathtaking views, and unforgettable experiences! Whether you’re an experienced traveler or a curious newcomer, our carefully curated Airbnb recommendations are here to guide you to your next favorite stay. """)
st.write("""Ready to explore new places and discover spaces you’ll love?""")
st.write("""Your next unforgettable accommodation experience awaits! 🏡""")

######################################## airbnb_tab info ########################################

# CSS stilini eklemek için st.markdown fonksiyonunu kullan
st.markdown("""
    <style>
    /* Sekmelerin varsayılan stilini ayarla */
    .stTabs [role="tab"] {
        color: #C8AD7F;
        border: none;
        padding: 0px;
    }

    /* Orijinal çizgiyi gizlemek için */
    .stTabs [role="tab"]:not([aria-selected="true"]) {
        border-bottom: none;
    }

    /* Seçili sekmenin altındaki çizgiyi ve rengini değiştir */
    .stTabs [role="tab"][aria-selected="true"] {
        color: #39FF14; /* Burada istediğiniz rengi belirleyin */
        border-bottom: 3px solid #39FF14; /* Çizginin rengini burada belirleyin */
    }

    /* Sekme üzerine gelindiğinde (hover) rengini değiştir */
    .stTabs [role="tab"]:hover {
        color: #39FF14; /* Burada istediğiniz rengi belirleyin */
    }

    /* Sekme içeriklerinin stilini ayarlamak için */
    .stTabs .stTabsPanel {
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# Sekmeler oluştur
home_tab, airbnb_tab = st.tabs(["Home", "Airbnb Recommendation"])

######################################## airbnb_tab button info ########################################

st.markdown(
    """
    <style>
    .stButton > button {
        background-color: black;
        color: #B0FF92;
        border: 2px solid black; /* Varsayılan çerçeve rengi */
        transition: color 0.3s, border-color 0.3s; /* Renk değişiminin daha yumuşak olması için */
    }
    .stButton > button:hover {
        color: #77DD77; /* Mouse üzerine gelindiğinde yazı rengi */
        border-color: #77DD77; /* Mouse üzerine gelindiğinde çerçeve rengi bordo */
    }
    </style>
    """,
    unsafe_allow_html=True
)

######################################## home_page sayfa duzenlemesi ########################################

############## home page airbnb onerisi ile ilgili secenekler icin  ##############

# CSS stilini ekliyoruz
st.markdown(
    """
    <style>
    .home-background {
        background-color: #B0FF92;  /* Bordo renk */
        padding: 5px;  /* Çerçeve içindeki boşluk miktarını artırdık */
        border-radius: 10px;
        display: flex;
        justify-content: center;  /* Yatayda ortalamak için */
        align-items: center;  /* Dikeyde ortalamak için */
        height: 40px;  /* Çerçeve yüksekliğini ayarlayın, isteğinize göre düzenleyin */
    }
    .home-background h1 {
        color: black;
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
    home_tab.markdown('<div class="home-background"><h1>The Best Places</h1></div>', unsafe_allow_html=True)

home_tab.markdown("<br>", unsafe_allow_html=True)

############## home page anime onerisi ile ilgili popularity icin  ##############

# Manhattan kiralık oda ve fiyat listesi
manhattan_dict = {
    "Private Room in Spacious Quiet Apt., Elevator ...": 288.000,
    "TriBeCa 2500 Sq Ft w/ Priv Elevator": 70.000,
    "West Side Charm - Central Park! Uh": 660.000,
    "Downtown Full Floor Loft": 855.000,
    "Live like a local! Queen size bed, private room.": 965.000,
    "Private Studio with workstation Museum Block...": 349.000,
    "A Beautiful Brownstone Apartment": 274.000,
    "Beautiful private 1BR apt in Harlem": 207.000,
    "TIMES SQ/THEATRE DIST STUDIO": 608.000,
    "Queen bed-Close to Columbia U & Central Park": 590.000
}

# Dataframe oluşturma
manhattan = pd.DataFrame(list(manhattan_dict.items()), columns=["Manhattan", "Price (USD)"])

# İsimleri tıklanabilir hale getirme
def make_clickable(listing, link):
    return f'<a target="_blank" href="{link}">{listing}</a>'

# URL ekleme ve tıklanabilir hale getirme
urls = [
    "https://www.airbnb.com/",
    "https://www.airbnb.com/",
    "https://www.airbnb.com/",
    "https://www.airbnb.com/",
    "https://www.airbnb.com/",
    "https://www.airbnb.com/",
    "https://www.airbnb.com/",
    "https://www.airbnb.com/",
    "https://www.airbnb.com/",
    "https://www.airbnb.com/"
]

manhattan['Link'] = urls
manhattan['Manhattan'] = manhattan.apply(lambda row: make_clickable(row['Manhattan'], row['Link']), axis=1)
manhattan.drop(columns=['Link'], inplace=True)

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

# Brooklyn kiralık oda ve fiyat listesi
brooklyn_dict = {
    'Victorian Private Brownstone Apartment & Backyard': 812.0,
    'Stylish Arty Apt in Brooklyn': 598.0,
    'Couples Getaway in Brooklyn!!!': 295.0,
    'NYC 1st Shipping Container Home': 822.0,
    'Brooklyn Creative Snooze Factory': 982.0,
    'Chic Victorian private apartment in townhouse': 445.0,
    'Sunny+Cozy Double bedroom in BKLYN!': 501.0,
    'Special OFFER on Airbnb NYC Room!': 421.0,
    'Williamsburg 2b apartment with deck': 407.0,
    'Spacious, Private Oasis in Historic Brownstone': 451.0
}

# Dataframe oluşturma
brooklyn = pd.DataFrame(list(brooklyn_dict.items()), columns=["Brooklyn", "Price (USD)"])

# İsimleri tıklanabilir hale getirme
def make_clickable(listing, link):
    return f'<a target="_blank" href="{link}">{listing}</a>'

# URL ekleme ve tıklanabilir hale getirme
urls = [
    "https://www.airbnb.com/",
    "https://www.airbnb.com/",
    "https://www.airbnb.com/",
    "https://www.airbnb.com/",
    "https://www.airbnb.com/",
    "https://www.airbnb.com/",
    "https://www.airbnb.com/",
    "https://www.airbnb.com/",
    "https://www.airbnb.com/",
    "https://www.airbnb.com/"
]

brooklyn['Link'] = urls
brooklyn['Brooklyn'] = brooklyn.apply(lambda row: make_clickable(row['Brooklyn'], row['Link']), axis=1)
brooklyn.drop(columns=['Link'], inplace=True)

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

# Queens kiralık oda ve fiyat listesi
queens_dict = {
    "Room Near JFK Twin Beds": 295.000,
    "Private room mins from JFK": 54.000,
    "Cozy Room Family Home LGA Airport NO CLEANING FEE": 930.000,
    "My Little Guest Room in Flushing": 919.000,
    "Room steps away from LaGuardia airport": 396.000,
    "Safe cute near subway& Manhattan NY NY retro s...": 545.000,
    "Comfy Room Family Home LGA Airport NO CLEANING...": 942.000,
    "Astoria-Private Home NYC-": 465.000,
    "JFK 10 & LGA 15 MINUTES AWAY A/C PRIVATE BED...": 74.000,
    "★★★★★Astoria |❤of NYC| Near subway -Home Share": 156.000
}

# Dataframe oluşturma
queens = pd.DataFrame(list(queens_dict.items()), columns=["Queens", "Price (USD)"])

# İsimleri tıklanabilir hale getirme
def make_clickable(listing, link):
    return f'<a target="_blank" href="{link}">{listing}</a>'

# URL ekleme ve tıklanabilir hale getirme
urls = [
    "https://www.airbnb.com/",
    "https://www.airbnb.com/",
    "https://www.airbnb.com/",
    "https://www.airbnb.com/",
    "https://www.airbnb.com/",
    "https://www.airbnb.com/",
    "https://www.airbnb.com/",
    "https://www.airbnb.com/",
    "https://www.airbnb.com/",
    "https://www.airbnb.com/"
]

queens['Link'] = urls
queens['Queens'] = queens.apply(lambda row: make_clickable(row['Queens'], row['Link']), axis=1)
queens.drop(columns=['Link'], inplace=True)

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
    col1.write(css + manhattan.to_html(escape=False, index=False), unsafe_allow_html=True)

with col2:
    col2.write(css + brooklyn.to_html(escape=False, index=False), unsafe_allow_html=True)

with col2:
    col3.write(css + queens.to_html(escape=False, index=False), unsafe_allow_html=True)

############## home page ana title diger secenekler icin  ##############

# CSS stilini ekliyoruz
st.markdown(
    """
    <style>
    .discover-background {
        background-color: #B0FF92;  /* Bordo renk */
        padding: 5px;  /* Çerçeve içindeki boşluk miktarını artırdık */
        border-radius: 10px;
        display: flex;
        justify-content: center;  /* Yatayda ortalamak için */
        align-items: center;  /* Dikeyde ortalamak için */
        height: 40px;  /* Çerçeve yüksekliğini ayarlayın, isteğinize göre düzenleyin */
    }
    .discover-background h1 {
        color: black;
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
    image_anime = "https://i.giphy.com/11KzOet1ElBDz2.webp"
    redirect_anime = "https://animerecommendations.streamlit.app/"

    html_anime = f"""
    <div style="position: relative; width: 150px; height: 150px;">
        <a href="{redirect_anime}" target="_blank">
            <img src="{image_anime}" style="width:150px;height:150px;">
            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; background: rgba(0, 0, 0, 0.5); color: white; font-size: 15px; font-weight: bold;">ANIME</div>
        </a>
    </div>
    """

    col2.markdown(html_anime, unsafe_allow_html=True)


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

    ######################################## airbnb sayfa duzenlemesi ########################################

with airbnb_tab:

    airbnb_col1, airbnb_col2, airbnb_col3, airbnb_col4 = airbnb_tab.columns(4)
    selected_neighboorhood = airbnb_col1.selectbox('Neighbourhood', options= airbnb_data.neighbourhood_group.unique())

    price_min = airbnb_col2.number_input('Min. Price', min_value=50, max_value= int(airbnb_data.price.max()), value = 50)
    price_max = airbnb_col2.number_input('Max. Price', min_value=50, max_value = int(airbnb_data.price.max()), value= 999)
    selected_room_type = airbnb_col3.selectbox('Room Type', options = airbnb_data['room type'].unique())
    selected_cancellation_policy = airbnb_col4.selectbox('Cancellation Policy', options = airbnb_data['cancellation_policy'].unique())


    airbnb_tab.markdown("""
        <style>
        .space-above {
            margin-top: 20px;
        }
        .stButton>button {
            background-color: #a3c9f1;
            color: #000000;
        }
        </style>
        """, unsafe_allow_html=True)

    aircol1, aircol2, aircol3 = airbnb_tab.columns([1,0.5,1], gap='large')
    airrecommend_button = aircol2.button('Discover Your Perfect Getaway')


    def recommend_airbnb(user_neighbourhood_group, user_price_range_min, user_price_range_max, user_room_type,
                         user_cancellation_policy, num_neighbors=2, num_recommendations=500, limit=3):

        # Kullanıcı kriterlerine göre filtreleme
        filtered_listings = airbnb_data[
            (airbnb_data['neighbourhood_group'] == user_neighbourhood_group) &
            (airbnb_data['price'] >= user_price_range_min) &
            (airbnb_data['price'] <= user_price_range_max) &
            (airbnb_data['room type'] == user_room_type) &
            (airbnb_data['cancellation_policy'] == user_cancellation_policy)
            ]

        if filtered_listings.empty:
            airbnb_tab.text("Kriterlere uygun sonuç bulunamadı.")
            return None

        # Kullanılacak özellikleri seçelim
        features = airbnb_data[['price', "service fee", 'number of reviews', 'review rate number', 'lat', 'long']]
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)

        # K-Nearest Neighbors modelini oluşturalım
        knn = NearestNeighbors(n_neighbors=num_neighbors, algorithm='auto')
        knn.fit(features_scaled)

        # Filtrelenmiş evlerin özelliklerini alalım
        filtered_features = filtered_listings[
            ['price', "service fee", 'number of reviews', 'review rate number', 'lat', 'long']]
        filtered_features_scaled = scaler.transform(filtered_features)

        # Benzer evleri bulalım
        distances, indices = knn.kneighbors(filtered_features_scaled)

        # Benzer ev ilanlarının bilgilerini alalım
        recommended_listings = airbnb_data.iloc[indices.flatten()]

        # Yalnızca review rate number 3 ve üzeri olanları filtreleyelim
        recommended_listings = recommended_listings[recommended_listings['review rate number'] >= limit]

        if recommended_listings.empty:
            airbnb_tab.text(f"Review rate number {limit} ve üzeri uygun sonuç bulunamadı.")
            return None

        # Review rate number'a göre büyükten küçüğe sıralayalım
        recommended_listings = recommended_listings.sort_values(by='review rate number', ascending=False)

        # İlk num_recommendations tanesini seçelim
        top_recommendations = recommended_listings.head(num_recommendations)
        top_recommendations['number of reviews'] = top_recommendations['number of reviews'].astype(int)
        # Ortalama konumu bulalım
        avg_lat = top_recommendations['lat'].mean()
        avg_long = top_recommendations['long'].mean()

        # Haritayı oluştur
        map_ = folium.Map(location=[avg_lat, avg_long], zoom_start=10)
        marker_cluster = MarkerCluster().add_to(map_)

        for idx, row in top_recommendations.iterrows():
            popup_html = f"""
            <div style="background-color: #B0FF92; padding: 10px; width: 200px;">
                <strong>{row['NAME']}</strong><br>
                Price: ${row['price']}<br>
                Service Fee: ${row['service fee']}<br>
                Review Rate: {row['review rate number']}<br>
                Number of Reviews: {row['number of reviews']}
            </div>
            """
            folium.Marker(
                location=[row['lat'], row['long']],
                popup=folium.Popup(popup_html, max_width=250),
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(marker_cluster)

        # Haritayı Jupyter Notebook içinde görüntüle
        return map_, top_recommendations


    if airrecommend_button:
        if price_min > price_max:
            airbnb_tab.text('Minimum Price cannot be bigger than Maximum Price')
        else:
            map_, recommendations = recommend_airbnb(user_neighbourhood_group = selected_neighboorhood, user_price_range_min = price_min,
                user_price_range_max=price_max, user_room_type = selected_room_type,user_cancellation_policy= selected_cancellation_policy)

            folium_static(map_, width=1750 , height=600)
