FROM python:3.8

COPY ./specification/examples/responses /sandbox/api/examples
COPY ./sandbox /sandbox

WORKDIR /sandbox

RUN pip install poetry && poetry install --without dev

EXPOSE 9000

CMD ["poetry", "run", "gunicorn", "api.app:app", "--bind=0.0.0.0:9000"]
