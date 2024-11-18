FROM python:3.11-alpine
RUN mkdir -p /server
WORKDIR /server
COPY server.py /server
RUN chmod 744 /server/server.py
EXPOSE 8080
ENTRYPOINT ["python3", "/server/server.py"]