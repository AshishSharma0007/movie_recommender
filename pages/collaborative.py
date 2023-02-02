import pickle
import streamlit as st
import requests
import pandas as pd
import numpy as np

movies = pickle.load(open('movies_col.pkl','rb'))
similarity = pickle.load(open('similarity_col.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
def id(name):
    tmdbId = movies[movies['title'] == name].tmdbId.values[0]
    return tmdbId

def fetch_poster(tmdbId):
    response = requests.get('https://api.themoviedb.org/3/movie/{0}?api_key=be6df6e555f848fba7f61656104ff43e&language=en-US'.format(tmdbId))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(name):
    tmdbId = movies[movies['title'] == name].tmdbId.values[0]
    index = np.where(pt.index == tmdbId)[0][0]
    similar_movies = sorted(list(enumerate(similarity[index])),key=lambda x:x[1],reverse=True)[1:9]
    movies_list = []
    poster_list = []
    for i in similar_movies:
        movies_list.append(movies[movies['tmdbId'] == pt.index[i[0]]].title.values[0])
        x = id(movies[movies['tmdbId'] == pt.index[i[0]]].title.values[0])
        y = fetch_poster(x)
        poster_list.append(y)
    return movies_list,poster_list


st. set_page_config(layout="wide")
st.sidebar.markdown("# COLLABORATIVE RECOMMENDER")
st.sidebar.write("The collaborative filtering algorithm uses user behavior to select the items to be recommended. These systems are widely used and do not require item metadata like their content-based counterparts. There are different types of collaborating filtering techniques")
st.title("Collaborative Filtering Based Movies Recommender System")
selected = st.selectbox('Select any one movie for Recommendations:',movies['title'].values)


if st.button('Recommend Movies'):
    names,posters = recommend(selected)
    st.header('We recommend you these movies on basis of your choice:')
    for i in range(2):
        col1, col2,col3,col4 = st.columns(4)
        with col1:
            st.subheader(names[0 + 4*i])
            if posters[0 + 4*i]:
                st.image(posters[0 + 4*i],use_column_width='auto')
        with col2:
            st.subheader(names[1 + 4*i])
            if posters[1 + 4*i]:
                st.image(posters[1 + 4*i],use_column_width='auto')
        with col3:
            st.subheader(names[2 + 4*i])
            if posters[2 + 4*i]:
                st.image(posters[2 + 4*i],use_column_width='auto')
        with col4:
            st.subheader(names[3 + 4*i])
            if posters[3 + 4*i]:
                st.image(posters[3 + 4*i],use_column_width='auto')