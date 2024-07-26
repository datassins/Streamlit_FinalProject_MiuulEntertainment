
import streamlit as st
import pandas as pd
from scrape import get_image_from_imdb
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import folium
from streamlit_folium import folium_static, st_folium
from sklearn.neighbors import NearestNeighbors
import folium
from folium.plugins import MarkerCluster
from sklearn.preprocessing import StandardScaler
import streamlit.components.v1 as components

st.set_page_config(layout= 'wide', page_title = 'Miuultainment')

@st.cache_data
def get_airbnb():
    airbnb = pd.read_csv('data/airbnb_data.csv')
    return airbnb 

airbnb_data = get_airbnb()


@st.cache_data
def get_data():
    meta = pd.read_csv('data/movie_recommendation_file.csv')
    return meta

meta = get_data()

@st.cache_data
def calculate_cosine_sim(dataframe):
    tfidf = TfidfVectorizer(stop_words='english')
    dataframe['overview'] = dataframe['overview'].fillna('')
    tfidf_matrix = tfidf.fit_transform(dataframe['overview'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cosine_sim

cosine_sim = calculate_cosine_sim(meta)


#@st.cache_data
#def popular_movies():
#    popular_movies = meta[['id', 'imdb_id','title','vote_average', 'vote_count']].sort_values(by='vote_average',ascending=False)[:50].reset_index(drop=True)
#    return popular_movies



st.image('C:/Users/erhan/OneDrive/Resimler/miuulentertainment.gif',width=1400)
st.title(':rainbow[MIUULtainment] :house: :movie_camera: :video_game:  :green_book: 🎶')

st.markdown('**Miuultainment: Enjoy a Unique Experience of Entertainment!**')
st.write("""Welcome to Miuultainment, the innovative recommendation site that caters to all your entertainment needs in one place.
Whether you're searching for a fantastic Airbnb for your next vacation, an enchanting book to read, a captivating movie to watch,
 an exciting game to play, or some new music to enjoy, Miuultainment has got you covered.""")



home_tab, airbnb_tab, amazon_tab, tmdb_tab, metacritic_tab = st.tabs(["Home","AirBnb", "Amazon", "TMDB", "MetaCritic"])

music_html = """
<audio id="audio1" autoplay style="display:none;">
  <source src="https://soundfxcenter.com/movies/matrix/8d82b5_Matrix_Welcome_To_The_Real_World_Sound_Effect.mp3" type="audio/mpeg">
</audio>

<audio id="audio2" autoplay style="display:none;">
  <source src="https://soundfxcenter.com/movies/matrix/8d82b5_Matrix_Welcome_To_The_Real_World_Sound_Effect.mp3" type="audio/mpeg">
</audio>

<audio id="audio3" autoplay style="display:none;">
  <source src="https://soundfxcenter.com/movies/matrix/8d82b5_Matrix_Welcome_To_The_Real_World_Sound_Effect.mp3" type="audio/mpeg">
</audio>

<audio id="audio4" autoplay style="display:none;">
  <source src="https://soundfxcenter.com/movies/matrix/8d82b5_Matrix_Welcome_To_The_Real_World_Sound_Effect.mp3" type="audio/mpeg">
</audio>

<audio id="audio5" autoplay style="display:none;">
  <source src="https://soundfxcenter.com/movies/matrix/8d82b5_Matrix_Welcome_To_The_Real_World_Sound_Effect.mp3" type="audio/mpeg">
</audio>

<script>
document.addEventListener('DOMContentLoaded', (event) => {
  const tabs = document.querySelectorAll('.stTabs [role="tab"]');
  let currentAudio = 0;
  
  function playAudio(index) {

    for (let i = 1; i <= 5; i++) {
      document.getElementById('audio' + i).pause();
    }

    document.getElementById('audio' + (index + 1)).play();
  }

  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => {
      playAudio(index);
    });
  });

  playAudio(0);
});
</script>
"""



 #! Home Tab
with home_tab:

   
    home_tab.header('Discover Your Next Adventure')
    home_tab.write("""At Miuultainment, we believe that every experience should be extraordinary. 
    Our platform curates personalized recommendations based on your preferences, ensuring that you find the perfect match every time.""")

    col_airbnb, col_amazon, col_movie, col_game = home_tab.columns(4)
    col_airbnb.header('Stay in the Best Places')
    airbnb = 'C:/Users/erhan/OneDrive/Resimler/1airbnb.png'
    col_airbnb.image(airbnb)
    col_airbnb.write("""Explore our extensive collection of top-rated Airbnb's. 
                    From cozy cabins in the woods to luxurious city apartments, we provide you with the best options to make your stay unforgettable.""")

    col_amazon.header('Read Engaging Books')
    amazon = 'C:/Users/erhan/OneDrive/Resimler/amazonbooks.png'
    col_amazon.image(amazon)
    col_amazon.write("""Dive into a world of literature with our handpicked book recommendations. Whether you love fiction, non-fiction, mystery,
                romance, or sci-fi, Miuultainment helps you discover books that you'll love.""")


    col_movie.header('Watch Captivating Movies')
    tmdb = 'C:/Users/erhan/OneDrive/Resimler/tmdb.jpg'
    col_movie.image(tmdb)
    col_movie.write("""Enjoy a cinematic experience with our movie suggestions. Whether you’re into thrillers, comedies, dramas, or documentaries,
                Miuultainment ensures you never run out of great movies to watch.""")

    col_game.header('Play Exciting Games')
    metacritic = 'C:/Users/erhan/OneDrive/Resimler/metacritic.png'
    col_game.image(metacritic)
    col_game.write("""Level up your gaming experience with our curated game recommendations. 
                From action-packed adventures to mind-bending puzzles, find the perfect game to keep you entertained for hours.""")
    
 
#! TMDB tab
with tmdb_tab:


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
        movie_indices = similarity_scores_df.sort_values(by="score", ascending=False).index[1:6]
        # Film bilgilerini döndürme
        return dataframe.loc[movie_indices]

    tmdb_col1, tmdb_col2, tmdb_col3 = tmdb_tab.columns([1,2,1])
    selected_movie = tmdb_col2.selectbox('Choose a movie you like.', options= meta.title.unique())


    recommendations_df = content_based_recommender(title=selected_movie,cosine_sim=cosine_sim,dataframe=meta)
    movie_1, movie_2, movie_3, movie_4, movie_5 = tmdb_tab.columns(5)


    tmdbcol1, tmdbcol2, tmdbcol3 = tmdb_tab.columns([1,0.5,1], gap='large')
    recommend_button = tmdbcol2.button('Recommend a Movie')

    if recommend_button:
        # Önerilen filmleri göster
        for index, movie_col in enumerate([movie_1, movie_2, movie_3, movie_4, movie_5]):
            # `recommendations_df` DataFrame'inden film ID'sini ve başlığını al
            if index < len(recommendations_df):
                movie_row = recommendations_df.iloc[index]
                movie_id = movie_row['id']
                movie_title = movie_row['title']
                
                # `meta` DataFrame'inde film ID'sine göre arama yap
                movie = meta.loc[meta['id'] == movie_id]  # Meta DataFrame'inde id sütununa göre arama yap

                if movie.empty:
                    continue  # Film bulunamadıysa bir sonraki filme geç
                
                imdb_id = movie['imdb_id'].values[0]  # Numpy array'den str'e dönüştürme

                movie_col.subheader(f"**{movie_title}**")

                # Resim URL'sini alma ve kontrol etme
                image_url = get_image_from_imdb(imdb_id)
                if image_url:
                    movie_col.image(image_url,width = 200, use_column_width=True)



    #! popular movies deneme

    # popular_movies = meta[['id', 'imdb_id','title','vote_average', 'vote_count']].sort_values(by='vote_average',ascending=False)[:50].reset_index(drop=True)
    # image_urls = [get_image_from_imdb(imdb_id) for imdb_id in popular_movies['imdb_id']]
    # tmdb_tab.title('Popular Movies')






with airbnb_tab:

    airbnb_col1, airbnb_col2, airbnb_col3, airbnb_col4 = airbnb_tab.columns(4)
    selected_neighboorhood = airbnb_col1.selectbox('Neighboord', options= airbnb_data.neighbourhood_group.unique())

    price_min = airbnb_col2.number_input('Min. Price', min_value=0, max_value= airbnb_data.price.max().astype(int), value = 0)
    price_max = airbnb_col2.number_input('Max. Price', min_value=1, max_value = airbnb_data.price.max().astype(int), value= 999)
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
    airrecommend_button = aircol2.button('Recommend AirBnb')


    def recommend_airbnb(user_neighbourhood_group,user_price_range_min,user_price_range_max, user_room_type, user_cancellation_policy, num_neighbors=2,num_recommendations = 500,limit = 3):

        # Kullanıcı kriterlerine göre filtreleme
        filtered_listings = airbnb_data[
            (airbnb_data['neighbourhood_group'] == user_neighbourhood_group) &
            (airbnb_data['price'] >= user_price_range_min) &
            (airbnb_data['price'] <= user_price_range_max) &
            (airbnb_data['room type'] == user_room_type) &
            (airbnb_data['cancellation_policy']==user_cancellation_policy)
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
        filtered_features = filtered_listings[['price', "service fee", 'number of reviews', 'review rate number', 'lat', 'long']]
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
            folium.Marker(
                location=[row['lat'], row['long']],
                popup=f"<strong>{row['NAME']}</strong><br>Price: ${row['price']}<br>Service Fee: ${row['service fee']}<br>Review Rate: {row['review rate number']}<br>Number of Reviews: {row['number of reviews']}",
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
        
            folium_static(map_, width=1400, height=600)


with amazon_tab:
    st.subheader("Sekme 4")
    st.write("Burada Sekme 4 içeriği bulunacak.")

with metacritic_tab:
    st.subheader("Sekme 5")
    st.write("Burada Sekme 5 içeriği bulunacak.")

st.markdown(music_html, unsafe_allow_html=True)

