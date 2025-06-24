import streamlit as st
import pandas as pd

from src.data_loader import load_and_prepare_data, get_random_user_id
from src.user_based_recommender import user_based_recommender
from src.item_based_recommender import item_based_recommender
from src.hybrid_recommender import hybrid_recommender


st.set_page_config(page_title="Movie Recommender", layout="centered")
st.title("🎬 Movie Recommender Playground")

st.markdown("""
Yüklediğin `movie.csv` ve `rating.csv` ile istediğin öneri algoritmasını çalıştırabilirsin.
""")

movies_file = st.file_uploader("1) `movie.csv` yükle", type="csv")
ratings_file = st.file_uploader("2) `rating.csv` yükle", type="csv")
run_button = st.button("Önerileri Göster")

if run_button:
    # Eğer ikisi de yoksa hata ver:
    if not movies_file and not ratings_file:
        st.info("Yüklemedin, o zaman default veriyle devam ediliyor.")
        df_filtered, user_movie_df = load_and_prepare_data()
    elif movies_file and ratings_file:
        st.success("Yüklenen CSV’lerle ilerleniyor.")
        df_filtered, user_movie_df = load_and_prepare_data(
            movie_path=movies_file,
            rating_path=ratings_file
        )
    else:
        st.error("Lütfen ya hiç dosya yükleme (default kullanım) ya da her iki dosyayı birlikte yükle.")
        st.stop()

    # Bir kullanıcı seç ve algoritmayı çalıştır
    users = user_movie_df.index.tolist()
    selected_user = st.selectbox("3) Kullanıcı seç", users)
    algo = st.radio("4) Algoritma seç", ["User-Based", "Item-Based", "Hybrid"])

    if algo == "User-Based":
        recs = user_based_recommender(selected_user, user_movie_df)
    elif algo == "Item-Based":
        recs = item_based_recommender(selected_user, user_movie_df)
    else:
        recs = hybrid_recommender(selected_user, user_movie_df)

    st.subheader(f"{algo} Önerileri")
    st.table(recs.head(10))
