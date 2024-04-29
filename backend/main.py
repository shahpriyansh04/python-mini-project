from flask import Flask, request
import pickle
from flask_cors import CORS, cross_origin

import requests

app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

movies = pickle.load(open('./movie_list.pkl','rb'))
similarity = pickle.load(open('.//similarity.pkl','rb'))

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    movie_match = movies[movies['title'] == movie]
    if movie_match.empty:
        return "Movie not found", []
    index = movie_match.index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return [{'name': name, 'poster': poster} for name, poster in zip(recommended_movie_names, recommended_movie_posters)]   
@app.route("/")
@cross_origin()
def hello_world():
    movie = request.args.get('movie')
    recommendations = recommend(movie)
    print(recommendations)
    return recommendations