import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

class CollaborativeFilteringRecommender:
    def __init__(self, interaction_matrix):
        self.interaction_matrix = interaction_matrix
        self.similarity_matrix = None
    
    def fit(self):
        # Calcular la similitud de usuarios
        self.similarity_matrix = cosine_similarity(self.interaction_matrix)
    
    def recommend(self, user_id, top_n=5):
        user_similarities = self.similarity_matrix[user_id]
        similar_users = user_similarities.argsort()[::-1][:top_n]
        return similar_users
