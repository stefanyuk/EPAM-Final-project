# Restaurant App

## Description

Restaurant app is a web application that will have several users. Among them are:
- Managers
- Customers

The purposes of the application are: 
- to make an easy process of ordering food
- to create a good management system for manager

Application uses RESTful web service to perform CRUD operations.

## Technologies

- Python 3.8 or higher
- Bootstrap
- Jquery
- Javascript
- Postgresql database


## Installing and using Postgresql

In case if you have some difficulties to set up the PostgreSQL database there is presented such a small tutorial (for Ubuntu 18.04 or 20.04):

1. Download PostgreSQL:
> sudo apt update
> sudo apt install postgresql postgresql-contrib

you will be prompt to type Y | N type Y to continue

2. Using the service command, check the PGSQL service status, if the service is down we will start it up.

> sudo service --status-all

If [-] PostgreSQL it means that server is down. In case if [+] PostgreSQL you can use it.

3. Connect to basic account
> sudo -i -u postgres psql

4. Create restwebapp database:
> createdb restwebapp

## Setup

1. Clone the repo
> git clone https://github.com/stefanyuk/EPAM-Final-project.git

2. Create virtual environment in project
> cd EPAM-Final-project
> python3.9 -m venv venv
> source venv/bin/activate

3. Install project requirements
> pip install -r requirements.txt

4. Prepare the database for usage
Postgresql must already be installed in the system. 
Setup environment variables for the database configuration or change the config file.

Example configuration: 
> 'postgresql://postgres:1234@localhost:5432/restwebapp'

5. Run the migration scripts to create database schema:
> flask db init - further use is optional, in case of intentional reinstallation
> flask db migrate
> flask db update


![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")