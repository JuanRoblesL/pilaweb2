FROM python:3.11-rc-alpine

WORKDIR /code

ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache gcc musl-dev linux-headers

COPY requeriments.txt requeriments.txt

RUN pip install -r requeriments.txt

COPY . /code/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]