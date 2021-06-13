from flask import request
from flask_restful import Resource
from database import mongo
from customs import custom_response, custom_paginated_response
from constants import DEFAULT_PAGE_LIMIT
from authentication import authenticate
from bson.objectid import ObjectId
from flask_pymongo import pymongo

class MoviesApi(Resource):
    # def get(self):
    #     FILTER_FIELDS = ('name', 'year', 'imdb_score', 'director')
    #     filter_params = {}
    #     for filter_key, value in request.args.items():
    #         if filter_key in FILTER_FIELDS:
    #             filter_params[filter_key] = {"$regex": "/.*" + value[0] + ".*/"}

    #     page_limit = int(request.args.get('limit', DEFAULT_PAGE_LIMIT))
    #     offset = int(request.args.get('offset', 0))

    #     starting_id = mongo.db.movies.find(filter_params).sort('_id', pymongo.DESCENDING)
    #     last_id = starting_id[offset]['_id']

    #     next_url = '/api/movies/?' + str(page_limit) + '&offset=' + str(offset + page_limit)
    #     prev_url = '/api/movies/?' + str(page_limit) + '&offset=' + str(offset - page_limit)

    #     movies = mongo.db.movies.find({
    #         '_id': {'$lte': last_id}
    #     }, **filter_params).sort('_id', pymongo.DESCENDING).limit(page_limit)
    #     # .limit(page_limit)
    #     return custom_response([movie for movie in movies], 'Success.', 201)

    def get(self):
        FILTER_FIELDS = ('name', 'year', 'imdb_score', 'director')
        filter_params = {}
        for filter_key, value in request.args.items():
            if filter_key in FILTER_FIELDS:
                filter_params[filter_key] = {"$regex": "/.*" + value[0] + ".*/"}

        page_limit = int(request.args.get('limit', DEFAULT_PAGE_LIMIT))
        offset = int(request.args.get('offset', 0))

        movies = mongo.db.movies.find(filter_params).sort('_id', pymongo.DESCENDING)
        return custom_paginated_response([movie for movie in movies], request.base_url, offset, page_limit)

    @authenticate
    def post(self):
        movie = request.json
        id = mongo.db.movies.insert(movie)
        new_movie = mongo.db.movies.find_one(id)
        return custom_response(new_movie, 'Object created Successfully.', 201)

class MovieApi(Resource):
    # @authenticate
    def put(self, id):
        movie = request.json
        id = movie.pop('_id', None)
        if not mongo.db.movies.find_one({"_id": ObjectId(id)}):
            return custom_response([], 'Movie not found', 412)

        mongo.db.movies.update_one({"_id": ObjectId(id)}, {"$set": movie})
        return custom_response([], 'Object Updated Successfully.', 412)

    # @authenticate
    def delete(self, id):
        movie = request.json
        id = movie.pop('_id', None)
        delete_result = mongo.db.movies.delete_one({"_id": ObjectId(id)})

        if delete_result.deleted_count == 1:
            return custom_response([], 'Success.', 201)

        return custom_response([], 'Movie Not found', 412)
