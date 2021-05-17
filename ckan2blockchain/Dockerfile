FROM python:3.8.5

WORKDIR .
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install autoconf
RUN apt-get install dh-autoreconf -y
RUN apt-get install libssl-dev -y
RUN apt install build-essential automake pkg-config libtool libffi-dev libgmp-dev -y
RUN apt install libsecp256k1-dev -y
RUN pip3 install eth-testrpc
RUN pip3 install eth-tester
RUN pip3 install 'rlp==0.6.0'
RUN pip3 install python-dotenv
COPY . .
RUN pwd
EXPOSE 3000
CMD [ "python3", "main.py" ]
