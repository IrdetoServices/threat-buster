#!/usr/bin/env bash

LC_CTYPE=C
DB_USER=`cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 16 | head -n 1`
DB_PASSWORD=`cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 40 | head -n 1`

aws cloudformation create-stack --stack-name threat-buster$1 --template-body file://cloudformation/rds.yaml --parameters ParameterKey=DBUser,ParameterValue=$DB_USER ParameterKey=DBPassword,ParameterValue=$DB_PASSWORD ParameterKey=BaseName,ParameterValue=threatbuster --region eu-west-2 --capabilities CAPABILITY_IAM