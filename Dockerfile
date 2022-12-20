# pull official base image
FROM python:3.8.6-slim-buster

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.3.1\
    PYTHONUNBUFFERED=1\
    PYTHONDONTWRITEBYTECODE=1

####### Install Poetry ############
RUN pip install --upgrade pip

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc \
  && apt-get clean

RUN pip install "poetry==$POETRY_VERSION"

# Make poetry available
ENV PATH="${PATH}:/root/.poetry/bin"
######################################

# Copy project files
COPY poetry.lock pyproject.toml ./

# install python dependencies
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi


# add app
COPY . .