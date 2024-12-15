#!/bin/bash
echo "Stop container."
echo "Checking if server container exists and running."
output=$(docker container ls -f status=running -f name=server -a | tail +2 | head -1 | wc -m)

if [ "$output" -gt 0 ];
then
    echo "Does exist server container that is running. Stopping server container."
    docker stop server
else
    echo "Does not exist server container that is running."
fi