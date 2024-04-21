FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /app

EXPOSE 8000

CMD ["python", "app.py", "--host=0.0.0.0", "--port=8000"]
