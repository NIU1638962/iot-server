#!/bin/bash
cp -r ~/.aws .aws
docker build --tag server .
rm -f -R -d .aws