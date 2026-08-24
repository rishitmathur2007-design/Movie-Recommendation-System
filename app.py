import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):

    url = "https://api.themoviedb.org/3/movie/{}?api_key=2f8e4b3c1d0eb7344b6ae9c9bd5f69fc&language=en-US".format(movie_id)
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyZjhlNGIzYzFkMGViNzM0NGI2YWU5YzliZDVmNjlmYyIsIm5iZiI6MTc4NzU5NTQyMy4zMTIsInN1YiI6IjZhOGM4YTlmMzkxZmU3MGQ4YzJhMjgzOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.iaALq02bVDhOVqBndSi-voXx9KzwDfcGuzeullzXZT8"
    }
    
    response = requests.get(url, headers=headers)
    response=response.json()
    poster_path=response['poster_path']
    full_path="https://image.tmdb.org/t/p/w500/"+poster_path
    return full_path
     
def recommend(movie):
    index=movies[movies['title'] == movie].index[0]
    distance=sorted(list(enumerate(similarity[index])), reverse=True,key= lambda x: x[1])
    recommended_movie_name=[]
    recommended_movie_poster=[ ]
    for i in distance[1:6]:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movie_poster.append(fetch_poster(movie_id))
        recommended_movie_name.append(movies.iloc[i[0]].title)
    return recommended_movie_name,recommended_movie_poster

st.header("Movie Recommendation System Using Machine Learning ")
movies=pickle.load(open("data/movie_list.pickle",'rb'))
similarity=pickle.load(open('data/similarity.pickle','rb'))
movies_list=movies['title'].values
selected_movie=st.selectbox("Type/Select Move name to get recomendation",movies_list)
if st.button("Show Recommendation"):
    recommended_movie_name,recommended_movie_poster=recommend(selected_movie)
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.text(recommended_movie_name[0])
        st.image(recommended_movie_poster[0])

    with col2:
            st.text(recommended_movie_name[1])
            st.image(recommended_movie_poster[1])

    with col3:
            st.text(recommended_movie_name[2])
            st.image(recommended_movie_poster[2])

    with col4:
            st.text(recommended_movie_name[3])
            st.image(recommended_movie_poster[3])

    with col5:
            st.text(recommended_movie_name[4])
            st.image(recommended_movie_poster[4])


        