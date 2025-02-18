migrations:
	python ./backend/manage.py makemigrations
	python ./backend/manage.py migrate

run-backend:
	python ./backend/manage.py runserver