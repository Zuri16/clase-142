from flask import Flask, jsonify, request
from demographic_filtering import output
from content_filtering import get_recommendations
import pandas as pd

movies_data = pd.read_csv('final.csv')

app = Flask(__name__)

all_movies = movies_data[["original_title","poster_link","release_date","runtime","weighted_rating"]]

liked_movies = []
not_liked_movies = []
did_not_watch = []

def assign_val():
    m_data = {
        "original_title": all_movies.iloc[0,0],
        "poster_link": all_movies.iloc[0,1],
        "release_date": all_movies.iloc[0,2] or "N/A",
        "duration": all_movies.iloc[0,3],
        "rating":all_movies.iloc[0,4]/2
    }
    return m_data

@app.route("/movies")
def get_movie():
    movie_data = assign_val()

    return jsonify({
        "data": movie_data,
        "status": "success"
    })

@app.route("/like")
def liked_movie():
    global all_movies
    movie_data=assign_val()
    liked_movies.append(movie_data)
    all_movies.drop([0], inplace=True)
    all_movies = all_movies.reset_index(drop=True)
    return jsonify({
        "status": "success"
    })

# api para devolver la lista de películas que le gustan
@app.route("/liked")
def lik_movie():
    global liked_movies
    return jsonify({
        "data":liked_movies,
        "status":"success"
    })


@app.route("/dislike")
def unliked_movie():
    global all_movies

    movie_data=assign_val()
    not_liked_movies.append(movie_data)
    all_movies.drop([0], inplace=True)
    all_movies=all_movies.reset_index(drop=True)
    
    return jsonify({
        "status": "success"
    })

@app.route("/did_not_watch")
def did_not_watch_view():
    global all_movies

    movie_data=assign_val()
    did_not_watch.append(movie_data)
    all_movies.drop([0], inplace=True)
    all_movies=all_movies.reset_index(drop=True)
    
    return jsonify({
        "status": "success"
    })

# api para devolver películas populares
@app.route("/popular")
def popular_movies():
    pelis_populares=[]
    for x,y in output.iterrows():
        data = {
        "original_title": y['original_title'],
        "poster_link": y['poster_link'],
        "release_date": y['release_date'] or "N/A",
        "duration": y['runtime'],
        "rating":y['weighted_rating']/2
        }
        pelis_populares.append(data)
    return jsonify({
        "data":pelis_populares,
        "status":"success"
    })

# api para devolver una lista de películas recomendadas
@app.route("/recomended")
def recomendado():
    global liked_movies
    colums_names = ["original_title","poster_link","release_date","runtime","weighted_rating"]
    all_columns=pd.DataFrame(columns=colums_names)
    for x in liked_movies:
        recomen=get_recommendations(x["original_title"])
        all_columns=all_columns.append(recomen)
    all_columns.drop_duplicates(subset=["original_title"],inplace=True)
    pelis_populares=[]
    for x,y in all_columns.iterrows():
        data = {
        "original_title": y['original_title'],
        "poster_link": y['poster_link'],
        "release_date": y['release_date'] or "N/A",
        "duration": y['runtime'],
        "rating":y['weighted_rating']/2
        }
        pelis_populares.append(data)
    return jsonify({
        "data":pelis_populares,
        "status":"success"
    })


if __name__ == "__main__":
  app.run()
