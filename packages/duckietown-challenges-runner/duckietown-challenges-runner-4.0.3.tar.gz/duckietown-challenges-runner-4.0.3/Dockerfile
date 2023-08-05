FROM ubuntu:18.04

RUN apt-get update \
    && apt-get install -y \
	curl \
	git \
	docker.io \
	python-pip \
	python-psutil \
    && curl -L https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose \
    && chmod +x /usr/local/bin/docker-compose \
    && apt-get remove -y curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /project

RUN apt-get update
RUN apt-get install -y python3 python3-pip

COPY requirements.txt .

ARG REFRESHED_REQS=5

RUN pip3 install -r requirements.txt

COPY  . .

RUN python3 setup.py develop --no-deps

RUN pip3 freeze
RUN dt-challenges-evaluator --version

CMD ["dt-challenges-evaluator"]
