export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

help:
	@echo "Please use 'make <target>' where <target> is one of the following:"
	@echo "  up                                 to run compose."
	@echo "  build                              to build and run docker-compose"
	@echo "  down                               to stop docker-compose"
	@echo "  down-volumes                       to stop docker-compose cleaning up volumes"
	@echo "  restart                            to restart docker-compose"
	@echo "  full-restart                       to restart docker-compose cleaning up volumes and rebuilding images"
	@echo "  logs                               to follow logs"
	@echo "  pre-commit                         to run the pre-commit checks."
	@echo "  test                               to run the tests"
	@echo "  dbdocs                             to generate documentation using dbdocs"
	@echo "  make-migrations                    to create migrations."
	@echo "  migrate                            to apply migrations."
	@echo "  shell                              to open django shell."
	@echo "  dbshell                            to open PSQL shell."
	@echo "  command                            to run django command."

up:
	docker-compose -f local.yml up -d

build:
	docker-compose -f local.yml up -d --build

down:
	docker-compose -f local.yml down

down-volumes:
	docker-compose -f local.yml down --volumes

restart: down up logs

full-restart: down-volumes build logs

logs:
	docker-compose -f local.yml logs -f -t

pre-commit:
	docker-compose -f local.yml run --rm django pre-commit run --all-files $(marker)

test:
	docker-compose -f local.yml run --rm django coverage run --rcfile=.pre-commit/setup.cfg -m pytest $(marker) --disable-pytest-warnings;
	docker-compose -f local.yml run --rm django coverage html --rcfile=.pre-commit/setup.cfg;
	docker-compose -f local.yml run --rm django coverage report --rcfile=.pre-commit/setup.cfg;
	docker-compose -f local.yml run --rm django coverage report --rcfile=.pre-commit/setup.cfg > coverage.txt;
	docker-compose -f local.yml run --rm django coverage json --rcfile=.pre-commit/setup.cfg;
	docker-compose -f local.yml run --rm django coverage xml -i --rcfile=.pre-commit/setup.cfg;

swaggerhub:
	docker-compose -f local.yml run --rm django python manage.py generate_swagger test.yaml -u https://bespot_assesement.herokuapp.com --api-version 1.0.0

make-migrations:
	docker-compose -f local.yml run --rm django python manage.py makemigrations;

migrate:
	docker-compose -f local.yml run --rm django python manage.py migrate;

shell:
	docker-compose -f local.yml exec django python manage.py shell;

dbshell:
	docker-compose -f local.yml exec postgres psql -U admin -d bespot_assesement;

command:
	docker-compose -f local.yml run --rm django python manage.py $(command);
