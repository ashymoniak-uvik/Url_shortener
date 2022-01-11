FROM python:3.10

# set environment variables
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

ADD ./requirements.txt /app/

# Install the pip requirements file depending on

RUN pip install -Ur requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]