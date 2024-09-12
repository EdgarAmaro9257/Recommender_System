from flask import Flask, request, jsonify
from models.collaborative_filtering import CollaborativeFilteringRecommender
import pandas as pd
import numpy as np

app = Flask(__name__)

# Generar un conjunto de datos de interacción más grande
np.random.seed(42)
n_users = 100  # Número de usuarios
n_items = 50   # Número de ítems

interaction_data = pd.DataFrame({
    'user_id': np.random.randint(1, n_users + 1, size=1000),
    'item_id': np.random.randint(101, 101 + n_items, size=1000),
    'rating': np.random.randint(1, 6, size=1000)  # Ratings entre 1 y 5
})

# Crear la matriz de interacciones usando pivot_table
interaction_matrix = interaction_data.pivot_table(index='user_id', columns='item_id', values='rating', aggfunc='mean').fillna(0)

# Crear recomendador
recommender = CollaborativeFilteringRecommender(interaction_matrix)
recommender.fit()

@app.route('/recommend/<int:user_id>', methods=['GET'])
def recommend(user_id):
    # Verificar si el usuario existe en los datos
    if user_id not in interaction_matrix.index:
        return jsonify({'error': 'El usuario no existe en el sistema.'}), 404

    try:
        recommendations = recommender.recommend(user_id)
        if recommendations is None or len(recommendations) == 0:
            return jsonify({'error': 'No se encontraron recomendaciones para este usuario.'}), 400
        return jsonify({'recommendations': recommendations.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
