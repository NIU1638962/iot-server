#!/bin/bash
bash stop_container.sh

if [ "docker container ls -f status=exited -f name=server -a | tail +2 | head -1 | wc -m" != 0 ]
then
    docker remove server
fi