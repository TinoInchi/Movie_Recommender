import pandas as pd
import os
from UI_movie_recommender import *



# Main
if __name__ == '__main__':

    # Get Path to Files
    dirname = os.path.dirname(__file__)
    movie_file_name = os.path.join(dirname,'movies.csv')
    reviews_file_name = os.path.join(dirname,'ratings.csv')

    # Read csv Files
    movies = pd.read_csv(movie_file_name)
    reviews = pd.read_csv(reviews_file_name)

    # Adjust & Clean Data
    movies['raw_title'] = movies['title'].apply(get_only_movie_title)
    movies['year'] = movies['title'].apply(get_only_movie_year)
    movies = movies.drop('title',axis=1)
    movies = movies.rename(columns={"raw_title": "title"})
    movies['split_genre'] = movies['genres'].apply(split_genre)

    # Make a list of movie titles

    movie_titles = movies['title'].to_list()

    # Get a List with all Genres
    list_of_all_genres = []
    list_of_all_genres = get_all_genres(movies,list_of_all_genres)
    list_of_all_genres = set(list_of_all_genres)
    list_of_all_genres = ['All'] + list(list_of_all_genres)

    app = MovieRecommenderApp(list_of_all_genres,movie_titles, movies, reviews)
    app.mainloop()