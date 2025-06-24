import pandas as pd
from .user_based_recommender import user_based_recommender
from .item_based_recommender import item_based_recommender


def hybrid_recommender(
    selected_user, df_filtered, user_movie_df, movies_df, total_recs=10, user_based_n=5, item_based_n=5
):

    """
    İki yöntemin önerilerini birleştirerek toplam (örneğin 10) benzersiz film önerisi sunar.
    """
    user_based_rec = user_based_recommender(selected_user, df_filtered, user_movie_df, movies_df)
    item_based_rec = item_based_recommender(selected_user, df_filtered, user_movie_df)

    hybrid = pd.concat([user_based_rec[['title']], item_based_rec[['title']]], ignore_index=True)
    hybrid_unique = hybrid.drop_duplicates().reset_index(drop=True)

    # İstenen sayıda öneri sağlanmazsa, user-based önerilerden tamamlarız.
    if hybrid_unique.shape[0] < total_recs:
        additional = user_based_rec[~user_based_rec['title'].isin(hybrid_unique['title'])].head(
            total_recs - hybrid_unique.shape[0])
        hybrid_unique = pd.concat([hybrid_unique, additional[['title']]], ignore_index=True)

    #print("\n----- HR - hybrid_recommender : hybrid_unique.head(total_recs)  -----")
    #print(hybrid_unique.head(total_recs))

    return hybrid_unique.head(total_recs)