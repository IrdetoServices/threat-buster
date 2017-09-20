#!/usr/bin/env bash

LC_CTYPE=C
DB_USER=`cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 16 | head -n 1`
DB_PASSWORD=`cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 40 | head -n 1`


while getopts n:c: o
do	case "$o" in
	n)	NAME="$OPTARG";;
	c)	CERT="$OPTARG";;
	[?])	print >&2 "Usage: $0 [-n] Name -c CERTARN"
		exit 1;;
	esac
done

aws cloudformation create-stack --stack-name threat-buster$NAME --template-body file://cloudformation/rds.yaml --parameters ParameterKey=DBUser,ParameterValue=$DB_USER ParameterKey=DBPassword,ParameterValue=$DB_PASSWORD ParameterKey=BaseName,ParameterValue=threatbuster ParameterKey=DNSName,ParameterValue=$NAME ParameterKey=CertificateARN,ParameterValue=$CERT --region eu-west-2 --capabilities CAPABILITY_IAM