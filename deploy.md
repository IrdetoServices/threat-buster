# Deployment to AWS

This project is setup up to deploy to AWS via a combination of CloudFormation and Elastic Beanstalk. 

# To create a new environment

## Pre-reqs

* AWS Account
* Working AWS CLI

## Creation

* Run ``` deploy.sh ```
    * Optionally edit the params if you want to rename things
* Wait for it to complete the cloud formation (take 10-15 mins)
* Connect project to the EB
    * ``` eb init ``` (note if you have already used eb remove .elasticbeanstalk)
        * Select the application CF created
    * ``` eb list ``` (find the environment it created)
    * ``` eb use OUTPUT_OF_LAST_COMMAND```
    * ``` eb deploy```
    
## Configuration

* Review portal/aws_local_settings_template.py
** Set any settings you want and upload to root of the config bucket created by the cloud formation as local_settings.py

## Deleting an environment

* Delete the cloud formation
* It will fail to delete the S3 buckets - manually empty them and re-run the delete
    * You could do this first but due to the smartness of EB it may repopulate them in the meantime so simplest to do it this way round!

## Extras

* If you want to enable X-ray either modify CF or edit the Elastic Beanstalk settings in AWS Console