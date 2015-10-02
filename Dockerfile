FROM debian
MAINTAINER Markus Lindberg <markus@lindberg.io>

RUN apt-get update && apt-get install -y \
	python-mysqldb \
	python-pip \
	python-configparser \
	libffi-dev \
	libssl-dev \
	python-dev

RUN pip install tvdb_api \
	pyopenssl \
	praw

RUN pip install --upgrade cffi

RUN pip install --upgrade pyopenssl

COPY . /

CMD ["python", "reddit-episode-bot.py"]
