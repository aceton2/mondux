FROM python:3.6-slim
RUN pip install flask psycopg2-binary
WORKDIR /home/app
CMD flask run -h 0.0.0.0
