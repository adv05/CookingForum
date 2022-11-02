FROM python:3.10-slim-buster

# Metadata
LABEL name="CookingForum"
LABEL maintainer="AntonioDV"
LABEL version="0.1"

ARG YOUR_ENV="virtualenv"

ENV YOUR_ENV=${YOUR_ENV} \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.2.2 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

# Install poetry dependencies
RUN DEBIAN_FRONTEND=noninteractive apt update && apt install -y libpq-dev gcc curl

# Install project libraries
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN pip install "poetry==$POETRY_VERSION"

# Project Python definition
WORKDIR /admin-app

# Copy relevant project files
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry config virtualenvs.create false \
    && poetry install $(test "$YOUR_ENV" = production) --no-dev --no-interaction --no-ansi
COPY app .
COPY .env .

# Load my modules
ENV PYTHONPATH="/workspaces/CookingForum/app"

# Run tests
CMD ["pytest", "-rA", "/admin-app/test"]