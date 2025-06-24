"""
Movie-Recommender paketinin ana giriş noktası.
Altındaki recommender modüllerini doğrudan import etmeye izin verir.
"""

from .user_based_recommender import user_based_recommender
from .item_based_recommender import item_based_recommender
from .hybrid_recommender import hybrid_recommender
from .data_loader import get_random_user_id, load_and_prepare_data

__all__ = [
    "user_based_recommender",
    "item_based_recommender",
    "hybrid_recommender",
    "data_loader"
]
