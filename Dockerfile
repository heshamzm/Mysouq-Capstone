  
FROM python:3.7-alpine
RUN mkdir /capstone
WORKDIR /capstone
ADD requirements.txt .
RUN pip3 install -r requirements.txt
COPY app/ .
ENTRYPOINT ["sh"]