FROM python:3.6

RUN apt-get update
RUN apt-get upgrade -y

RUN apt-get install xfonts-75dpi -y
RUN apt-get install xfonts-base -y
RUN wget https://downloads.wkhtmltopdf.org/0.12/0.12.2.1/wkhtmltox-0.12.2.1_linux-jessie-amd64.deb
RUN dpkg -i wkhtmltox-0.12.2.1_linux-jessie-amd64.deb
#
RUN apt-get install libreoffice -y

COPY . /app
WORKDIR /app

ADD requirements.txt .
RUN pip install -r requirements.txt
ADD uwsgi.ini uwsgi.ini

CMD ["uwsgi", "--ini", "uwsgi.ini"]