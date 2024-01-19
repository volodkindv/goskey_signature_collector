FROM python:3.10-slim-bullseye

WORKDIR /app

RUN pip install poetry
RUN poetry config virtualenvs.create false
COPY ./pyproject.toml /app
COPY ./poetry.lock /app
RUN poetry install --only main --no-interaction --no-ansi --no-root

COPY ./src/bot /app/bot
COPY ./src/run_bot.py /app
COPY ./src/__init__.py /app

CMD ["python3",  "run_bot.py"]
