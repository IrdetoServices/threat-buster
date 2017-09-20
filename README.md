Threat Buster is a tool to gather, analyse and track responses to threats. It's a research tool from Irdeto that is currently being developed.

# Contributing

Pull requests are welcome, commit should be commented and should have our license header on all files.

```
__copyright__ = """

    Copyright 2017 Irdeto BV

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""
__license__ = "Apache 2.0"
```

# Setup for Mac

* Install Pycharm - https://www.jetbrains.com/pycharm/
* Install Brew - http://brew.sh/
* Run
```
brew install python3 postgres
brew services start postgresql
npm install -g bower
createdb threat-buster
pip install virtualenv
pip install virtualenvwrapper
```
* Add to your .profile
```
export WORKON_HOME=~/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
```
* If it doesn't exist create WORKON_HOME
* Create a Python3 virtualenv
```
mkvirtualenv -p /usr/local/bin/python3 threat-buster
```
* Change to wherever you checked this out
```
setvirtualenvproject threat-buster
```
* Load dependencies
```
pip install -r requirements.txt
```
* Open in Pycharm
* Set interpreter to be .virtualenvs/threat-buster/bin/python3 in project settings

# Running

## In Pycharm with manage.py

In tools -> Run Manage.Py task
* migrate
* runserver
* createsuperuser

## In Pycharm with menus

Use the Run menus


## On the command line
run manage.py on the command line
```
workon threat-buster
python manage.py migrate
python manage.py runserver
python manage.py  bower install
python manage.py  collectstatic

```

# What's here

* django app
* All Auth enabled configured for local logins
* CSS from http://startbootstrap.com/
* Simple model for tenants/endpoints
* django-tables-2 is used to render tables in user app
* django-crud-builder is used for editing endpoints
* elastic beanstalk deployment
