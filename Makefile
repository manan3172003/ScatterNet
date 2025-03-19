install-requirements:
	cd ./backend && \
	pip install -r requirements.txt

migrations:
	python ./backend/manage.py makemigrations
	python ./backend/manage.py migrate

build-frontend:
	cd ./frontend && \
	npm install && \
	npm run build && \
	cd .. && \
	python ./backend/manage.py collectstatic --no-input

clean-db:
	python ./backend/manage.py clear_db

populate-db:
	python ./backend/manage.py add_initial_data

build-backend: install-requirements clean-db migrations populate-db
	python ./backend/manage.py runserver

run-app-local: build-frontend build-backend

run-app-docker:
	docker compose up --build

run-migrations-docker:
	docker compose exec dodgerblue python manage.py makemigrations
	docker compose exec dodgerblue python manage.py migrate

run-tests:
	docker compose build test
	docker compose run --rm test