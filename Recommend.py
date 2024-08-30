import os
import random

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv('Credentials.env')

spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=spotify_client_id,
    client_secret=spotify_client_secret)
)


class Genre:
    def __init__(self, name, keywords):
        self.name = name
        self.keywords = keywords
        self.songs = []
        self.random_songs = []

    def add_songs(self, song_list):
        self.songs.extend(song_list)

    def add_random_songs(self, song_list):
        self.random_songs.extend(song_list)

    def matches(self, text):
        return any(keyword in text.lower() for keyword in self.keywords)


class MusicRecommendationSystem:
    def __init__(self):
        self.genres = [
            Genre("Pop", ["happy", "dance", "upbeat"]),
            Genre("Rock", ["wild", "cool", "free"]),
            Genre("Soul", ["enlightened", "stoic", "confused"]),
            Genre("Blues", ["sad", "blue", "melancholy"]),
            Genre("Classical", ["calm", "relax", "neutral"]),
            Genre("Random", ["", "i don't know"])
        ]

    def populate_genres_with_songs(self, genre: Genre):
        song_list = self.fetch_songs_from_spotify(genre.name, 10)
        return song_list

    def populate_genres_with_random_songs(self):
        for genre in self.genres:
            random_genre = self.get_random_genre(random.randint(1, 5))
            song_list = self.fetch_songs_from_spotify(random_genre, 5)
            genre.add_random_songs(song_list)

    @staticmethod
    def fetch_songs_from_spotify(genre_name, limit: int):
        results = sp.search(q=f'genre:{genre_name}', type='track', limit=limit)
        songs_from_network = [f"{item['name']} by {item['artists'][0]['name']}" for item in results['tracks']['items']]
        return songs_from_network

    def recommend_songs(self, input_text):
        for genre in self.genres:
            if genre.matches(input_text):
                return self.return_ramdom_song_list(self.populate_genres_with_songs(genre))
            else:
                self.populate_genres_with_random_songs()
                return self.return_ramdom_song_list(genre.random_songs)

    @staticmethod
    def return_ramdom_song_list(list_of_songs: list):
        return random.sample(list_of_songs, 4)

    @staticmethod
    def get_random_genre(number: int):
        if number == 1:
            genre = "Pop"
        elif number == 2:
            genre = "Rock"
        elif number == 3:
            genre = "Soul"
        elif number == 4:
            genre = "Blues"
        else:
            genre = "Classical"

        return genre


if __name__ == "__main__":
    spotify_client_id = "68fd62c50a074e2dbebb11c83f98dac5"
    spotify_client_secret = "ee5dd23b0b274446a713a6a20966cbab"

    recommender = MusicRecommendationSystem()

    user_input = input("Describe your mood or preference: ")
    songs = recommender.recommend_songs(user_input.strip())

    print("Recommended songs:")
    for song in songs:
        print(song)
