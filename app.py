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

if st.button("Önerileri Göster"):
    if not movies_file or not ratings_file:
        st.error("Her iki dosyayı da yükleyin.")
        st.stop()

    # 1) Streamlit üzerinden DataFrame’e dönüştür
    movies_df = pd.read_csv(movies_file)
    ratings_df = pd.read_csv(ratings_file)

    # 2) Hazırla (data_loader içinden)
    df_filtered, user_movie_df = load_and_prepare_data(
        movies_df=movies_df,
        ratings_df=ratings_df,
        min_votes=1000
    )

    # 3) Rastgele kullanıcı seç
    selected_user = get_random_user_id(user_movie_df)
    st.markdown(f"**Seçilen Kullanıcı ID:** {selected_user}")

    # 4) Algoritmayı çağırırken DF’leri de geç
    algo = st.radio("Algoritma", ["User-Based", "Item-Based", "Hybrid"])
    if algo == "User-Based":
        recs = user_based_recommender(
            selected_user, df_filtered, user_movie_df, movies_df
        )
    elif algo == "Item-Based":
        recs = item_based_recommender(
            selected_user, df_filtered, user_movie_df
        )
    else:
        recs = hybrid_recommender(
            selected_user, df_filtered, user_movie_df, movies_df
        )

    # 5) Sonucu göster
    st.subheader(f"{algo} Önerileri")
    st.table(recs)
