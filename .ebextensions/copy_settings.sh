#!/bin/bash
echo $CONFIG_BUCKET

# Param1 has in it environment name according to docs
aws s3 cp s3://$CONFIG_BUCKET/local_settings.py portal/local_settings.py