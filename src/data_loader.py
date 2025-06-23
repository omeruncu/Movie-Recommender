import pandas as pd


def load_and_prepare_data(movie_path='data/movie.csv', rating_path='data/rating.csv', min_votes=1000):
    """
    Verilen movie ve rating CSV dosyalarını okuyup aşağıdaki işlemleri yapar:

    - Dosyaları oku.
    - movieId üzerinden iki veri setini birleştir.
    - Toplam oy sayısı min_votes değerinin altında (default: 1000) olan filmleri belirle ve çıkar.
    - Kullanıcıların (userId) satır ve film isimlerinin sütun olduğu pivot tablo oluştur.

    Returns:
        df_filtered: Filtrelenmiş birleşik dataframe.
        user_movie_df: Pivot tablo (userId x film) – rating değerleri.
        movies_to_remove: Çıkarılan film isimlerinin listesi.
    """
    # Dosyaları oku
    movies = pd.read_csv(movie_path)
    ratings = pd.read_csv(rating_path)

    # movieId üzerinden birleştir
    df = pd.merge(ratings, movies, on='movieId', how='left')

    # 1000'in altında oy alan filmleri veri setinden çıkar
    df_filtered = df[~df['title'].isin(df['title'].value_counts()[lambda x: x < min_votes].index)].copy()

    # Pivot tablo: index = userId, sütunlar = film isimleri, değer = rating
    user_movie_df = df_filtered.pivot_table(index='userId', columns='title', values='rating')
    #print("\n----- LOAD : df_filtered  -----")
    #print(df_filtered)
    #print("\n----- LOAD : user_movie_df  -----")
    #print(user_movie_df)

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
