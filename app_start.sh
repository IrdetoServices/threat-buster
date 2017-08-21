#!/usr/bin/env bash

if [ -n "$CONFIG_BUCKET" ]; then

    cd /var/app
    . bin/activate

    # Must check s3 region as in some regions calling without --region fails
    REGION=`aws s3api get-bucket-location --bucket $CONFIG_BUCKET --output text`
    aws s3 cp s3://$CONFIG_BUCKET/local_settings.py portal/local_settings.py --region $REGION

    ./manage.py migrate --noinput
    ./manage.py createsu
    ./manage.py bower_install --allow-root
    ./manage.py collectstatic --noinput
fi

/uwsgi-start.sh