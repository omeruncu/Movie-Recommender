import pandas as pd
from .data_loader import load_and_prepare_data


def select_user_data(df, user_id):
    """
    Seçili kullanıcıya ait gözlemleri ve izlediği filmleri belirler.

    Args:
      df: Filtrelenmiş dataframe.
      user_id: İncelenecek kullanıcı ID.

    Returns:
      random_user_df: Seçilen kullanıcıya ait dataframe.
      movies_watched: Kullanıcının oy verdiği filmlerin listesi.
    """
    random_user_df = df[df['userId'] == user_id]
    movies_watched = random_user_df['title'].tolist()

    #print("\n----- UBR - select_user_data : random_user_df  -----")
    #print(random_user_df)
    #print("\n----- UBR - select_user_data : movies_watched  -----")
    #print(movies_watched)

    return random_user_df, movies_watched


def get_users_same_movies(user_movie_df, movies_watched, threshold=0.4):
    """
    Seçilen kullanıcının izlediği filmleri temel alarak diğer kullanıcıları tespit eder.

    Args:
      user_movie_df: Pivot tablo.
      movies_watched: Seçilen kullanıcının izlediği filmlerin listesi.
      threshold: İzlenmesi gereken filmlerin oranı (default %60).

    Returns:
      movies_watched_df: Seçilen filmlere ait alt küme.
      user_movie_count: Her kullanıcının izlediği film sayısı.
      users_same_movies: Eşik değeri karşılayan kullanıcı ID listesi.
    """
    movies_watched_df = user_movie_df[movies_watched]
    user_movie_count = movies_watched_df.notnull().sum(axis=1)
    num_movies = len(movies_watched)
    users_same_movies = user_movie_count[user_movie_count >= threshold * num_movies].index.tolist()

    #print("\n----- UBR - get_users_same_movies : movies_watched_df  -----")
    #print(movies_watched_df)
    #print("\n----- UBR - get_users_same_movies : user_movie_count  -----")
    #print(user_movie_count)
    #print("\n----- UBR - get_users_same_movies : users_same_movies  -----")
    #print(users_same_movies)

    return movies_watched_df, user_movie_count, users_same_movies


def get_top_similar_users(user_movie_df, selected_user_id, users_same_movies, corr_threshold=0.65):
    """
    Seçili kullanıcı ile en benzer kullanıcıları korelasyon hesaplayarak belirler.

    Returns:
      top_users: Yüksek korelasyona sahip kullanıcıların dataframe'i.
    """
    filtered_users_df = user_movie_df.loc[users_same_movies]
    corr_series = filtered_users_df.T.corrwith(user_movie_df.loc[selected_user_id])
    corr_df = pd.DataFrame(corr_series, columns=['corr']).dropna().reset_index().rename(columns={'index': 'userId'})
    # Seçili kullanıcıyı hariç tut ve eşik değerinin üzerindekileri filtrele.
    top_users = corr_df[(corr_df['userId'] != selected_user_id) & (corr_df['corr'] > corr_threshold)]

    #print("\n----- UBR - get_top_similar_users : top_users  -----")
    #print(top_users)

    return top_users


def merge_top_users_with_ratings(top_users, df):
    """
    Top kullanıcıların rating bilgilerinin yer aldığı dataframe ile merge yapılır.
    """
    top_users_ratings = pd.merge(top_users, df[['userId', 'movieId', 'rating']], on='userId', how='inner')

    #print("\n----- UBR - merge_top_users_with_ratings : top_users_ratings  -----")
    #print(top_users_ratings)

    return top_users_ratings


def calculate_weighted_recommendation(top_users_ratings, movies_df, rating_threshold=3.5, top_n=5):
    """
    Her kullanıcının corr ve rating değerlerini çarpıp film bazında ağırlıklı ortalama hesaplar.
    """
    top_users_ratings['weighted_rating'] = top_users_ratings['corr'] * top_users_ratings['rating']
    recommendation_df = top_users_ratings.groupby('movieId').agg({'weighted_rating': 'mean'}).reset_index()
    recommendation_df = recommendation_df[recommendation_df['weighted_rating'] > rating_threshold].sort_values(
        'weighted_rating', ascending=False)
    recommendation_df = pd.merge(recommendation_df, movies_df[['movieId', 'title']], on='movieId', how='left')

    #print("\n----- UBR - calculate_weighted_recommendation : weighted_recommendation  -----")
    #print(recommendation_df[['title', 'weighted_rating']].drop_duplicates().head(top_n))

    return recommendation_df[['title', 'weighted_rating']].drop_duplicates().head(top_n)


def user_based_recommender(
    user_id, df_filtered: pd.DataFrame, user_movie_df: pd.DataFrame, top_n=5
):
    """
    Tüm kullanıcı-temelli öneri sürecini çalıştırır:
      - Veri yükleme
      - Kullanıcı izleme geçmişi
      - Benzer kullanıcıların tespiti ve ağırlıklı puan hesaplama
      - İlk 5 filmin önerilmesi
    """
    # Ortak veri hazırlama modülünü kullan
    # movies_df için ayrı okuma (aynı dosyayı tekrar kullanmak için DRY kuralına uyarız çünkü data_loader modülünden de dönebilir.)
    movies_df = pd.read_csv('data/movie.csv')

    # Seçili kullanıcının verilerini al
    random_user_df, movies_watched = select_user_data(df_filtered, user_id)
    movies_watched_df, user_movie_count, users_same_movies = get_users_same_movies(user_movie_df, movies_watched)
    top_users = get_top_similar_users(user_movie_df, user_id, users_same_movies)
    top_users_ratings = merge_top_users_with_ratings(top_users, df_filtered)
    recommendation = calculate_weighted_recommendation(top_users_ratings, movies_df)

    #print("\n----- UBR - user_based_recommender : recommendation  -----")
    #print(recommendation)

    return recommendation