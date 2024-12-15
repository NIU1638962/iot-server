#!/bin/bash
echo "Execute stop."
bash stop_container.sh

echo "Checking if server container exists and stopped."
output=$(docker container ls -f status=exited -f name=server -a | tail -n +2 | head -1 | wc -m)

if [ "$output" -gt 0 ];
then
    echo "Does exist server container that is stopped. Removing server container."
    docker remove server
else
    echo "Does not exist server container that is stopped."
fi