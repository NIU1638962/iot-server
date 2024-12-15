#!/bin/bash
echo "Execute stop."
bash stop_container.sh

echo "Checking if server container exists and stopped."
if [ "docker container ls -f status=exited -f name=server -a | tail +2 | head -1 | wc -m" == 0 ]
then
    echo "Does not exist server container that is stopped."
else
    echo "Does exist server container that is stopped. Removing server container."
    docker remove server
fi