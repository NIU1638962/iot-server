#!/bin/bash
echo "Checking if server container exists and running."
if [ "docker container ls -f status=running -f name=server -a | tail +2 | head -1 | wc -m" == 0 ]
then
    echo "Does not exist server container that is running."
else
    echo "Does exist server container that is running. Stopping server container."
    docker stop server
fi