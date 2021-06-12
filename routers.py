from movies import MoviesApi, MovieApi


def initialize_routes(api):
    api.add_resource(MoviesApi, '/api/movies/')
    api.add_resource(MovieApi, '/api/movies/<id>')
    # api.add_resource(SignupApi, '/auth/signup/')
    # api.add_resource(LoginApi, '/auth/login/')
