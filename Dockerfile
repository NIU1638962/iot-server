FROM python:3.11-alpine
ENV HOME=/root
RUN mkdir -p $HOME/.aws
COPY .aws $HOME/.aws
RUN mkdir -p /server
WORKDIR /server
COPY requirements.txt /server
RUN pip3 install -r requirements.txt
COPY server.py /server
COPY config.json /server
RUN chmod 744 /server/server.py
EXPOSE 8080
ENTRYPOINT ["python3", "/server/server.py"]