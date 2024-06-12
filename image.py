import requests

def get_movie_image_url(movie_title):
    # Replace 'YOUR_API_KEY' with your actual TMDb API key
    api_key = '36345046489aba1d9644b024a89e5756'
    base_url = 'https://api.themoviedb.org/3'
    search_url = f'{base_url}/search/movie'

    # Make a request to search for the movie
    response = requests.get(search_url, params={'api_key': api_key, 'query': movie_title})
    data = response.json()

    if 'results' in data and data['results']:
        # Check if the movie title is an exact match
        for result in data['results']:
            if result['title'].lower() == movie_title.lower():
                movie_id = result['id']
                break
        else:
            # If no exact match found, use the first result
            movie_id = data['results'][0]['id']

        # Get movie details
        details_url = f'{base_url}/movie/{movie_id}'
        response = requests.get(details_url, params={'api_key': api_key})
        details_data = response.json()

        # Get poster URL
        if 'poster_path' in details_data and details_data['poster_path']:
            poster_path = details_data['poster_path']
            poster_url = f'https://image.tmdb.org/t/p/original{poster_path}'
            return poster_url
        else:
            return None
    else:
        return None

# # Example usage
# movie_title = 'Cool Hand Luke'
# poster_url = get_movie_image_url(movie_title)
# if poster_url:
#     print(f"Poster URL for '{movie_title}': {poster_url}")
# else:
#     print(f"Poster URL for '{movie_title}' not found.")
