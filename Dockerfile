FROM python

WORKDIR /src

COPY . . 

RUN pip3 install -r requirements.txt

CMD python3 kraken.py
