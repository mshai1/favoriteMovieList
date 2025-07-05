# 🎬 Top 10 Movies List (Flask + SQLite Project)

This is a simple web app built with **Flask** and **SQLite** where you can create and manage a personal **Top 10 Movies** list. Movie data is fetched via the [TMDB (The Movie Database)](https://www.themoviedb.org/signup) API. After searching for a movie by title, you can rate and review it, and it will appear in your top 10 list, sorted by your rating.

---

## 🚀 Features

- 🔍 Search for movies by title using TMDB API
- 📆 View release dates of matching titles
- 📝 Add your own rating (out of 10.0) and review
- 📊 Automatically sorts and displays your movies by rating
- 🛠️ Built with Flask, SQLite, and Jinja2 templates

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```
git clone https://github.com/mshai1/favoriteMovieList.git
cd favoriteMovieList
```
### 2. Install Required Packages

 ``` pip install -r requirements.txt```


### 3. Get Your TMDB API Access Token
To use the search functionality, you need an API token from TMDB.

  - Sign up at TMDB
  - Go to your account → Settings → API → Create an API token

### 4. Run the App

By default, the app will be available at:
```http://localhost:5000```
