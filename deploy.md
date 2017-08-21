The command to deploy to eb is

eb create --database --envvars CONFIG_BUCKET=YOUR_BUCKET,SUPER_USER_NAME=YOUR_USERNAME,SUPER_USER_PASSWORD=YOUR_PASSWORD,SUPER_USER_EMAIL=YOUR_EMAIL --elb-type application