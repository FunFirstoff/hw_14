from flask import Flask, render_template, request, jsonify, redirect
import utils

app = Flask(__name__)


@app.route("/")
def index_page():
    years = utils.get_release_years()
    genres = utils.get_genres()
    types = utils.get_types()
    return render_template("index.html", years=years, genres=genres, types=types)


@app.route("/search/")
def search_page():
    s = request.args.get("s")
    p = request.args.get("p")
    if not p:
        p = 0

    movies = utils.search_by_title(s, p)
    return render_template("search.html", movies=movies, s=s, p=p)


@app.route("/movie/<show_id>/")
def movie_page(show_id):
    movie = utils.search_by_show_id(show_id)
    return jsonify(movie)


@app.route("/search-by-years/")
def years_page():
    y1 = request.args.get("y1")
    y2 = request.args.get("y2")
    if y1 > y2:
        return redirect(f"/movie/{y2}/to/{y1}/")
    else:
        return redirect(f"/movie/{y1}/to/{y2}/")


@app.route("/movie/<y1>/to/<y2>/")
def search_between_years_page(y1, y2):
    movies = utils.search_between_years(y1, y2)
    return jsonify(movies)


@app.route("/rating/<rating>/")
def rating_adult_page(rating):
    movies = utils.search_by_rating(rating)
    return jsonify(movies)


@app.route("/search-actors/")
def actors_page():
    af = request.args.get("af")
    al = request.args.get("as")
    if af != "" and al != "":
        cast = [af, al]
        actors = utils.get_cast(cast)
    else:
        actors = utils.get_cast()
        print(af)
    return jsonify(actors)


@app.route("/genre/<genre>/")
def genre_page(genre):
    movies = utils.search_by_genre(genre)
    return jsonify(movies)


@app.route("/type-year-genre/")
def type_year_genre_page():
    t = request.args.get("t")
    y = request.args.get("y")
    g = request.args.get("g")
    movies = utils.search_by_type_year_genre(t, y, g)
    return jsonify(movies)


if __name__ == '__main__':
    app.run()
