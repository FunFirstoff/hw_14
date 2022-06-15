import sqlite3


def search_by_title(title, page=0):
    limit = 10
    offset = limit * int(page)
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        select_query = f"SELECT * FROM netflix " \
                       f"WHERE title LIKE '%{title}%' " \
                       f"ORDER BY release_year DESC, date_added DESC " \
                       f"LIMIT {limit} OFFSET {offset}"
        cursor.execute(select_query)
        result = cursor.fetchall()
        movies = []
        field_names = [i[0] for i in cursor.description]
        i = 0
        for items in result:
            movies.append({})
            for item, field in zip(items, field_names):
                movies[i][field] = item
            i += 1
        return movies


def search_by_show_id(show_id):
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        select_query = f"SELECT title, country, release_year, listed_in, description " \
                       f"FROM netflix " \
                       f"WHERE show_id = '{show_id}'"
        cursor.execute(select_query)
        field_names = [i[0] for i in cursor.description]
        result = cursor.fetchone()
        movie = {}
        for item, field in zip(result, field_names):
            movie[field] = item

        return movie


def get_release_years():
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        select_query = f"SELECT DISTINCT release_year " \
                       f"FROM netflix " \
                       f"ORDER BY release_year"
        cursor.execute(select_query)
        result = cursor.fetchall()
        years = []
        for item in result:
            years.append(item[0])

        return years


def search_between_years(y1, y2):
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        select_query = f"SELECT title, release_year " \
                       f"FROM netflix " \
                       f"WHERE release_year BETWEEN {y1} AND {y2} " \
                       f"LIMIT 100"
        cursor.execute(select_query)
        result = cursor.fetchall()
        movies = []
        for item in result:
            movie = {"title": item[0],
                     "release_year": item[1]}
            movies.append(movie)

        return movies


def search_by_rating(rating):
    ratings = {
        "children": "'G'",
        "family": "'G', 'PG', 'PG-13'",
        "adult": "'R', 'NC-17'"
    }

    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()

        select_query = f"SELECT title, rating, description " \
                       f"FROM netflix " \
                       f"WHERE rating in ({ratings[rating]})"
        cursor.execute(select_query)
        result = cursor.fetchall()
        movies = []
        for item in result:
            movie = {"title": item[0],
                     "rating": item[1],
                     "description": item[2]}
            movies.append(movie)

        return movies


def get_genres():
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        select_query = f"SELECT DISTINCT listed_in " \
                       f"FROM netflix "
        cursor.execute(select_query)
        result = cursor.fetchall()
        result = list(result)
        all_genres = []
        for item in result:
            item = str(list(item)[0])
            genres = item.split(", ")
            if len(genres) > 1:
                for genre in genres:
                    all_genres.append(genre)
            else:
                all_genres.append(item)

        all_genres = set(all_genres)
        return all_genres


def search_by_genre(genre):
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        select_query = f"SELECT title, description " \
                       f"FROM netflix " \
                       f"WHERE listed_in LIKE '%{genre}%' " \
                       f"ORDER BY release_year DESC, date_added DESC " \
                       f"LIMIT 10"
        cursor.execute(select_query)
        result = cursor.fetchall()
        movies = []
        for item in result:
            movie = {"title": item[0],
                     "description": item[1]}
            movies.append(movie)

        return movies


def get_cast(s_actors=["Jack Black", "Dustin Hoffman"]):
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        select_query = f"SELECT `cast` " \
                       f"FROM netflix " \
                       f"WHERE `cast` LIKE '%{s_actors[0]}%' " \
                       f"AND `cast` LIKE '%{s_actors[1]}%' "
        cursor.execute(select_query)
        result = cursor.fetchall()
        actors_total = {}
        actors_result = []
        for items in result:
            for item in items:
                actors = item.split(", ")
                for actor in actors:
                    if actor in actors_total:
                        actors_total[actor] += 1
                    else:
                        actors_total[actor] = 1
        for key, value in actors_total.items():
            if value > 2 and key not in s_actors:
                actors_result.append(key)

        return actors_result


def get_types():
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        select_query = f"SELECT DISTINCT `type` " \
                       f"FROM netflix "
        cursor.execute(select_query)
        result = cursor.fetchall()
        types = []
        for item in result:
            types.append(item[0])

        return types


def search_by_type_year_genre(show_type, release_year, genre):
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        select_query = f"SELECT title, description " \
                       f"FROM netflix " \
                       f"WHERE `type` = '{show_type}' " \
                       f"AND release_year = '{release_year}' " \
                       f"AND listed_in LIKE '%{genre}%' "
        cursor.execute(select_query)
        result = cursor.fetchall()
        movies = []

        for item in result:
            movie = {
                "title": item[0],
                "description": item[1]
            }
            movies.append(movie)

        return movies
