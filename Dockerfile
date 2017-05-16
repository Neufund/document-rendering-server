FROM python:3.4

RUN apt-get update
RUN apt-get upgrade -y

RUN apt-get install xfonts-75dpi -y
RUN apt-get install xfonts-base -y
RUN wget http://download.gna.org/wkhtmltopdf/0.12/0.12.2.1/wkhtmltox-0.12.2.1_linux-jessie-amd64.deb
RUN dpkg -i wkhtmltox-0.12.2.1_linux-jessie-amd64.deb
#
RUN apt-get install libreoffice -y

RUN mkdir -p /develop/tmp/
COPY . /app
WORKDIR /app
#
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD uwsgi.ini uwsgi.ini
#
ENV FLASK_DEBUG 0
ENV FLASK_HOST 0.0.0.0
ENV FLASK_APP server

EXPOSE 5000

CMD ["uwsgi", "--ini", "uwsgi.ini"]