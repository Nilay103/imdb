
# Movies CRUD API using Flask and Mongodb.

Howdy! Welcome to the Flask Rest API. In this project I've tried to create a simple Movies CRUD API and authentication by using Flask, pymongo and jwt.

To run this project: 
  1. Git clone repo
  2. [create](https://docs.python.org/3/library/venv.html) a virtual environment. 
  3. activate virtual env.
  4. pip install -r requirements.txt
  5. [install](https://docs.mongodb.com/manual/administration/install-community/) mongodb and create database. (optional: you can use Atlas cluster too.)
  6. create config.ini file in same project folder.
  
  ```
    [main]
    SECRET_KEY = your secret key
    DEBUG = True/False

    [database]
    MONGODB_URL = mongodb://localhost:27017/db_name or connection url of your Atlas cluster.

    [logging]
    folder = /var/log/imdb_logs

  ```
  7. run: python app.py
  8. TO run test cases: python -m unittest test.py
  
  loadtest result for 70000 entries. (After applying caching!)
  ![Screenshot from 2021-06-13 22-57-08](https://user-images.githubusercontent.com/43541680/121816813-60be1800-cc9b-11eb-87e9-d230030a8ba2.png)
  
For documentation you can visit swagger:
![Screenshot from 2021-06-15 00-38-14](https://user-images.githubusercontent.com/43541680/121947793-18265d80-cd74-11eb-8891-b883ea90d593.png)

For working demo please visit [this](http://35.174.139.2/api/movies/).

To download docker image please visit [this](https://hub.docker.com/repository/docker/nilay103/dockerhub).
