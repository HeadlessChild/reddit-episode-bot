FROM debian
MAINTAINER Markus Lindberg <markus@lindberg.io>

COPY requirements.txt /

RUN apt-get update && apt-get install -y \
	python-mysqldb \
	python-pip \
	python-configparser \
	libffi-dev \
	libssl-dev \
	python-dev

RUN pip install -r requirements.txt

RUN pip install --upgrade cffi

RUN pip install --upgrade pyopenssl

COPY reddit-episode-bot.py /

CMD ["python", "reddit-episode-bot.py"]
