import streamlit as st
import pickle
import pandas as pd
import numpy as np

movies_list_ = pickle.load(open("movie_list.pkl", "rb"))
model = pickle.load(open("model.pkl", "rb"))
book_pivot = pickle.load(open("book_pivot.pkl", "rb"))


def get_isbn(name):
    final_rating = pd.read_csv("final_data.csv")
    isbn = final_rating.loc[
        final_rating['title'] == name].iloc[
        0].ISBN
    return isbn


def fetch_cover(isbn):
    url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"
    return url


def get_recommendations(name, no_of_recommendations=5):
    num = np.where(book_pivot.index == name)[0]
    if len(num) == 0:
        print("No such book in list")
        return
    else:
        num = num[0]
    distances, suggestions = model.kneighbors(book_pivot.iloc[num, :].values.reshape(1, -1), n_neighbors=no_of_recommendations + 1)
    return list(book_pivot.iloc[suggestions[0][1:]].index)


def fetch_books_data(name):
    book_list = get_recommendations(name, 5)
    cover_list = []
    for book in book_list:
        isbn = get_isbn(book)
        url = fetch_cover(isbn)
        cover_list.append(url)
    return cover_list


st.title("Book Recommender System")

option = st.selectbox(
    'Please Select a Book',
    movies_list_)


if st.button("Recommend"):
    names, posters = get_recommendations(option, 5), fetch_books_data(option)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(f'{names[0]}')
        st.image(f"{posters[0]}")

    with col2:
        st.text(f'{names[1]}')
        st.image(f"{posters[1]}")

    with col3:
        st.text(f'{names[2]}')
        st.image(f"{posters[2]}")

    with col4:
        st.text(f'{names[3]}')
        st.image(f"{posters[3]}")

    with col5:
        st.text(f'{names[4]}')
        st.image(f"{posters[4]}")


footer = """<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: black;
color: white;
text-align: center;
}

#love {
color: red;
}
</style>
<div class="footer">
<p>Developed with <span id="love">❤</span> by <a style='display: block; text-align: center;' href="https://github.com/astrovishalthakur" target="_blank">Vishal Thakur</a></p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)


