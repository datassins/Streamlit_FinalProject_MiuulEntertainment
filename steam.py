import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
from bs4 import BeautifulSoup
pd.set_option('colheader_justify', 'left')

upcoming_games_df = pd.read_csv("upcoming_games.csv")
df_most_anticipated_games = pd.read_csv("most_anticipated_games.csv")

upcoming_games_df['Release Date'] = pd.to_datetime(upcoming_games_df['Release Date'])
upcoming_games_df = upcoming_games_df.sort_values('Release Date', ascending=False)

df_most_anticipated_games['Release Date'] = pd.to_datetime(df_most_anticipated_games['Release Date'])
df_most_anticipated_games = df_most_anticipated_games.sort_values('Release Date', ascending=False)


def get_image_from_steam(steam_id):
    url = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{steam_id}/header.jpg"
    response = requests.get(url)
    if response.status_code == 200:
        return url
    else:
        return None
    
def render_fixed_size_table(df, table_height=400, table_width=250):
    html_table = df.to_html(escape=False, index=False)
    html_code = f"""
    <div style="height:{table_height}px; width:{table_width}px; overflow:auto;">
        {html_table}
    </div>
    """
    return html_code

# Sayfa ayarları
st.set_page_config(layout='wide', page_title='Game Recommender', page_icon="🦈")

# Load the data
game = pd.read_csv('content_steam.csv')


