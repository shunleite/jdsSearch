FROM python:3.8

RUN mkdir -p /usr/src/app/jds_search

RUN git clone https://github.com/shunleite/jdsSearch.git /usr/src/app/jds_search

WORKDIR /usr/src/app/jds_search

#ADD ./requirements.txt /usr/src/app/jds_search/requirements.txt

RUN pip install -r /usr/src/app/jds_search/requirements.txt

ADD . /usr/src/app/jds_search

# RUN
CMD streamlit run /usr/src/app/jds_search/stCloudForSt.py --server.port=8055 --server.headless=true --global.developmentMode=false