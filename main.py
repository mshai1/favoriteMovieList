from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

'''
Install the required packages first:
Open the Terminal in Pycharm(Bottom Left)

On Windows type:
python -m pip install -r requirements.txt

Om MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = ''
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


new_movie = Movie(
    title="Avatar The Way of Water",
    year=2022,
    description="Set more than a decade after the event of the first film, learn the story of Sully family(Jake, Netiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedy thet endure.",
    rating=7.3,
    ranking=9,
    review="I liked the water.",
    img_url="https://media.themoviedb.org/t/p/w600_and_h900_bestv2/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
)


with app.app_context():
    existing = db.session.execute(db.select(Movie).where(Movie.title == "Avatar The Way of Water")).scalar()
    if not existing:
        db.session.add(new_movie)
        db.session.commit()
    else:
        print("Movie already exists in the DB.")


@app.route('/')
def main():
    result = db.session.execute(db.select(Movie))
    all_movies = result.scalars().all()
    return render_template('index.html', movies=all_movies)

