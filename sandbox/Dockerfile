FROM python:3.12

COPY . /sandbox

WORKDIR /sandbox

RUN pip install poetry

RUN poetry install --without dev

EXPOSE 9000

CMD ["poetry", "run", "gunicorn", "api.app:app", "--bind=0.0.0.0:9000"]
