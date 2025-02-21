migrations:
	python ./backend/manage.py makemigrations
	python ./backend/manage.py migrate

run-backend:
	docker compose up --build

tests:
	docker compose build test

run-tests:
	docker compose run test