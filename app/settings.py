import os

# ----- Security -----
SECRET_KEY = os.getenv(
    'SECRET_KEY', '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
)
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 30)
ALGORITHM = "HS256"


# ----- Mongo -----
MONGO_HOST = os.getenv('MONGO_HOST', 'usm-mongo')
MONGO_PORT = os.getenv('MONGO_PORT', 27017)
MONGO_DB = os.getenv('MONGO_DB', 'usm')

MONGO_USER_FILES_BUCKET = os.getenv('MONGO_USER_FILES_BUCKET', 'user_files')
MONGO_POST_FILES_BUCKET = os.getenv('MONGO_POST_FILES_BUCKET', 'post_files')


# ----- Redis -----
REDIS_HOST = os.getenv('REDIS_HOST', 'usm-redis')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
REDIS_DB = os.getenv('REDIS_DB', 0)


# ----- Elasticsearch -----
ELASTICSEARCH_HOST = os.getenv('ELASTICSEARCH_HOST', 'usm-elastic')
ELASTICSEARCH_PORT = os.getenv('ELASTICSEARCH_PORT', 9200)


# ----- Logging -----
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOGGING = dict(
    version=1,
    formatters={
        'f': {
            'format': '%(levelname)-9s %(asctime)s %(name)-12s %(message)s',
            'datefmt': '%d-%b-%y %H:%M:%S',
        }
    },
    handlers={
        'h': {'class': 'logging.StreamHandler', 'formatter': 'f', 'level': LOG_LEVEL}
    },
    root={
        'handlers': ['h'],
        'level': LOG_LEVEL,
    },
)
