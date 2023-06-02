FROM python:3.11-alpine3.18

WORKDIR /code

COPY requirements.txt /code

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["python3", "-m", "flask", "run", "--debug", "--host=0.0.0.0"]