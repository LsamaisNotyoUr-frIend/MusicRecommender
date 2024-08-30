import os
import random
import tkinter as tk
from tkinter import messagebox
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
        song_list = self.fetch_songs_from_spotify(genre.name, 20)
        return song_list

    def populate_genres_with_random_songs(self):
        for genre in self.genres:
            random_genre = self.get_random_genre(random.randint(1, 5))
            song_list = self.fetch_songs_from_spotify(random_genre, 10)
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
        return random.sample(list_of_songs, 5)

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


class MusicApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.recommend_button = None
        self.label = None
        self.back_button = None
        self.text_box = None
        self.result_label = None
        self.title("Music Recommendation System")
        self.geometry("500x400")
        self.recommender = MusicRecommendationSystem()
        self.create_widgets()

    def create_widgets(self):
        # Label for mood input
        self.label = tk.Label(self, text="Enter your mood or preference:")
        self.label.pack(pady=10)

        # Textbox for user input
        self.text_box = tk.Text(self, height=5, width=50)
        self.text_box.pack(pady=10)

        # Recommend Button
        self.recommend_button = tk.Button(self, text="Recommend", command=self.recommend_songs)
        self.recommend_button.pack(pady=10)

        # Back Button
        self.back_button = tk.Button(self, text="Back", command=self.reset_ui)
        self.back_button.pack(pady=10)

        # Label for displaying recommendations
        self.result_label = tk.Label(self, text="", justify="left")
        self.result_label.pack(pady=10)

    def recommend_songs(self):
        user_mood = self.text_box.get("1.0", "end-1c").strip()
        if not user_mood:
            messagebox.showwarning("Input Error", "Please enter your mood or preference.")
            return

        songs_recommended = self.recommender.recommend_songs(user_mood)
        recommendations = "\n".join(songs_recommended)
        self.result_label.config(text=f"Recommended Songs:\n{recommendations}")

    def reset_ui(self):
        self.text_box.delete("1.0", "end")
        self.result_label.config(text="")


if __name__ == "__main__":
    app = MusicApp()
    app.mainloop()
