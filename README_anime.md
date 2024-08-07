# Business Problem:

A recommendation system has been designed to predict the ratings that users would give to anime they haven’t watched and to suggest films similar to those they have selected.

# About Dataset:

Recommendation data at myanimelist.net. This dataset contains information about anime and the preference from different users.

anime_filtered csv:

contain general information of every anime like genre, stats, studio, etc. 
The main dataset contains the following contents. 
The features needed specifically for the project / their transformed versions can be found in the file. The new ‘Features’ attribute has been created by combining a few of the following attributes.

	 •	MAL_ID: MyAnimeList ID of the anime. (e.g., 1)
	 •	Score: Average score given by all users in the MyAnimeList database. (e.g., 8.78)
	 •	Genres: Comma-separated list of the anime’s genres. (e.g., Action, Adventure, Comedy, Drama, Sci-Fi, Space)
	 •	English name: Full English name of the anime. (e.g., Cowboy Bebop)
	 •	Japanese name: Full Japanese name of the anime. (e.g., カウボーイビバップ)
	 •	Type: TV, movie, OVA, etc. (e.g., TV)
	 •	Episodes: Number of episodes. (e.g., 26)
	 •	Aired: Airing date. (e.g., April 3, 1998 - April 24, 1999)
	 •	Premiered: Season premiere. (e.g., Spring 1998)
	 •	Producers: Comma-separated list of producers. (e.g., Bandai Visual)
	 •	Licensors: Comma-separated list of licensors. (e.g., Funimation, Bandai Entertainment)
	 •	Studios: Comma-separated list of studios. (e.g., Sunrise)
	 •	Source: Source material (Manga, Light novel, Book, etc.). (e.g., Original)
	 •	Duration: Duration per episode. (e.g., 24 min per episode)
	 •	Rating: Age rating. (e.g., R - 17+ (violence & profanity))
	 •	Ranked: Ranking position by score. (e.g., 28)
	 •	Popularity: Ranking position by the number of users who added the anime to their lists. (e.g., 39)
	 •	Members: Number of community members in this anime group. (e.g., 1,251,960)
	 •	Favorites: Number of users who added the anime to their ‘favorites’. (e.g., 61,971)
	 •	Watching: Number of users watching the anime. (e.g., 105,808)
	 •	Completed: Number of users who completed the anime. (e.g., 718,161)
	 •	On-Hold: Number of users who put the anime ‘on hold’. (e.g., 71,513)
	 •	Dropped: Number of users who dropped the anime. (e.g., 26,678)
	 •	Plan to Watch: Number of users who plan to watch the anime. (e.g., 329,800)
	 •	Score-10: Number of users who gave a score of 10. (e.g., 229,170)
	 •	Score-9: Number of users who gave a score of 9. (e.g., 182,126)
	 •	Score-8: Number of users who gave a score of 8. (e.g., 131,625)
	 •	Score-7: Number of users who gave a score of 7. (e.g., 62,330)
	 •	Score-6: Number of users who gave a score of 6. (e.g., 20,688)
	 •	Score-5: Number of users who gave a score of 5. (e.g., 8,904)
	 •	Score-4: Number of users who gave a score of 4. (e.g., 3,184)
	 •	Score-3: Number of users who gave a score of 3. (e.g., 1,357)
	 •	Score-2: Number of users who gave a score of 2. (e.g., 741)
	 •	Score-1: Number of users who gave a score of 1. (e.g., 1,580)
	
 rating_complete_filtered csv:
 
 This dataset only considers animes that the user has watched completely (watching_status==2) and gave it a score (score!=0)

 This file have the following columns:
 
	 •	user_id: non identifiable randomly generated user id.
	 •	anime_id: - MyAnimelist ID of the anime that this user has rated.
	 •	rating: rating that this user has assigned.

**Visit our site:** [Miuul Entertainment](https://miuulentertainment.streamlit.app/)


