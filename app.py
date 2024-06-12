from flask import Flask, render_template, request
from recommender import recommend_movie
from image import get_movie_image_url
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_movie():
    movie_title = request.form['movie_title']
    print(movie_title)
    related_movies = []
    recommendations = recommend_movie(movie_title)
    if recommendations:
        for title, correlation in recommendations.items():
            print(f"Movie: {title}, Correlation: {correlation}")
            movie_image=get_movie_image_url(title)
            related_movies.append({'name': title, 'image': movie_image})
        main_movie_image=get_movie_image_url(movie_title)
        return render_template('result.html',main_movie_image=main_movie_image,related_movies=related_movies)
    else:
        return render_template('not_found.html')

if __name__ == '__main__':
    app.run(debug=True)
