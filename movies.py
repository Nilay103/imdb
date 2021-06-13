from bson.objectid import ObjectId
from flask import request
from flask_pymongo import pymongo
from flask_restful import Resource

from authentication import authenticate
from constants import DEFAULT_PAGE_LIMIT
from customs import custom_response, custom_paginated_response
from database import mongo
from cache import cache


class MoviesApi(Resource):
    @cache.cached(timeout=50)
    def get(self):
        search_param = request.args.get('search')
        filter_param = {"$text": {"$search": search_param}} if search_param else None

        page_limit = int(request.args.get('limit', DEFAULT_PAGE_LIMIT))
        offset = int(request.args.get('offset', 0))

        movies = mongo.db.mo1.find(filter_param).sort('_id', pymongo.DESCENDING)
        # return json.loads(json_util.dumps((movies)))
        return custom_paginated_response([movie for movie in movies], request.base_url, offset, page_limit)

    @authenticate
    def post(self):
        movie = request.json
        # mongo.db.mo1.insert_many(movie)
        # return custom_response([], '.', 201)
        if mongo.db.movies.find_one({'name': movie.get('name'), 'director': movie['director']}):
            return custom_response([], 'Duplicate Movie Being Created', 412)
        movie['_id'] = mongo.db.movies.insert_one(movie)
        return custom_response(movie, 'Object created Successfully.', 201)


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
