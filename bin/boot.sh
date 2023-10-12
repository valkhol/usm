#!/bin/sh

set -ev

host="0.0.0.0"
port="8110"

python app/service/mongo_data_creator.py
python app/service/init_elasticsearch.py

echo " APPLICATION STARTED: host: ${host}  port: ${port}"
uvicorn --host ${host} --port ${port} --factory app.app:create_app