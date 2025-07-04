from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import os

'''
Install the required packages first:
Open the Terminal in Pycharm(Bottom Left)

On Windows type:
python -m pip install -r requirements.txt

Om MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project
'''

TMDB_API_KEY = os.getenv('TMDB_API_KEY')
print(TMDB_API_KEY)
TMDB_ACCESS_API_KEY = os.getenv('TMDB_ACCESS_API_KEY')
TMDB_URL = "https://api.themoviedb.org/3/search/movie?include_adult=false&language=en-US&page=1"
MOVIE_DB_INFO_URL = "https://api.themoviedb.org/3/movie"
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer " + TMDB_API_KEY
}

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBAB6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///favorite-movies-list.db"

db = SQLAlchemy(model_class=Base)
db.init_app(app)


#CREATE THE MOVIE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

    def __repr__(self):
        return f'<Movie {self.title}>'


#Create table schema in the database. Requires application context.
# with app.app_context():
#     db.create_all()

#
# new_movie = Movie(
#     title="Avatar The Way of Water",
#     year=2022,
#     description="Set more than a decade after the event of the first film, learn the story of Sully family(Jake, Netiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedy thet endure.",
#     rating=7.3,
#     ranking=9,
#     review="I liked the water.",
#     img_url="https://media.themoviedb.org/t/p/w600_and_h900_bestv2/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
# )
#
#
# with app.app_context():
#     existing = db.session.execute(db.select(Movie).where(Movie.title == "Avatar The Way of Water")).scalar()
#     if not existing:
#         db.session.add(new_movie)
#         db.session.commit()
#     else:
#         print("Movie already exists in the DB.")


class AddMovieForm(FlaskForm):
    title = StringField("Movie Title")
    submit = SubmitField("Add Movie")


class RateMovieForm(FlaskForm):
    rating = StringField("Your Rating Out of 10 e.g. 7.5")
    review = StringField("Your Review")
    submit = SubmitField("Done")


@app.route('/')
def main():
    result = db.session.execute(db.select(Movie).order_by(Movie.rating))
    all_movies = result.scalars().all()

    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()

    return render_template('index.html', movies=all_movies)


@app.route('/add', methods=['GET', 'POST'])
def add_movie():
    form = AddMovieForm()
    if form.validate_on_submit():
        movie_title = form.title.data
        body = {
            "query": movie_title
        }
        #Need to make an API call to fetch movie details
        result = requests.get(url=TMDB_URL, headers=headers, params=body)
        all_movies = result.json()['results']
        print(all_movies)
        return render_template('select.html', movies=all_movies)
    return render_template('add.html', form=form)


@app.route('/find')
def find_movie():
    movie_api_id = request.args.get("id")
    if movie_api_id:
        movie_api_url = f"{MOVIE_DB_INFO_URL}/{movie_api_id}"
        response = requests.get(url=movie_api_url, headers=headers)
        data = response.json()
        new_movie = Movie(
            title = data["title"],
            year = data["release_date"].split("-")[0],
            img_url = f"{MOVIE_DB_IMAGE_URL}/{data["poster_path"]}",
            description = data['overview']
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('edit_movie', movie_id=new_movie.id))


@app.route('/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit_movie(movie_id):
    form = RateMovieForm()
    movie = db.get_or_404(Movie, movie_id)

    if request.method == 'POST':
        movie.rating = request.form.get('rating')
        movie.review = request.form.get('review')
        db.session.commit()
        return redirect(url_for('main'))

    return render_template('edit.html', form=form, movie=movie)


@app.route('/delete/<int:movie_id>')
def delete_movie(movie_id):
    movie = db.get_or_404(Movie, movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('main'))


if __name__=='__main__':
    app.run(debug=True)