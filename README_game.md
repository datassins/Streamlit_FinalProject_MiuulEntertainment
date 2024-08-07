# Business Problem:
A recommendation system has been designed to predict the ratings that users would give to games they haven’t played and to suggest games similar to those they have selected. This system primarily uses a content-based filtering approach, where the similarity between games is calculated based on their attributes.

# Solution:
The recommendation system leverages content-based filtering to provide personalized game recommendations. This approach focuses on the attributes of the games themselves to determine similarity and make suggestions.

# Approach:
**Feature Extraction:** Extract relevant features from the game dataset, such as genres, publishers, ratings, and other metadata.

**Vectorization:** Convert the extracted features into a vector representation using techniques like TF-IDF (Term Frequency-Inverse Document Frequency) for text-based attributes and one-hot encoding for categorical attributes.

**Similarity Calculation:** Compute the similarity between games using cosine similarity. This measures the cosine of the angle between two non-zero vectors, providing a similarity score between 0 (no similarity) and 1 (exactly similar).

**Recommendation Generation:** For a given game, find other games with the highest cosine similarity scores and recommend them to the user.

# About Dataset:
The dataset contains information about various games available on Steam, including general information such as release date, platform availability, ratings, and user reviews. The dataset is used to build a recommendation system for predicting user ratings and suggesting similar games.

## Game Information Dataset (content_steam.csv):

The dataset contains the following attributes:

**app_id:** Steam App ID of the game. (e.g., 13500)

**title:** Title of the game. (e.g., Prince of Persia: Warrior Within™)

**date_release:** Release date of the game. (e.g., 2008-11-21)

**win:** Availability on Windows platform (True/False). (e.g., True)

**mac:** Availability on Mac platform (True/False). (e.g., False)

**linux:** Availability on Linux platform (True/False). (e.g., False)

**rating:** User rating of the game. (e.g., Very Positive)

**positive_ratio:** Percentage of positive reviews. (e.g., 84)

**user_reviews:** Number of user reviews. (e.g., 2199)

**price_final:** Final price of the game. (e.g., 9.99)

**price_original:** Original price of the game. (e.g., 9.99)

**discount:** Discount percentage on the game. (e.g., 0.0)

**steam_deck:** Steam Deck compatibility (True/False). (e.g., True)

**overview:** A brief description of the game. (e.g., "Enter the dark underworld of Prince of Persia Warrior Within...")

**header_image:** URL of the header image. (e.g., https://cdn.akamai.steamstatic.com/steam/apps/13500/header.jpg?t=1447351266)

**genres:** Comma-separated list of genres. (e.g., Action, Adventure)

**Publishers:** Publisher of the game. (e.g., Ubisoft)

## Game Information Dataset (most_anticipated_games.csv):

The dataset contains the following attributes:

**Most Anticipated Games:** Title of the game. (e.g., <a href="https://www.gamespot.com/games/the-elder-scrolls-vi/" target="_blank">The Elder Scrolls VI</a>)

**Release Date:** Release date of the game. (e.g., 2008-11-21)

## Game Information Dataset (upcoming_games.csv):

The dataset contains the following attributes:

**Upcoming Games:** Title of the game. (e.g., <a href='https://www.gamespot.com/games/star-wars-outlaws/' target='_blank'>Star Wars Outlaws</a>)

**Release Date:** Release date of the game. (e.g., 2008-11-21)

**Visit our site:** [Miuul Entertainment](https://miuulentertainment.streamlit.app/)
