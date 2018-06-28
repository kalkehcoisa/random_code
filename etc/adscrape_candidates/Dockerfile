FROM ubuntu:trusty

RUN \
    apt-get update --fix-missing && \
    apt-get install -y \
        libxml2 \
        libxml2-dev \
        libxslt1-dev \
        curl \
        libpq-dev \
        libcurl4-gnutls-dev \
        python3 \
        python3-pip \
        python3-pycurl \
        python3-dev

COPY . /adscrape_candidates/
WORKDIR /adscrape_candidates/

RUN pip3 install -r requirements.txt

CMD ["python3 server.py"]
