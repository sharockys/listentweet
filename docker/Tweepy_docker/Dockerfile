FROM python:3.8-slim-buster

WORKDIR /listentweet

COPY requirements.txt .
COPY setup.py .
COPY listentweet listentweet

RUN apt update && apt install git -y
RUN ls
RUN pip install -r requirements.txt

CMD ["python", "listentweet/data/tweepy_wrapper.py"]