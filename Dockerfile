FROM python:3.12-slim


RUN pip install poetry==1.8.2

WORKDIR /app

COPY pyproject.toml poetry.lock .env ./

#Contents of src will end up in the WORKDIR
COPY src/ ./

RUN touch README.md
RUN poetry install

CMD ["poetry", "run", "uvicorn", "api.app:app", "--host", "0.0.0.0", "--reload"]