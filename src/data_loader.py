import pandas as pd


def load_and_prepare_data(
    movie_path=None,
    rating_path=None,
    movies_df=None,
    ratings_df=None,
    min_votes=1000
):
    """
    Ya doğrudan DataFrame (movies_df, ratings_df),
    ya path (movie_path, rating_path) ver.
    """
    # Movies DataFrame'i belirle
    if movies_df is None:
        source = movie_path or "data/movie.csv"
        movies_df = pd.read_csv(source)

    # Ratings DataFrame'i belirle
    if ratings_df is None:
        source = rating_path or "data/rating.csv"
        ratings_df = pd.read_csv(source)

    # Merge + filtre + pivot
    df = pd.merge(ratings_df, movies_df, on="movieId", how="inner")
    to_keep = df["title"].value_counts()[lambda x: x >= min_votes].index
    df_filtered = df[df["title"].isin(to_keep)].copy()
    user_movie_df = df_filtered.pivot_table(
        index="userId", columns="title", values="rating"
    ).fillna(0)

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
