FROM python

WORKDIR /src

COPY . . 

RUN pip3 install discord

CMD python3 kraken.py
