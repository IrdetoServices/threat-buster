#!/bin/bash
echo $CONFIG_BUCKET

# Must check s3 region as in some regions calling without --region fails
REGION=`aws s3api get-bucket-location --bucket $CONFIG_BUCKET --output text`
aws s3 cp s3://$CONFIG_BUCKET/local_settings.py portal/local_settings.py --region $REGION