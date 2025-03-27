FROM python:3.12-slim as base

# ENV PYTHONUNBUFFERED=1

RUN apt-get update -y \
    # dependencies for building Python packages && cleaning apt apt packages
    && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --upgrade pip setuptools pipenv watchdog

# aka ``cp`` on unix
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy

# copy the project
WORKDIR /app/
COPY ./ ./


# DEV IMAGE
from base as dev
EXPOSE 8000
ENTRYPOINT ["python"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]

# PRODUCTION IMAGE
from base as prod

ENV GUNICORN_CMD_ARGS="--bind 0.0.0.0:8000"

EXPOSE 8000
ENTRYPOINT ["python"]
CMD ["-m", "gunicorn", "config.wsgi"]
