#!/bin/bash
echo "Execute delete."
bash delete_container.sh

echo "Run container."
docker run -d --name server -p 8080:8080 server