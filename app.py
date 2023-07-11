import streamlit as st
import pandas as pd
import pickle
import requests
import helper


def fetch_poster_id(movie_id):
    response = requests.get(
        "https://api.themoviedb.org/3/movie/{}?api_key=a0e6cfb9d26ccd752369ea3b9821a488&language=en-US".format(
            movie_id))

    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]


st.title("Movies Recommendation System");
movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
similarity = helper.create_similarity_vector(movies)



def recommend_movie(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    recommended_movies = []
    recommended_movies_posters = []
    movies_list = sorted(enumerate(distances), reverse=True, key=lambda x: x[1])[1:6]
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster_id(movies.iloc[i[0]].movie_id))
    return recommended_movies, recommended_movies_posters


selected_movie_name = st.selectbox(
    'Type a movie you want to be recommended',
    movies["title"].values)

if st.button("Recommend"):
    names, posters = recommend_movie(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.write(names[0])
        st.image(posters[0])

    with col2:
        st.write(names[1])
        st.image(posters[1])

    with col3:
        st.write(names[2])
        st.image(posters[2])
    with col4:
        st.write(names[3])
        st.image(posters[3])
    with col5:
        st.write(names[4])
        st.image(posters[4])
