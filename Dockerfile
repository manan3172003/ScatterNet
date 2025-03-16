FROM python:3.12-alpine

WORKDIR /frontend

RUN apk update && apk add --no-cache nodejs npm

COPY ./frontend/package*.json /frontend/

RUN npm install

WORKDIR /backend

# Environment settings
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Python dependencies
COPY ./backend/requirements.txt /backend/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

WORKDIR /frontend

COPY ./frontend /frontend/

RUN npm run build

WORKDIR /backend

# Copy backend code
COPY ./backend /backend/

# Collect Django static files
RUN python manage.py collectstatic --no-input