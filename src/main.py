from user_based_recommender import user_based_recommender
from item_based_recommender import item_based_recommender
from hybrid_recommender import hybrid_recommender
from data_loader import get_random_user_id, load_and_prepare_data



def main():
    # Ortak veri yükleyiciden pivot tablosunu elde ediyoruz
    _, user_movie_df = load_and_prepare_data()
    # Örnek kullanıcı ID'si (veri setinize göre değiştirin)
    random_user_id = get_random_user_id(user_movie_df)

    print("----- User Based Recommendation (İlk 5 Film) -----")
    user_rec = user_based_recommender(random_user_id)
    print(user_rec)

    print("\n----- Item Based Recommendation (İlk 5 Film) -----")
    item_rec = item_based_recommender(random_user_id)
    print(item_rec)

    print("\n----- Hybrid Öneriler (Toplam 10 Film) -----")
    hybrid_rec = hybrid_recommender(random_user_id)
    print(hybrid_rec)


if __name__ == "__main__":
    main()