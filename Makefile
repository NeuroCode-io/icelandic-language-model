#!make
include .env
export $(shell sed 's/=.*//' .env)
version := $(shell git rev-parse --short HEAD)

.PHONY: all install version clean lint build

all:	clean install

install:
	poetry install

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name .cache -exec rm -rf {} +
	find . -name .pytest_cache -exec rm -rf {} +
	find . -name __pycache__ -exec rm -rf {} +

format:
	black .

deploy:
  poetry export --output requirements.txt
	docker build -t donchev7/icelandic-model:v$(version) .
	docker push donchev7/icelandic-model:v$(version)


create_machine:
	azure/create_vm.sh

delete_machine:
	azure/delete_vm.sh
