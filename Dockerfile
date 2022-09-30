FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /usr/app/src

RUN apt-get update && yes | apt-get install libmysqlclient-dev 
RUN apt-get -y install python3.10 python3-dev && apt-get -y install python3-pip
RUN yes | apt-get install vim

RUN mkdir DB_Management_Interface
COPY ./c ./DB_Management_Interface/c
COPY ./python/GUI ./DB_Management_Interface/python/GUI
COPY ./python/bindings ./DB_Management_Interface/python/bindings
COPY ./python/tests ./DB_Management_Interface/python/tests
COPY ./python/configure.py ./DB_Management_Interface/python/
COPY ./python/requirements.txt ./DB_Management_Interface/python/


ENV PYTHONPATH "${PYTHONPATH}:/usr/app/src/DB_Management_Interface"


RUN cd ./DB_Management_Interface/c && make clean && make && cd ..
RUN pip3 install -r ./DB_Management_Interface/python/requirements.txt
# RUN python3 -m unittest ./tests/test_*