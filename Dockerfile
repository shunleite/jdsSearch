FROM python:3.8

RUN mkdir -p /usr/src/app/jds_search
WORKDIR /usr/src/app/jds_search

ADD ./requirements.txt /usr/src/app/jds_search/requirements.txt

RUN pip install -r requirements.txt

ADD . /usr/src/app/jds_search

# RUN
CMD streamlit run main.py --server.port=8033 --server.headless=true --global.developmentMode=false