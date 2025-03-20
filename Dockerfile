FROM python:3.12-slim

# ENV PYTHONUNBUFFERED=1

# for celery if the root user specified
ENV C_FORCE_ROOT=1

RUN apt-get update -y \
    # Python dependencies && cleaning apt apt packages
    && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --upgrade pip setuptools pipenv watchdog

# aka ``cd``
# WORKDIR /app/

# aka ``cp`` on unix
COPY Pipfile Pipfile.lock ./
# only for dev purposes. use multistage builds or multiple Dockerfiles
RUN pipenv install --system --dev

# copy the project
COPY ./ ./

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
