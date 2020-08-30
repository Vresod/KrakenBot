FROM python

WORKDIR /src

COPY . . 

CMD python3 kraken.py
