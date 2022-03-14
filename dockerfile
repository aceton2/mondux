FROM python:3.6-slim
RUN pip install flask psycopg2-binary
RUN apt-get update && apt-get install -y netcat
WORKDIR /home/app
CMD ["python"]
