FROM python:3
WORKDIR /TFB103-3project
COPY . /TFB103-3project
RUN pip install requests bs4 pandas numpy fake_useragent