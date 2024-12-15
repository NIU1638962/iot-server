#!/bin/bash
bash delete_container.sh

docker run -d --name server -p 8080:8080 server