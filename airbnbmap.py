import folium
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import folium
from folium.plugins import MarkerCluster
import pandas as pd
from sklearn.preprocessing import StandardScaler

def recommend_airbnb(user_neighbourhood_group,user_price_range_min,user_price_range_max, user_room_type, user_cancellation_policy, num_neighbors=2,num_recommendations = 100,limit = 3):

    # Kullanıcı kriterlerine göre filtreleme
    filtered_listings = df[
        (df['neighbourhood_group'].isin(user_neighbourhood_group)) &
        (df['price'] >= user_price_range_min) &
        (df['price'] <= user_price_range_max) &
        (df['room type'] == user_room_type) &
        (df['cancellation_policy'].isin(user_cancellation_policy))
    ]
    
    if filtered_listings.empty:
        print("Kriterlere uygun sonuç bulunamadı.")
        return None

    # Kullanılacak özellikleri seçelim
    features = df[['price', "service fee", 'number of reviews', 'review rate number', 'lat', 'long']]
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    # K-Nearest Neighbors modelini oluşturalım
    knn = NearestNeighbors(n_neighbors=num_neighbors, algorithm='auto')
    knn.fit(features_scaled)

    # Filtrelenmiş evlerin özelliklerini alalım
    filtered_features = filtered_listings[['price', "service fee", 'number of reviews', 'review rate number', 'lat', 'long']]
    filtered_features_scaled = scaler.transform(filtered_features)

    # Benzer evleri bulalım
    distances, indices = knn.kneighbors(filtered_features_scaled)

    # Benzer ev ilanlarının bilgilerini alalım
    recommended_listings = df.iloc[indices.flatten()]

    # Yalnızca review rate number 3 ve üzeri olanları filtreleyelim
    recommended_listings = recommended_listings[recommended_listings['review rate number'] >= limit]
    
    if recommended_listings.empty:
        print(f"Review rate number {limit} ve üzeri uygun sonuç bulunamadı.")
        return None
    
    # Review rate number'a göre büyükten küçüğe sıralayalım
    recommended_listings = recommended_listings.sort_values(by='review rate number', ascending=False)
    
    # İlk num_recommendations tanesini seçelim
    top_recommendations = recommended_listings.head(num_recommendations)
        
    # Ortalama konumu bulalım
    avg_lat = top_recommendations['lat'].mean()
    avg_long = top_recommendations['long'].mean()

    # Haritayı oluştur
    map_ = folium.Map(location=[avg_lat, avg_long], zoom_start=12)
    marker_cluster = MarkerCluster().add_to(map_)
    
    for idx, row in top_recommendations.iterrows():
        folium.Marker(
            location=[row['lat'], row['long']],
            popup=f"<strong>{row['NAME']}</strong><br>Price: ${row['price']}<br>Service Fee: ${row['service fee']}<br>Review Rate: {row['review rate number']}<br>Number of Reviews: {row['number of reviews']}",
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(marker_cluster)
    
    # Haritayı Jupyter Notebook içinde görüntüle
    return map_, top_recommendations



