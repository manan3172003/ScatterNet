FROM python:3.12-alpine


WORKDIR /frontend

RUN apk update && apk add --no-cache nodejs npm

COPY ./frontend /frontend/

RUN npm install

RUN npm run build

WORKDIR /backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./backend/requirements.txt /backend/
RUN pip install -r requirements.txt

COPY ./backend /backend/

RUN python manage.py collectstatic --no-input