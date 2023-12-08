FROM python:3.12
LABEL authors="Alex Sokolov"

WORKDIR /code

#
COPY ./req.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install --upgrade pydantic

#
COPY ./app /code/app

#
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]