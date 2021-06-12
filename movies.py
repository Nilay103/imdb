from flask import request
from flask_restful import Resource
from database import mongo
from customs import custom_response
from authentication import authenticate
from bson.objectid import ObjectId

class MoviesApi(Resource):
    def get(self):
        filter_params = {}
        for filter_key, value in request.args.items():
            filter_params[filter_key] = {"$regex": "/.*" + value[0] + ".*/"}
        movies = mongo.db.movies.find(filter_params)
        return custom_response([movie for movie in movies], 'Success.', 201)

    # @authenticate()
    def post(self):
        movie = request.json
        id = mongo.db.movies.insert(movie)
        new_movie = mongo.db.movies.find_one(id)
        return custom_response(new_movie, 'Object created Successfully.', 201)

class MovieApi(Resource):
    # @authenticate()
    def put(self, id):
        movie = request.json
        id = movie.pop('_id', None)
        if not mongo.db.movies.find_one({"_id": ObjectId(id)}):
            return custom_response([], 'Movie not found', 412)

        mongo.db.movies.update_one({"_id": ObjectId(id)}, {"$set": movie})
        return custom_response([], 'Object Updated Successfully.', 412)

    # @authenticate()
    def delete(self, id):
        movie = request.json
        id = movie.pop('_id', None)
        delete_result = mongo.db.movies.delete_one({"_id": ObjectId(id)})

        if delete_result.deleted_count == 1:
            return custom_response([], 'Success.', 201)

        return custom_response([], 'Movie Not found', 412)
