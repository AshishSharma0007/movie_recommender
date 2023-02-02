import streamlit as st
import pickle
import requests


movies = pickle.load(open('movies_con.pkl','rb'))
similarity_con = pickle.load((open('similarity_con.pkl','rb')))


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{0}?api_key=be6df6e555f848fba7f61656104ff43e&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    ditances = similarity_con[movie_index]
    movies_list = sorted(list(enumerate(ditances)),reverse=True,key=lambda x:x[1])[1:9]

    recommend_movies = []
    recommend_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movies_posters.append(fetch_poster(movie_id))
    return recommend_movies,recommend_movies_posters





st.set_page_config(layout="wide")
st.sidebar.markdown("# CONTENT BASED RECOMMENDER")
st.sidebar.write("This approach filters the items based on the likings of the user. It gives result based on what the user has rated earlier. The method to model this approach is the Vector Space Model (VSM).It derives the similarity of the item from its description and introduces the concept of TF-IDF (Term Frequency-Inverse Document Frequency) In this system we had created a system that takes a single movie input from the user and suggest other movies based on the choice given by the user.In this we have used the cosine singularities technique. this technique helps to create vectors in space of every movie  and we stores the cosine angle difference of each movie with all other movies output is obtained as the most similar movies.")
st.title("Content Based Movies Recommender System")
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
