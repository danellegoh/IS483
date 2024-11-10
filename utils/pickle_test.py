from sklearn.cluster import KMeans
import pickle

# Sample data for KMeans training (replace with your actual training data)
data = [
    [4, 250],
    [3, 200],
    [5, 300],
    [2, 150],
    [1, 100]
]

# Train the KMeans model
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(data)

# Save the model to a new file
with open('health_tier_cluster_model_v2.pkl', 'wb') as model_file:
    pickle.dump(kmeans, model_file)
