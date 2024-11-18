#!/bin/bash
if [ "docker container ls -f status=running -f name=server -a | tail +2 | head -1 | wc -m" != 0 ]
#if [[ $"$(docker container ls -f status=running -a)" == *"server"* ]]
then
    docker stop server
fi 

if [ "docker container ls -f status=exited -f name=server -a | tail +2 | head -1 | wc -m" != 0 ]
then
    docker remove server
fi

docker run -d --name server -p 8080:8080 server