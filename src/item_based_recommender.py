import pandas as pd
from data_loader import load_and_prepare_data


def item_based_recommender(user_id, top_n=5):
    """
    Kullanıcının 5 puan verdiği filmlerden en güncel olanı üzerinden
    diğer filmlerle korelasyon hesaplayarak öneri üretir.

    Adımlar:
    - Ortak veri setini load_and_prepare_data ile elde etmek.
    - Seçili kullanıcının 5 puan verdiği filmleri zaman sırasına göre sıralamak.
    - En güncel filmin pivot tablodaki sütununu kullanarak diğer filmlerle korelasyonu hesaplamak.
    - Seçili film hariç en yüksek korelasyona sahip ilk 5 filmi döndürmek.
    """
    df_filtered, user_movie_df = load_and_prepare_data()

    # Seçili kullanıcının verilerini al
    user_data = df_filtered[df_filtered['userId'] == user_id]
    five_star_movies = user_data[user_data['rating'] == 5]

    if five_star_movies.empty:
        print("Kullanıcının 5 puan verdiği film bulunamadı.")
        return None

    five_star_movies = five_star_movies.sort_values('timestamp', ascending=False)
    selected_movie_title = five_star_movies.iloc[0]['title']

    if selected_movie_title not in user_movie_df.columns:
        print("Seçilen film pivot tablosunda yer almıyor.")
        return None

    correlations = user_movie_df.corrwith(user_movie_df[selected_movie_title])
    corr_df = pd.DataFrame(correlations, columns=['correlation']).dropna().reset_index().rename(
        columns={'index': 'title'})

    # Seçilen filmi hariç tut ve korelasyona göre sıralama yap
    corr_df = corr_df[corr_df['title'] != selected_movie_title]
    recommendations = corr_df.sort_values('correlation', ascending=False).head(top_n)

    #print("\n----- IBR - item_based_recommender : recommendations  -----")
    #print(recommendations)

    return recommendations