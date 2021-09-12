FROM python:3
WORKDIR /data
COPY . /data
RUN pip install requests bs4 pandas numpy fake_useragent