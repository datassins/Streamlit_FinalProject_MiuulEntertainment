# Miuul Entertainment - Movie Recommendation and Image Scraping

This repository contains the movie recommendation system and a script to scrape movie images from IMDb. These are key components of the Miuul Entertainment site.

## Overview

Miuul Entertainment offers personalized movie recommendations and visually rich content sourced from IMDb. 

**Visit our site:** [Miuul Entertainment](https://miuulentertainment.streamlit.app/)

## Movie Recommendation System

The movie recommendation system uses content-based filtering to suggest movies similar to the ones you like.

### Files

- `imdb_main.py`: Streamlit application file for the movie recommendation system.
- `movie_recommendation_file.csv`: CSV file containing movie metadata.

### Main Features

- **Personalized Recommendations:** The system analyzes movie metadata and provides recommendations based on the selected movie's content.
- **Rich Visuals:** Access movie posters and details via IMDb.

### How It Works

Users can select a movie they like from the Streamlit app. The system provides a list of similar movies based on the movie's overview, title, and genres.

## IMDb Image Scraping

The `scrape.py` script fetches movie images from IMDb using IMDb IDs.

### Files

- `scrape.py`: Script for scraping movie images from IMDb.

### Main Features

- **Fetch Movie Images:** Retrieve high-quality movie posters directly from IMDb using the movie's IMDb ID.

## Additional Information

This repository is a part of the larger Miuul Entertainment project, which includes various entertainment recommendations. Explore our [site](https://miuulentertainment.streamlit.app/) for more!

## License

This project is licensed under the MIT License. See the LICENSE file for more information.
