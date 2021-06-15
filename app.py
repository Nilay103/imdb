from bson.objectid import ObjectId

from flask import Flask, request
from flask_caching import Cache
from flask_pymongo import pymongo
from flask_restplus import Api, Resource

from authentication import authenticate
from constants import DEBUG, MONGODB_URL, SECRET_KEY, DEFAULT_PAGE_LIMIT, DEBUG
from customs import custom_response, custom_paginated_response
from database import initialize_db, mongo
from registration import registration_bp

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config["MONGO_URI"] = MONGODB_URL

api = Api(app)
app.register_blueprint(registration_bp)
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})
name_space = api.namespace('api', description='Main APIs')
initialize_db(app)


@name_space.route('/movies/')
class MoviesApi(Resource):
    @cache.cached(timeout=500)
    def get(self):
        search_param = request.args.get('search')
        filter_param = {"$text": {"$search": search_param}} if search_param else None

        page_limit = int(request.args.get('limit', DEFAULT_PAGE_LIMIT))
        offset = int(request.args.get('offset', 0))

        movies = mongo.db.movies.find(filter_param).sort('_id', pymongo.DESCENDING)
        return custom_paginated_response([movie for movie in movies], request.base_url, offset, page_limit)
        # if you want to return as html page directly! 
        # movies = respnose.json['data']
        # return render_template("movies.html", len = len(movies), movies = movies)

    @authenticate
    def post(self):
        movie = request.json
        if mongo.db.movies.find_one({'name': movie.get('name'), 'director': movie['director']}):
            return custom_response([], 'Duplicate Movie Being Created', 412)
        mongo.db.movies.insert_one(movie)
        return custom_response(movie, 'Object created Successfully.', 201)

@name_space.route('/movies/<id>')
class MovieApi(Resource):
    @authenticate
    def put(self, id):
        movie = request.json
        id = movie.pop('_id', None)
        if not mongo.db.movies.find_one({"_id": ObjectId(id)}):
            return custom_response([], 'Movie not found', 412)

        mongo.db.movies.update_one({"_id": ObjectId(id)}, {"$set": movie})
        return custom_response([], 'Object Updated Successfully.', 412)

    @authenticate
    def delete(self, id):
        delete_result = mongo.db.movies.delete_one({"_id": ObjectId(id)})

        if delete_result.deleted_count == 1:
            return custom_response([], 'Success.', 201)

        return custom_response([], 'Movie Not found', 412)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=DEBUG)
