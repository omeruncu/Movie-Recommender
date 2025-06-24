import streamlit as st
import pandas as pd
from src import (
    user_based_recommender,
    item_based_recommender,
    hybrid_recommender
)
from src.data_loader import load_and_prepare_data, get_random_user_id

st.set_page_config(page_title="Movie Recommender", layout="centered")
st.title("🎬 Movie Recommender Playground")

st.markdown("""
Yüklediğin `movie.csv` ve `rating.csv` ile istediğin öneri algoritmasını çalıştırabilirsin.
""")

movies_file = st.file_uploader("1) `movie.csv` yükle", type="csv")
ratings_file = st.file_uploader("2) `rating.csv` yükle", type="csv")
run_button = st.button("Önerileri Göster")

if run_button:
    if not movies_file or not ratings_file:
        st.error("Lütfen her iki CSV dosyasını da yükleyin.")
    else:
        # DataFrame'leri oku ve pivot tablosunu hazırla
        movies = pd.read_csv(movies_file)
        ratings = pd.read_csv(ratings_file)
        df_filtered, user_movie_df = load_and_prepare_data(movie_path=None, rating_path=None)
        # Eğer load fonksiyonun direkt path okumaya ayarlıysa:
        df_filtered = pd.merge(ratings, movies, on="movieId", how="left")
        user_movie_df = df_filtered.pivot_table(
            index="userId", columns="title", values="rating"
        )

        users = list(user_movie_df.index)
        selected_user = st.selectbox("3) Bir kullanıcı seç", users)

        algo = st.radio(
            "4) Algoritma seç",
            ["User-Based", "Item-Based", "Hybrid"]
        )

        # Önerileri hesapla ve göster
        if algo == "User-Based":
            recs = user_based_recommender(selected_user).head(5)
        elif algo == "Item-Based":
            recs = item_based_recommender(selected_user).head(5)
        else:
            recs = hybrid_recommender(selected_user)

        st.subheader(f"{algo} Önerileri")
        st.table(recs)
