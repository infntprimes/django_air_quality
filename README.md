# Django_Air_Quality

## Local Installation

#### Setup dependencies:
Make sure you have python3, virtualenv, and mysql installed:

`brew install python mysql`
`pip3 install virtualenv`

Activate a virtual environment: 
`virtualenv env`
`source env/bin/activate`

Install remaining dependencies:
`pip3 install -r requirements.txt`

Google's cloud_sql_proxy is also required when running locally:

(https://cloud.google.com/sql/docs/mysql/sql-proxy#install)


#### To run:

First initialize the cloud sql proxy:

`./cloud_sql_proxy -instances=rb-training:us-central1:rb-training=tcp:3306 \
-credential_file=gae_credentials.json &`

Handle migrations:

`python3 manage.py migrate && python3 manage.py makemigrations`

Finally to execute:

`python3 manage.py runserver`


