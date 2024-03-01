import pandas as pd
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_only_movie_title(title:str) -> str:
    title_with_no_symbols = re.sub("[^a-zA-Z0-9]"," ",title)
    title_in_array = title_with_no_symbols.split()

    try:
        if len(title_in_array[-1]) == 4 and int(title_in_array[-1]):
            year_of_title = title_in_array.pop()
        else:
            year_of_title = np.nan
    except:
        year_of_title = np.nan
    new_title = ' '.join(title_in_array)

    return new_title


def get_only_movie_year(title: str) -> str:
    title_with_no_symbols = re.sub("[^a-zA-Z0-9]"," ",title)
    title_in_array = title_with_no_symbols.split()

    try:
        if len(title_in_array[-1]) == 4 and int(title_in_array[-1]):
            year_of_title = title_in_array.pop()
        else:
            year_of_title = np.nan
    except:
        year_of_title = np.nan

    return year_of_title

def search_for_similar_titles(title: str, movies):
    title = get_only_movie_title(title)
    vectorizer = TfidfVectorizer(ngram_range=(1,2))
    tfidf = vectorizer.fit_transform(movies['title'])
    query_vec = vectorizer.transform([title])
    similarity = np.float32(cosine_similarity(query_vec,tfidf).flatten())

    most_similar_ids = np.argpartition(similarity,-10)[-10:]
    most_similar_title = movies.iloc[most_similar_ids][::-1]

    return most_similar_title

def find_similar_movies(movie_id, movies, reviews):
    similar_users = reviews[(reviews['movieId'] == movie_id) & (reviews['rating'] >= 4)]['userId'].unique()
    similar_users_movies = reviews[(reviews['userId'].isin(similar_users)) & (reviews['rating'] >= 4)]['movieId']

    similar_users_movies = similar_users_movies.value_counts() / len(similar_users)
    similar_users_movies = similar_users_movies[similar_users_movies > .1]

    all_users = reviews[(reviews['movieId'].isin(similar_users_movies.index) & (reviews['rating'] >= 4))]
    all_user_movies = all_users['movieId'].value_counts() / len(all_users['userId'].unique())
    recommend_perc = pd.concat([similar_users_movies,all_user_movies],axis=1)
    recommend_perc.columns = ['similar','all']
    recommend_perc['score'] = recommend_perc['similar'] / recommend_perc['all']
    recommend_perc = recommend_perc.sort_values('score',ascending=False)
    return recommend_perc.head(30).merge(movies, left_index=True,right_on='movieId')[['movieId','title','year','genres','score']]

def split_genre(genres):
    genres = genres.split('|')
    return genres

def get_all_genres(df,list_of_all_genres):
    for genres in df['split_genre']:
        for genre in genres:
            list_of_all_genres.append(genre)
    return list_of_all_genres

def check_genre_with_rec(title, genre, movies, reviews):
    results = search_for_similar_titles(title, movies)
    movie_id = results.iloc[0]['movieId']
    rec_movies_all = find_similar_movies(movie_id, movies, reviews)
    if genre == 'All':
        return rec_movies_all.head(6)[['title','year','genres']]

    rec_movies_all['split_genre'] = rec_movies_all['genres'].apply(split_genre)

    index_listing = []

    for index in range(len(rec_movies_all['split_genre'])):
        if genre in rec_movies_all['split_genre'].iloc[index]:
                index_listing.append(rec_movies_all['movieId'].iloc[index])

    index_df = pd.DataFrame(index_listing,columns=['movieId'])
    rec_movies_genre = rec_movies_all[rec_movies_all['movieId'].isin(index_df['movieId'])]
    rec_movies_genre = rec_movies_genre.head(6)[['title','year','genres']]
    return rec_movies_genre
