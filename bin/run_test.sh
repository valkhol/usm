#!/bin/sh

set -ev

pytest --cov=app --cov-report term-missing -vvv tests
python app/service/mongo_drop_db.py