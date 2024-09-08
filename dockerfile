FROM python:3.12
RUN pip install poetry

WORKDIR /srcs
COPY pyproject.toml poetry.lock ./
COPY srcs srcs
RUN poetry install --no-root

EXPOSE 8000

WORKDIR /srcs/srcs
ENTRYPOINT ["poetry", "run", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
