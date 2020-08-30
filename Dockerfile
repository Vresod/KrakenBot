FROM python

WORKDIR /src

COPY . . 

RUN pip3 install discord.py

CMD python3 kraken.py
