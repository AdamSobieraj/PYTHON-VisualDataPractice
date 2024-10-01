import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Załadowanie danych
movies_df = pd.read_csv('tmdb_movies.csv')
genres_df = pd.read_csv('tmdb_genres.csv')

# Sprawdzenie nazwy kolumny 'id' w genres_df
print("Nazwy kolumn w genres_df:")
genres_df = genres_df.rename(columns={genres_df.columns[0]: 'genre_id'})
print(genres_df.columns)

# Zmiana nazwy kolumny 'id' na 'genre_id' w movies_df
movies_df['genre_id'] = movies_df['genre_id']

# Konwersja kolumny release_date na typ datetime
movies_df['release_date'] = pd.to_datetime(movies_df['release_date'])

# Utworzenie kolumn avg_budget i avg_revenue
movies_df['avg_budget'] = movies_df['budget']
movies_df['avg_revenue'] = movies_df['revenue']

# 1. Lista 10 najwyżej ocenianych filmów
third_quartile = np.percentile(movies_df['vote_count'], 75)
top_films = movies_df[movies_df['vote_count'] > third_quartile].sort_values('vote_average', ascending=False).head(10)
print("Lista 10 najwyżej ocenianych filmów:")
print(top_films[['title', 'vote_average']])

# 2. Grupowanie tabeli i tworzenie wykresu
grouped_data = movies_df.groupby(movies_df['release_date'].dt.year)[['avg_revenue', 'avg_budget']].agg({'avg_revenue': 'mean', 'avg_budget': 'mean'}).reset_index()

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

ax1.plot(grouped_data['release_date'], grouped_data['avg_budget'])
ax1.set_title('Średni budżet filmów według roku')
ax1.set_xlabel('Rok')
ax1.set_ylabel('Średni budżet')

ax2.bar(grouped_data['release_date'], grouped_data['avg_revenue'])
ax2.set_title('Średni przychód filmów według roku')
ax2.set_xlabel('Rok')
ax2.set_ylabel('Średni przychód')

plt.tight_layout()
plt.show()

# 3. Łączenie baz danych i znajdowanie najczęściej występującego gatunku
merged_df = movies_df.merge(genres_df, left_on='genre_id', right_on='genre_id', how='left')
merged_df['genres'] = merged_df['genres'].fillna('N/A')

# Obliczenie częstotliwości występowania gatunków
genre_counts = merged_df['genres'].value_counts().reset_index()
genre_counts.columns = ['Gatunek', 'Częstotliwość']

# 4. ile filmów tego gatunku znajduje się w bazie
print("\nNajczęściej występujący gatunek:")
print(genre_counts.nlargest(1, columns=['Częstotliwość']))

# 5. Znalezienie filmów z najdłuższym czasem trwania dla każdego gatunku
max_runtime_films = merged_df[merged_df['genres'] != 'N/A'].groupby('genres')['runtime'].agg(['max']).reset_index()

print("\nFilmy z najdłuższym czasem trwania dla każdego gatunku:")
print(max_runtime_films)

# Tworzenie histogramu czasu trwania dla gatunku z najdłuższym średnim czasem trwania
avg_runtime = merged_df.groupby('genres')['runtime'].mean().reset_index()
max_avg_runtime = avg_runtime.loc[avg_runtime['runtime'].idxmax()]

plt.figure(figsize=(12, 6))
plt.hist(merged_df[merged_df['genres'] == max_avg_runtime['genres']]['runtime'], bins=20, edgecolor='black')
plt.axvline(x=max_avg_runtime['runtime'], color='red', linestyle='--', label=f'Sredni czas trwania: {max_avg_runtime["runtime"]} minuty')
plt.title(f'Histogram czasu trwania filmów - Gatunek: {max_avg_runtime["genres"]}')
plt.xlabel('Czas trwania (minuty)')
plt.ylabel('Liczba filmów')
plt.legend()
plt.tight_layout()
plt.show()
