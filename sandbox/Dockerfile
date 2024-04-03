FROM python:3.8

COPY . /sandbox

WORKDIR /sandbox

RUN pip install poetry

RUN poetry install --only sandbox

EXPOSE 9000

CMD ["poetry", "run", "gunicorn", "app:app", "--bind=localhost:9000"]
