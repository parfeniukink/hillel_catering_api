FROM python:3.12-slim AS base

# ENV PYTHONUNBUFFERED=1

RUN apt-get update -y \
    # dependencies for building Python packages && cleaning apt apt packages
    && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --upgrade pip setuptools pipenv watchdog
COPY Pipfile Pipfile.lock ./
WORKDIR /app/
# copy the project
COPY ./ ./


from base as dev
RUN pipenv sync --dev --system

EXPOSE 8000
ENTRYPOINT ["python"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]


from base as prod
RUN pipenv install --deploy --system

ENV GUNICORN_CMD_ARGS="--bind 0.0.0.0:8000"

EXPOSE 8000
ENTRYPOINT ["python"]
CMD ["-m", "gunicorn", "config.wsgi:application"]
