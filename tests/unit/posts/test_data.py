# ---------------------------------
# ---------- CREATE POST ----------
# ---------------------------------

POST_DATA_WITH_FILE = {
    'url': None,
    'file': b"test",
    'user': None,
    'topic': 'test-topic',
    'description': 'test-description',
}

POST_DATA_WITH_URL = {
    'url': 'some-url.com',
    'file': None,
    'user': None,
    'topic': 'test-topic',
    'description': 'test-description',
}

POST_DATA_WITH_WRONG_URL = {
    'url': 'some-url-wrong.com',
    'file': None,
    'user': None,
    'topic': 'test-topic',
    'description': 'test-description',
}

POST_DATA_WITH_URL_WITH_FILE = {
    'url': 'some-url.com',
    'file': b"test",
    'user': None,
    'topic': 'test-topic',
    'description': 'test-description',
}

POST_DATA_NO_URL_NO_FILE = {
    'url': 'some-url.com',
    'file': b"test",
    'user': None,
    'topic': 'test-topic',
    'description': 'test-description',
}

# ---------------------------------
# ---------- CREATE POST ----------
# ---------------------------------

UPDATE_POST_DATA = {
    'url': 'update-some-url.com',
    'file': None,
    'user': None,
    'topic': 'update-test-topic',
    'description': 'update-test-description',
}