@st.cache_data
def calculate_cosine_sim(dataframe):
    tfidf = TfidfVectorizer(stop_words='english')
    dataframe['overview'] = dataframe['overview'].fillna('')
    tfidf_matrix = tfidf.fit_transform(dataframe['overview'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cosine_sim

cosine_sim_game = calculate_cosine_sim(game)

st.markdown(
    """
    <style>
    .stApp {
        margin: 0;
        padding: 0;
    }
    .css-18e3th9 {
        gap: 0 !important;
    }
    .css-1cpxqw2 {
        padding: 0 !important;
        margin: 0 !important;
    }
    .resizable-image {
        padding: 0;
        margin: 0;
    }
    .resizable-image img {
        width: 100%;
        height: 400px;
        display: block;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3, col4, col5 = st.columns(5)

col1.markdown(
    """
    <div class="resizable-image">
        <img src="https://media1.tenor.com/m/t1KbzWJ9sGkAAAAd/elden-ring-action-rpg.gif" alt="Resim">
    </div>
    """,
    unsafe_allow_html=True,
)

col2.markdown(
    """
    <div class="resizable-image">
        <img src="https://media1.tenor.com/m/Z5t0eehZn3gAAAAd/darksiders_2-prince-of-persia.gif" alt="Resim">
    </div>
    """,
    unsafe_allow_html=True,
)

col3.markdown(
    """
    <div class="resizable-image">
        <img src="https://media1.tenor.com/m/sctssthXIm8AAAAC/play-game.gif" alt="Resim">
    </div>
    """,
    unsafe_allow_html=True,
)

col4.markdown(
    """
    <div class="resizable-image">
        <img src="https://media1.tenor.com/m/BDValJzc6P4AAAAC/rdr2.gif" alt="Resim">
    </div>
    """,
    unsafe_allow_html=True,
)

col5.markdown(
    """
    <div class="resizable-image">
        <img src="https://media1.tenor.com/m/COG1mdmj0X0AAAAd/swtor-the-old-republic.gif" alt="Resim">
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style="text-align: center;">
        <h1 style="color: #A0622D ;">Discover a New World</h1>
        <hr style="border: none; border-top: 2px solid #A0622D;">
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div style="text-align: center;">
        <h1 style="color: #999999 ; font-size: 20px;">Level up your gaming experience with our curated game recommendations. From action-packed adventures to mind-bending puzzles, find the perfect game to keep you entertained for hours.</h1>
        <hr style="border: none; border-top: 2px solid #A0622D;">
    </div>
    """,
    unsafe_allow_html=True,
)

if 'active_tab' not in st.session_state:
    st.session_state['active_tab'] = 'Home'

def set_active_tab(tab_name):
    st.session_state['active_tab'] = tab_name






home_tab, steam_tab = st.tabs(["Home", "Recommender"])

with home_tab.container():
    set_active_tab('Home')

with home_tab:
        home_tab.markdown(
        """
        <div class="title-background">Game News</div>
        <div class="custom-divider"></div>
        """,
        unsafe_allow_html=True,
    )
        home_tab.write("")
        home_tab.write("")
        home_tab.write("")
        home_tab.write("")
        home_tab.write("")
        home_tab.write("")

home_tab.markdown(
    """
    <style>
    .title-background {
        background-color: #A0622D;
        color: black; /* Text color */
        padding: 10px;
        text-align: center; 
        border-radius: 100px;
        font-size: 32px;
        font-weight: bold; 
    }
    .upcoming-games-table {
        background-color: #54649;
        color: white ; /* Text color */
        padding: 5px; 
        text-align: center;
        font-size: 15px;
        font-weight: bold; 
    }
    @media (max-width: 1200px) {
        iframe {
            height: 300px; 
        }
        .title-background {
            font-size: 24px; /* Daha küçük ekranlar için font boyutu */
            padding: 8px; /* Daha küçük ekranlar için padding */
        }
    }
    @media (max-width: 768px) {
        iframe {
            height: 200px; /* Daha küçük ekranlar için iframe yüksekliği */
        }
        .title-background {
            font-size: 18px; /* Daha küçük ekranlar için font boyutu */
            padding: 6px; /* Daha küçük ekranlar için padding */
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

col1, col2= home_tab.columns([1, 1])

col1.markdown(
    """
    <iframe width="100%" height="420" src="https://www.youtube.com/embed/iaJ4VVFGIa8" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    """,
    unsafe_allow_html=True
)

col2.markdown(
    """
    <iframe width="100%" height="420" src="https://www.youtube.com/embed/kfYEiTdsyas" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    """,
    unsafe_allow_html=True
)


home_tab.write("")
home_tab.write("")
home_tab.write("")
home_tab.write("")
home_tab.write("")
home_tab.write("")


# İkinci satırdaki sütunlar
col1, col2 = home_tab.columns([1, 1])

if not upcoming_games_df.empty:
    col1.markdown('<div class="upcoming-games-table">' + render_fixed_size_table(upcoming_games_df, 420, col1.width) + '</div>', unsafe_allow_html=True)
else:
    col1.write("No upcoming games found.")

if not df_most_anticipated_games.empty:
    col2.markdown('<div class="upcoming-games-table">' + render_fixed_size_table(df_most_anticipated_games, 420, col3.width) + '</div>', unsafe_allow_html=True)
else:
    col2.write("No most anticipated games found.")






home_tab.markdown('<div class="title-background">Play a Game</div>', unsafe_allow_html=True)






home_tab.write("")
home_tab.write("")
home_tab.write("")
home_tab.write("")





home_tab.markdown(
    """
    <style>
    .iframe-container {
        width: 850px; /* Aynı genişlik */
        height: 500px;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-left: auto; /* Ortalamak için */
        margin-right: auto; /* Ortalamak için */
    }
    .iframe-container iframe {
        width: 1000px; /* Aynı genişlik */
        height: 100%;
        border: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
    
home_tab.markdown(
    """
    <div class="iframe-container">
        <iframe src="https://games.construct.net/1690/latest"></iframe>
    </div>
    """,
    unsafe_allow_html=True,
)


home_tab.write("")
home_tab.write("")
home_tab.write("")
home_tab.write("")
home_tab.write("")
home_tab.write("")

home_tab.markdown('<div class="title-background">Discover Your Next Adventure!</div>', unsafe_allow_html=True)
home_tab.write("")
home_tab.write("")

with home_tab.container(): 

    col1, col2, col3, col4, col5, col6 = st.columns([1, 0.45, 0.45, 0.45, 1,0.5], gap='large')

    # ! airbnb column
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

    # ! anime column
    image_anime = "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExN2NrbXY3a3ptbDY0d256N2dtN2xkOTV1eXpnMGpvbG5obWlla29mZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/11KzOet1ElBDz2/giphy.webp"
    redirect_anime = "https://animerecommendations.streamlit.app/"

    html_anime = f"""
    <div style="position: relative; width: 150px; height: 150px;">
        <a href="{redirect_anime}" target="_blank">
            <img src="{image_anime}" style="width:150px;height:150px;">
            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; background: rgba(0, 0, 0, 0.5); color: white; font-size: 15px; font-weight: bold;">ANIME</div>
        </a>
    </div>
    """
    col5.markdown(html_anime, unsafe_allow_html=True)






# Steam Tab
with steam_tab:
    def content_based_recommender_game(title, cosine_sim_game, dataframe):
        indices = pd.Series(dataframe.index, index=dataframe['title'])
        indices = indices[~indices.index.duplicated(keep='last')]
        game_index = indices[title]
        similarity_scores = cosine_sim_game[game_index]
        similarity_scores_df = pd.DataFrame(similarity_scores, index=dataframe.index, columns=["score"])
        game_indices = similarity_scores_df.sort_values(by="score", ascending=False).index[1:11]
        return dataframe.loc[game_indices]


    if 'selected_game' not in st.session_state:
        st.session_state.selected_game = None

    if 'filter_by_genre' not in st.session_state:
        st.session_state.filter_by_genre = None

    if 'recommendations_df' not in st.session_state:
        st.session_state.recommendations_df = None

    # Seçim kutusu ve butonu aşağıya taşıma
    game_options = ["Choose a Game"] + list(game.title.unique())
    selected_game = st.selectbox('Choose a game you like.', options=game_options, index=0)

    if selected_game != "Choose a Game":
        st.write("Would you like to filter the recommendations by genre?")
        filter_by_genre = st.radio("Filter by genre?", ("No", "Yes"), index=0)

        if filter_by_genre == "Yes":
            st.session_state.filter_by_genre = True
            genre_options = ['Action', 'Adventure', 'Casual', 'Indie', 'Racing', 'RPG', 'Simulation', 'Sports', 'Strategy',
                            'Massively Multiplayer']
            selected_genre = st.multiselect('Select Genres', options=genre_options)
        else:
            st.session_state.filter_by_genre = False

        # Stil ayarları
        st.markdown("""
            <style>
            .stButton button {
                background-color: #a3c9f1 !important;
                color: blue !important;
                padding: 10px 24px !important;
                border: none !important;
                cursor: pointer !important;
                text-align: center !important;
                font-size: 16px !important;
                border-radius: 5px !important;
            }
            </style>
        """, unsafe_allow_html=True)

        show_recommendations = st.button('Show Recommendations')

        if show_recommendations and selected_game != "Choose a Game":
            st.session_state.selected_game = selected_game
            try:
                st.session_state.recommendations_df = content_based_recommender_game(title=selected_game,
                                                                                    cosine_sim_game=cosine_sim_game,
                                                                                    dataframe=game)

                if st.session_state.filter_by_genre and selected_genre:
                    genre_pattern = '|'.join(selected_genre)
                    filtered_recommendations_df = st.session_state.recommendations_df[
                        st.session_state.recommendations_df['genres'].str.contains(genre_pattern, na=False)]

                    if filtered_recommendations_df.empty:
                        st.warning("There is no result for these genres.")
                    else:
                        for index, game_row in enumerate(filtered_recommendations_df.itertuples()):
                            if index < 5:
                                if index == 0:
                                    cols = st.columns(5)
                                game_col = cols[index % 5]
                                game_id = game_row.app_id
                                game_title = game_row.title
                                game_rating = game_row.rating  # Rating kolonunu ekle
                                game_col.markdown(
                                    f"<a href='https://store.steampowered.com/app/{game_id}' target='_blank'><img src='{get_image_from_steam(game_id)}' style='max-width:100%;'></a>",
                                    unsafe_allow_html=True)
                                game_col.subheader(f"**{game_title}**", divider="violet")
                                game_col.write(f"Rating: {game_rating}")
                            elif index < 10:
                                if index == 5:
                                    cols = st.columns(5)
                                game_col = cols[index % 5]
                                game_id = game_row.app_id
                                game_title = game_row.title
                                game_rating = game_row.rating  # Rating kolonunu ekle
                                game_col.markdown(
                                    f"<a href='https://store.steampowered.com/app/{game_id}' target='_blank'><img src='{get_image_from_steam(game_id)}' style='max-width:100%;'></a>",
                                    unsafe_allow_html=True)
                                game_col.subheader(f"**{game_title}**", divider="violet")
                                game_col.write(f"Rating: {game_rating}")
                else:
                    for index, game_row in enumerate(st.session_state.recommendations_df.itertuples()):
                        if index < 5:
                            if index == 0:
                                cols = st.columns(5)
                            game_col = cols[index % 5]
                            game_id = game_row.app_id
                            game_title = game_row.title
                            game_rating = game_row.rating
                            game_col.markdown(
                                f"<a href='https://store.steampowered.com/app/{game_id}' target='_blank'><img src='{get_image_from_steam(game_id)}' style='max-width:100%;'></a>",
                                unsafe_allow_html=True)
                            game_col.subheader(f"**{game_title}**", divider="violet")
                            game_col.write(f"Rating: {game_rating}")
                        elif index < 10:
                            if index == 5:
                                cols = st.columns(5)
                            game_col = cols[index % 5]
                            game_id = game_row.app_id
                            game_title = game_row.title
                            game_rating = game_row.rating
                            game_col.markdown(
                                f"<a href='https://store.steampowered.com/app/{game_id}' target='_blank'><img src='{get_image_from_steam(game_id)}' style='max-width:100%;'></a>",
                                unsafe_allow_html=True)
                            game_col.subheader(f"**{game_title}**", divider="violet")
                            game_col.write(f"Rating: {game_rating}")
            except KeyError:
                st.error("Please select a valid game.")

