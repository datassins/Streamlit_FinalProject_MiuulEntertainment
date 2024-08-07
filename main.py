import streamlit as st
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests


def get_image_from_book(url_id):
    url = f"https://books.google.nl/books/publisher/content?id={url_id}&printsec=frontcover&img=1&zoom=1"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return url
    else:
        print(f"Failed to retrieve image for {url_id}, Status Code: {response.status_code}")
        return None


st.set_page_config(layout='wide', page_title='Book Recommendation', page_icon = "📚" )


@st.cache_data
def load_data(path):
    return pd.read_csv(path)


book = load_data('book_recommendation.csv')

bestsellers = load_data('bestsellers.csv')


@st.cache_data
def calculate_cosine_sim_book(dataframe):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(dataframe['Combined'])
    cosine_sim_book = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cosine_sim_book


cosine_sim_book = calculate_cosine_sim_book(book)


def home():
    # Bestsellers section
    st.markdown(
        """
        <div class="bestsellers">
            <h1 style='color: #CD5C5C;'>Bestsellers</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

    best_1, best_2, best_3, best_4, best_5, best_6, best_7, best_8, best_9, best_10 = st.columns(10)

    for index, book_col in enumerate([best_1, best_2, best_3, best_4, best_5, best_6, best_7, best_8, best_9, best_10]):
        if index < len(bestsellers):
            book_row = bestsellers.iloc[index]
            book_id = book_row['new_url_id']
            preview_link = book_row['previewLink']
            book_col.markdown(f"""
                            <div style='display: flex; flex-direction: column; align-items: center;'>
                                <div style='height: 250px; display: flex; justify-content: center; align-items: center; flex-wrap: wrap;'>
                                <a href='{preview_link}' target='_blank'>
                                    <img src='{get_image_from_book(book_id)}' style='width:150px; height:200px; object-fit: 
                                    contain; display: block; margin: 10px;'/>
                                </a>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)

    #Hero section
    st.markdown(
        """
        <style>
        .hero { 
            background-color: #E9967A;
            text-align: center;
            flex-direction: column;
            padding: 40px;
            border-radius: 10px;
            margin-bottom: 20px;
            position: relative;
        }
        .hero h1 {
            font-family: "Times New Roman", Times, serif;
            font-size: 48px;
            color:  #F5F3D9;
            font-weight: bold;
        }
        .hero p {
            font-family: "Times New Roman", Times, serif;
            font-size: 18px;
            color: #F5F3D9;
            margin-top: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


    st.markdown(
        """
        <div class="hero">
            <h1>Find Your Next Favorite Book</h1>
            <p>Get ready for a world of amazing stories! We've handpicked some of the most captivating books just for you. 
            Whether you're into heart-pounding mysteries, swoon-worthy romances or mind-bending sci-fi, we've got something 
            that'll keep you hooked. Let's find your next favorite read together!</p> 
        </div>
        """,
        unsafe_allow_html=True,
    )

    #Explore Button section
    st.markdown(
        """
        <style>
        .stButton > button {
            background-color: #E9967A; 
            font-family: "Times New Roman", Times, serif;
            color: #F5F3D9;
            border: 2px solid black; 
            transition: color 0.3s, border-color 0.3s; 
            text-align: left;
            width: 100%;
            padding: 10px;
            border-radius: 100px;
            justify-content: center;
            align-items: left;
            margin: 0;
            cursor: pointer;
        }
        .stButton > button:hover {
            color:  #CD5C5C; 
            border-color: #CD5C5C; 
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    def switch_page(page_name):
        st.session_state.page = page_name


    if st.button('Explore Now'):
        switch_page('explore')

    st.markdown("<hr style='border: 1px solid #CD5C5C;'>", unsafe_allow_html=True)


    st.container().markdown("<br>", unsafe_allow_html=True)

    ############## home page diger seceneklerin gosterimi  ##############


    col1, col2, col3, col4, col5, col6 = st.container().columns([1, 0.45, 0.45, 0.45, 1, 0.5], gap='large')

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

    # ! airbnb column
    image_amazon = "https://media1.tenor.com/m/rsSIoLjds9UAAAAC/airbnb-door.gif"
    redirect_amazon = "https://airbnbrecommendations.streamlit.app/"
    html_amazon = f"""
        <div style="position: relative; width: 150px; height: 150px;">
            <a href="{redirect_amazon}" target="_blank">
                <img src="{image_amazon}" style="width:150px;height:150px;">
                <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; background: rgba(0, 0, 0, 0.5); color: white; font-size: 15px; font-weight: bold;">AIRBNB</div>
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

    st.markdown("<hr style='border: 1px solid #CD5C5C;'>", unsafe_allow_html=True)


def explore():
    # Bestsellers section

    st.markdown(
        """
        <style>
        .chooce_book {
            background-color: #F5F3D9;  
            padding: 5px;  
            border-radius: 10px;
            display: flex;
            justify-content: center; 
            align-items: center;  
            height: 50px;  
        }
        .chooce_book h1 {
            color: #CD5C5C; 
            font-family: "Times New Roman", Times, serif;
            font-size: 40px;  
            margin: 0;  
            text-align: center;  
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="chooce_book">
            <h1 style='color: #F5F3D9; font-family: "Times New Roman", Times, serif;' >Bestsellers</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<hr style='border: 1px solid #CD5C5C;'>", unsafe_allow_html=True)


    best_1, best_2, best_3, best_4, best_5, best_6, best_7, best_8, best_9, best_10 = st.columns(10)

    for index, book_col in enumerate([best_1, best_2, best_3, best_4, best_5, best_6, best_7, best_8, best_9, best_10]):
        if index < len(bestsellers):
            book_row = bestsellers.iloc[index]
            book_id = book_row['new_url_id']
            preview_link = book_row['previewLink']
            book_col.markdown(f"""
                                        <div style='display: flex; flex-direction: column; align-items: center;'>
                                            <div style='height: 250px; display: flex; justify-content: center; align-items: center; flex-wrap: wrap;'>
                                            <a href='{preview_link}' target='_blank'>
                                                <img src='{get_image_from_book(book_id)}' style='width:150px; height:200px; object-fit: 
                                                contain; display: block; margin: 10px;'/>
                                            </a>
                                            </div>
                                        </div>
                                    """, unsafe_allow_html=True)
    st.markdown(
        """
        <style>
        .chooce_book {
            background-color: #E9967A;   
            padding: 5px;  
            border-radius: 10px;
            display: flex;
            justify-content: center; 
            align-items: center;  
            height: 50px;  
        }
        .chooce_book h1 {
            color: #F5F3D9;
            font-family: "Times New Roman", Times, serif;
            font-size: 40px;  / Yazı boyutunu küçültün /
            margin: 0;  / Başlık etrafındaki varsayılan boşlukları kaldırın /
            text-align: center;  / Metni ortalayın */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="chooce_book">
            <h1 style='color: #F5F3D9; font-family: "Times New Roman", Times, serif;'> Find Your Next Favorite Book!</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<hr style='border: 1px solid #CD5C5C;'>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)


    def content_based_recommender_book(title, cosine_sim_book, dataframe):
        indices = pd.Series(dataframe.index, index=dataframe['Title']).drop_duplicates()
        book_index = indices[title]
        similarity_scores = pd.DataFrame(cosine_sim_book[book_index], columns=["score"])
        book_indices = similarity_scores.sort_values("score", ascending=False)[1:13].index
        last_df = dataframe[['Title', "review/score", "new_url_id"]].iloc[book_indices].sort_values('review/score', ascending=False)[0:10]
        return last_df[["Title", "review/score", "new_url_id"]]


    book_col1, book_col2, book_col3 = st.columns([1, 2, 1])
    amazoncol1, amazoncol2, amazoncol3 = st.columns([2, 1, 2], gap='large')
    recommend_button = amazoncol2.button('Recommend a Book')


    selected_book = book_col2.selectbox('Choose a book you like.', options=["Choose a book"] + book.Title.unique().tolist())

    if selected_book == "Choose a book":
        selected_book = None

    recommendations_df = None

    if selected_book is not None:
        recommendations_df = content_based_recommender_book(title=selected_book, cosine_sim_book=cosine_sim_book, dataframe=book)

    if recommendations_df is not None:
        book_1, book_2, book_3, book_4, book_5 = st.columns(5)
        book_6, book_7, book_8, book_9, book_10 = st.columns(5)

    if selected_book is not None and recommend_button:
        for index, book_col in enumerate([book_1, book_2, book_3, book_4, book_5, book_6, book_7, book_8, book_9, book_10]):
            if index < len(recommendations_df):
                book_row = recommendations_df.iloc[index]
                book_id = book_row['new_url_id']
                book_title = book_row['Title']
                book_score = book_row["review/score"]
                book_score = np.dot(book_score, np.random.uniform(0.95, 0.98))

              #
                site_url = f'https://books.google.pl/books?id={book_id}'


                book_col.markdown(f"""
                                                        <div style='display: flex; flex-direction: column; align-items: center;'>
                                                            <div style='height: 300px; display: flex; align-items: center;'>
                                                                <a href="{site_url}" target="_blank">
                                                                <img src='{get_image_from_book(book_id)}' style='width:150px; height:200px; object-fit: contain; display: block;'/>
                                                                </a>
                                                            </div>
                                                            <div style='height: 60px; display: flex; align-items: center;'>
                                                                <h3 style='text-align: center; font-size: 15px;'>{book_title}</h3>
                                                            </div>
                                                            <div style='height: 20px; display: flex; align-items: center;'>
                                                               <p style='text-align: center; font-size: 15px;'>Rating: {book_score:.2f} </p>
                                                            </div>
                                                        </div>
                                                    """, unsafe_allow_html=True)

    else:
        if recommend_button:
            st.warning("Please choose a book from the list.")


if 'page' not in st.session_state:
    st.session_state.page = 'home'

if st.session_state.page == 'home':
    home()
elif st.session_state.page == 'explore':
    explore()
