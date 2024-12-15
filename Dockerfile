FROM python:3.11-alpine
ENV HOME=/root
RUN mkdir -p /server
WORKDIR /server
COPY requirements.txt /server
RUN pip3 install -r requirements.txt
COPY server.py /server
COPY config.json /server
COPY airQ.db /server
RUN mkdir -p /server/public
COPY public/index.html /server/public
COPY public/Lyne.js /server/public
RUN chmod 744 /server/server.py
EXPOSE 8080
ENTRYPOINT ["python3", "-u", "/server/server.py"]