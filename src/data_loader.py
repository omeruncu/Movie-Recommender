import pandas as pd


def load_and_prepare_data(movie_path=None,
                          rating_path=None,
                          min_votes=1000):
    """
    movie_path, rating_path ya:
      • None ise proje içindeki data/movie.csv, data/rating.csv kullanılacak
      • file‐like obj (Streamlit) veya string path verilebilir
    """
    # default dosya yolları
    default_movies = "data/movie.csv"
    default_ratings = "data/rating.csv"

    # hem file‐like hem de path desteği için:
    movies_src = movie_path if movie_path is not None else default_movies
    ratings_src = rating_path if rating_path is not None else default_ratings

    # pandas, UploadedFile objesini de okuyabiliyor
    movies = pd.read_csv(movies_src)
    ratings = pd.read_csv(ratings_src)

    # merge + filtre + pivot
    df = pd.merge(ratings, movies, on="movieId", how="inner")
    # min_votes altı filmleri çıkar
    to_keep = df["title"].value_counts()[lambda x: x >= min_votes].index
    df_filtered = df[df["title"].isin(to_keep)].copy()
    user_movie_df = df_filtered.pivot_table(
        index="userId", columns="title", values="rating"
    )

    return df_filtered, user_movie_df



def get_random_user_id(user_movie_df):
    """
    Pivot tablosundaki (user_movie_df) kullanıcı ID'leri arasından rastgele bir tane seçer.

    Args:
        user_movie_df (DataFrame): index'lerinde kullanıcı ID'lerinin bulunduğu pivot tablo.

    Returns:
        int: Rastgele seçilen kullanıcı ID'si.
    """
    random_user_id = int(pd.Series(user_movie_df.index).sample(1).values[0])
    #print("\n----- LOAD : random_user_id  -----")
    #print(random_user_id)

    return random_user_id
