poetry run gunicorn -w 4 --reload --bind 0.0.0.0:10101 "myfirstaimodel:create_app()"
