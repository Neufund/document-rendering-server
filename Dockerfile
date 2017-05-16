FROM python:3.4

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app
ENV PYTHONPATH $PYTHONPATH:/urs/src/app

ADD requirements.txt .
RUN pip install -r requirements.txt
ADD uwsgi.ini uwsgi.ini
ADD *.py /usr/src/app/

ENV FLASK_DEBUG 0
ENV FLASK_HOST 0.0.0.0
ENV FLASK_APP server

ENV SERVER_IP 0.0.0.0
ENV IPFS_PORT 5001
EXPOSE 5000

CMD ["uwsgi", "--ini", "uwsgi.ini"]