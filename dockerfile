FROM python:3.6-slim
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
RUN apt-get update && apt-get install -y netcat
WORKDIR /home/app
CMD ["python"]
