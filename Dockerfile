FROM python:3.6

RUN apt-get update
RUN apt-get upgrade -y

RUN apt-get install xfonts-75dpi -y
RUN apt-get install xfonts-base -y
RUN wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl1.0/libssl1.0.0_1.0.2n-1ubuntu5.3_amd64.deb
RUN dpkg -i libssl1.0.0_1.0.2n-1ubuntu5.3_amd64.deb
RUN wget http://security.ubuntu.com/ubuntu/pool/main/libp/libpng/libpng12-0_1.2.54-1ubuntu1.1_amd64.deb
RUN dpkg -i libpng12-0_1.2.54-1ubuntu1.1_amd64.deb
RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.2.1/wkhtmltox-0.12.2.1_linux-jessie-amd64.deb
RUN dpkg -i wkhtmltox-0.12.2.1_linux-jessie-amd64.deb
#
RUN apt-get update
RUN apt-get install libreoffice -y

WORKDIR /app

ADD requirements.txt .
RUN pip install -r requirements.txt
ADD uwsgi.ini uwsgi.ini

COPY . /app

CMD ["uwsgi", "--ini", "uwsgi.ini"]
