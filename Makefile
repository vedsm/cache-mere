create_env:
	virtualenv venv
	echo "now call: source ./venv/bin/activate"

activate_env:
	source ./venv/bin/activate

install:
	pip3 install -r ./requirements.txt

test:
	echo "testing"

run_event_generator:
	echo "TODO: generate some events and push to to recever"

run_event_receiver:
	uvicorn --host 0.0.0.0 --port 5000 src.event_receiving.event_receiver:app

run_event_reader:
	python ./src/event_processing/event_reader.py

package:
	echo "to create a docker build/ python package/code artefacts"
	docker-compose -f ./docker-compose.yml build

publish:
	echo "to publish a created docker image / code artefacts to a cental repository"
	docker-compose -f ./docker-compose.yml push

run_package:
	docker-compose -f docker-compose.yml up

deploy:
	echo "deploying"


start_redis:
	docker-compose -f docker-compose-redis.yaml up -d

play_with_redis:
	docker exec -it cashe-mere_redis_1 /bin/bash

install_redis_ui:
	npm install -g redis-commander

start_redis_ui:
	redis-commander
