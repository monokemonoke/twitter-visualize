FROM python:3.8

WORKDIR /app

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

COPY requirements.txt requirements.txt 
COPY ipaexg00401/ipaexg.ttf ipaexg00401/ipaexg.ttf
RUN pip install -r requirements.txt
EXPOSE 5000

COPY ./app /app


CMD ["python", "app.py"]
