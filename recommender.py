import numpy as np
import pandas as pd
import re

column_names = ['user_id', 'item_id', 'rating', 'timestamp']
df = pd.read_csv('u.data', sep='\t', names=column_names)

movie_titles = pd.read_csv("Movie_Id_Titles")

df = pd.merge(df, movie_titles, on='item_id')

ratings = pd.DataFrame(df.groupby('title')['rating'].mean())
ratings['num of ratings'] = pd.DataFrame(df.groupby('title')['rating'].count())

moviemat = df.pivot_table(index='user_id', columns='title', values='rating')


#Function
def recommend_movie(movie):
    # Convert movie title to lowercase for case-insensitive search
    movie = movie.lower()
    
    # Get the movie title matching the input (ignoring case)
    matching_titles = [title for title in moviemat.columns if movie in title.lower()]
    if not matching_titles:
        return {}  # Return empty dictionary if no matching title found
    
    # Select the first matching title (assuming there's only one exact match)
    movie = matching_titles[0]
    
    movie_user_ratings = moviemat[movie]

    similar_to_movie = moviemat.corrwith(movie_user_ratings)
    corr_movie = pd.DataFrame(similar_to_movie, columns=['Correlation'])
    corr_movie = corr_movie.join(ratings['num of ratings'])

    corr_movie = corr_movie[corr_movie['num of ratings'] > 100].sort_values('Correlation', ascending=False).head(20)
    # Remove the year pattern from movie titles
    corr_movie.index = corr_movie.index.map(lambda x: re.sub(r'\s*\(\d{4}\)', '', x))
    result_dict = corr_movie['Correlation'].to_dict()  # Convert the correlation Series to a dictionary
    return result_dict

recommendations = recommend_movie('The god father')
for title, correlation in recommendations.items():
    print(f"Movie: {title}, Correlation: {correlation}")
