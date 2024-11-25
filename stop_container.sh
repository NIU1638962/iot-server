#!/bin/bash
if [ "docker container ls -f status=running -f name=server -a | tail +2 | head -1 | wc -m" != 0 ]
then
    docker stop server
fi