
import streamlit as st
import pandas as pd
from scrape import get_image_from_imdb
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit.components.v1 as components

st.set_page_config(layout= 'wide', page_title = 'Miuul Movie Recommender',page_icon=":clapper:")


@st.cache_data
def get_data():
    meta = pd.read_csv('movie_recommendation_file.csv')
    return meta

meta = get_data()

@st.cache_data
def calculate_cosine_sim(dataframe):
    tfidf = TfidfVectorizer(stop_words='english')
    dataframe['overview'] = dataframe['overview'].fillna('')
    dataframe['overview'] = dataframe['overview'] + ' ' + dataframe['title'] + ' ' + dataframe['genres']
    tfidf_matrix = tfidf.fit_transform(dataframe['overview'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cosine_sim

cosine_sim = calculate_cosine_sim(meta)



def content_based_recommender(title, cosine_sim, dataframe):
    # index'leri olusturma
    indices = pd.Series(dataframe.index, index=dataframe['title'])
    indices = indices[~indices.index.duplicated(keep='last')]
    # title'ın index'ini yakalama
    movie_index = indices[title]
    # Benzerlik skorlarını alma
    similarity_scores = cosine_sim[movie_index]
        # Eğer similarity_scores 3D bir dizi ise (örneğin, [1, 9548, 9548]), 2D'ye dönüştürme
    if similarity_scores.ndim == 3:
            similarity_scores = similarity_scores.squeeze()  # 3D'den 2D'ye sıkıştırma
        # Benzerlik skorlarını DataFrame'e dönüştürme
    similarity_scores_df = pd.DataFrame(similarity_scores, index=dataframe.index, columns=["score"])
        # Kendisi haric ilk 10 filmi getirme
    movie_indices = similarity_scores_df.sort_values(by="score", ascending=False).index[1:11]
        # Film bilgilerini döndürme
    return dataframe.loc[movie_indices]



col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown('<div style="width:277px;height:277px;"><img src="https://media1.tenor.com/m/O-yqDCMQTFoAAAAd/god-i-love-it-red.gif" style="width:100%; height:100%; object-fit:cover;"></div>', 
        unsafe_allow_html=True)


with col2:
    st.markdown(
    '<div style="width:277px;height:277px;"><img src="https://media1.tenor.com/m/l4PRWJ68WWYAAAAd/i-understand-don-vito-corleone.gif" style="width:100%; height:100%; object-fit:cover;"></div>', 
        unsafe_allow_html=True)

with col3:
    st.markdown(
    '<div style="width:277px;height:277px;"><img src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMWFxaTEzd2phcW13a3JveGd6aTZtN2UxZjM5azBiYzc3dDUwdTA0YSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/u7uiWWbRFC2TC/giphy.gif" style="width:100%; height:100%; object-fit:cover;"></div>', 
        unsafe_allow_html=True)


with col4:
    st.markdown(
    '<div style="width:277px;height:277px;"><img src="https://media1.tenor.com/m/B_p2kigHBqMAAAAd/deadpool-dance-bye-bye-bye.gif" style="width:100%; height:100%; object-fit:cover;"></div>', 
        unsafe_allow_html=True)

with col5:
    st.markdown(
    '<div style="width:277px;height:277px;"><img src="https://media1.tenor.com/m/V24w9mQa-nQAAAAd/%D8%A7%D9%84%D9%85%D9%88%D8%B3%D9%8A%D9%82%D8%A7%D8%B1.gif" style="width:100%; height:100%; object-fit:cover;"></div>', 
        unsafe_allow_html=True)

css = '''
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:1rem;
    }
</style>
'''

st.markdown(css, unsafe_allow_html=True)

st.markdown("""
    <style>
    /* Sekme başlıklarını hedefle ve stil uygula */
    .stTabs [role="tab"] {
        font-size: 10px; /* Yazı boyutu */
        border: 2px solid #000000; /* Kenarlık rengi ve kalınlığı */
        color: white; /* Metin rengi */
        padding: 10px; /* İç boşluk */
        border-radius: 10px 10px 0 0; /* Köşeleri yuvarlat */
        background-color: #000000; /* Arka plan rengi */
    }

    /* Seçili sekme stilini değiştir */
    .stTabs [role="tab"][aria-selected="true"] {
        font-size: 10px; /* Yazı boyutu */
        border-bottom: 3px solid skyblue; /* Alt çizgi rengi ve kalınlığı */
        color: skyblue; /* Metin rengi */
    }

    /* Sekme üzerine gelindiğinde (hover) stilini değiştir */
    .stTabs [role="tab"]:hover {
        color: skyblue; /* Metin rengi */
        border-color: black; /* Kenarlık rengi */
    }
    </style>
    """, unsafe_allow_html=True)

# Sekmeleri oluştur
home_tab, recommendation_tab = st.tabs(['Home', 'Movie Recommendation'])
st.markdown(
    """
    <style>
    .stButton > button {
        background-color: black;
        color: skyblue;
        border: 2px solid black; /* Varsayılan çerçeve rengi /
        transition: color 0.3s, border-color 0.3s; / Renk değişiminin daha yumuşak olması için /
    }
    .stButton > button:hover {
        color: skyblue; / Mouse üzerine gelindiğinde yazı rengi /
        border-color: black; / Mouse üzerine gelindiğinde çerçeve rengi bordo */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# with home_tab.container():  # Adjust to your layout

col1, col2, col3 = home_tab.columns(3)  # Adjust the ratio as needed
font_style = 'font-size: 16px;'
heading_style = 'font-size: 16px; margin-bottom: 5px;'





with col1:
    st.markdown("""
    <div style="text-align: justify; {}; ">
        <strong style="color: skyblue; {}">Personalized Recommendations</strong><br>
        <strong>Our system uses advanced algorithms to analyze your movie preferences and recommend films that match your taste. Discover hidden gems and timeless classics tailored just for you.<br>
    </div>
    """.format(font_style, heading_style), unsafe_allow_html=True)
    st.markdown("")
    st.markdown('<div style="width:450px;height:300px;"><img src="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExaHp4czExdnpkYTRzYnJnazQyY21tbzI1Mmh2dnNoZzVuMnU3YmlubSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/VGG8UY1nEl66Y/giphy.webp" style="width:100%; height:100%; object-fit:cover;"></div>', 
            unsafe_allow_html=True)

with col2:
    st.markdown('<div style="width:450px;height:300px;"><img src="https://media4.giphy.com/media/n5FovccDXbcOY/giphy.webp?cid=790b7611u348p2n3bwby2xos1v936j2gb1r9h6wyrs8lrt00&ep=v1_gifs_search&rid=giphy.webp&ct=g" style="width:100%; height:100%; object-fit:cover;"></div>', 
        unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: justify; {}; ">
        <strong style="color: skyblue; {}">What We Offer:</strong><br>
        <strong>Personalized Recommendations:</strong> Find movies similar to those you love.<br>
        <strong>Rich Visuals:</strong> Access movie posters and details via IMDb.
    </div>
    """.format(font_style, heading_style), unsafe_allow_html=True)
    col2.markdown("<br>", unsafe_allow_html=True)

    
with col3:
    st.markdown("""
        <div style="text-align: justify; {}; ">
        <strong style="color: skyblue; {}">How It Works:</strong><br>
        Our system analyzes your preferences and viewing history to provide tailored movie suggestions. By leveraging advanced algorithms and data from various sources, including IMDb, we deliver accurate and engaging recommendations. Simply explore the suggested movies, view their details, and enjoy discovering your next favorite film!
        </div>
        """.format(font_style, heading_style), unsafe_allow_html=True)
    
    st.markdown('<div style="width:450px;height:300px;"><img src="https://media3.giphy.com/media/tivaSkhu8MbKM/giphy.webp?cid=790b7611sjrk12dvwbjhnjayw0xawnnjgsziac0zhifwus4u&ep=v1_gifs_search&rid=giphy.webp&ct=g" style="width:100%; height:100%; object-fit:cover;"></div>', 
        unsafe_allow_html=True)


st.header("")    
airbnb, book, game, anime = home_tab.columns(4)

home_tab.markdown('''
<style>
.title-background {
    background-color: skyblue; /* Skyblue */
    color: #666666;
    text-align: center;
    border-radius: 15px; /* Köşeleri yuvarlatır */
    padding: 10px 20px; /* İç boşluk */
    border: 1px solid #1DB954; /* Çerçeve rengi ve kalınlığı */
    font-size: 20px; /* Yazı boyutu */
    width: 100%; /* Çerçeve genişliği */
    height: 50px; /* Çerçeve yüksekliği */
    display: flex; /* Flexbox kullanımı */
    align-items: center; /* Dikey merkezleme */
    justify-content: center; /* Yatay merkezleme */
}
.title-background h1 {
        color: white;
        font-size: 20px;  / Yazı boyutunu küçültün /
        margin: 0;  / Başlık etrafındaki varsayılan boşlukları kaldırın /
        text-align: center;  / Metni ortalayın */
    }
    </style>
</style>

<div class="title-background">
    <h1>Discover More!</h1>
</div>
''', unsafe_allow_html=True)
home_tab.markdown("<br>", unsafe_allow_html=True)
home_tab.markdown("<br>", unsafe_allow_html=True)



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


    # ! airbnb column
    image_airbnb = 'https://media1.tenor.com/m/rsSIoLjds9UAAAAC/airbnb-door.gif'
    redirect_airbnb = "https://airbnbrecommendations.streamlit.app/"

    html_airbnb = f"""
    <div style="position: relative; width: 150px; height: 150px;">
        <a href="{redirect_airbnb}" target="_blank">
            <img src="{image_airbnb}" style="width:150px;height:150px;">
            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; background: rgba(0, 0, 0, 0.5); color: white; font-size: 15px; font-weight: bold;">AIRBNB</div>
        </a>
    </div>
    """

    col3.markdown(html_airbnb, unsafe_allow_html=True)


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


with recommendation_tab:  # 'home_tab' yerine st.container kullanın
    movie_col1, movie_col2, movie_col3 = st.columns([1,2,1])
    selected_movie = movie_col2.selectbox('Choose a movie you like.', options=meta.title.unique())

    recommendations_df = content_based_recommender(title=selected_movie, cosine_sim=cosine_sim, dataframe=meta)
    
    # İlk 5 filmi göstermek için 5 kolon
    row1_cols = st.columns(5)
    # Sonraki 5 filmi göstermek için 5 kolon
    row2_cols = st.columns(5)

    tmdbcol1, tmdbcol2, tmdbcol3 = st.columns([1,0.5,1], gap='large')
    recommend_button = tmdbcol2.button('Recommend a Movie')

    if recommend_button:
        for index, movie_col in enumerate(row1_cols+row2_cols):
            if index < len(recommendations_df):
                movie_row = recommendations_df.iloc[index]
                movie_id = movie_row['id']
                movie_title = movie_row['title']

                # `meta` DataFrame'inde film ID'sine göre arama yap
                movie = meta.loc[meta['id'] == movie_id]  # Meta DataFrame'inde id sütununa göre arama yap

                if movie.empty:
                    continue  # Film bulunamadıysa bir sonraki filme geç

                imdb_id = movie['imdb_id'].values[0]  # Numpy array'den str'e dönüştürme
                imdb_url = f"https://www.imdb.com/title/{imdb_id}/"
                
                # Resim URL'sini alma ve kontrol etme
                image_url = get_image_from_imdb(imdb_id)
                if image_url:
                    # HTML bağlantısı ile resmi tıklanabilir yapma
                    movie_col.markdown(
                        f'<a href="{imdb_url}" target="_blank">'
                        f'<img src="{image_url}" width="200" style="display: block; margin-left: auto; margin-right: auto;">'
                        f'</a>',
                        unsafe_allow_html=True
                    )
                    
                    # Film adını standart font boyutunda gösterme
                    movie_col.markdown(f'<p style="text-align: center; font-size: 18px; font-weight: bold;">{movie_title}</p>', unsafe_allow_html=True)

