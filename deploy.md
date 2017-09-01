The command to deploy to eb is

As a one time activity create the RDS DB - this is NOT part of the EB deployment as you may want your RDS database to survive a rebuild.

aws cf ....
eb create --envvars CONFIG_BUCKET=YOUR_BUCKET,SUPER_USER_NAME=YOUR_USERNAME,SUPER_USER_PASSWORD=YOUR_PASSWORD,SUPER_USER_EMAIL=YOUR_EMAIL --elb-type application

