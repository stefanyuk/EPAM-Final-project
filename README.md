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


## Installing and using PostgreSQL

In case if you have some difficulties to set up the PostgreSQL database there is presented a small tutorial (for Ubuntu 20.04):

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

***
## Setup

1. Clone the repo
> git clone https://github.com/stefanyuk/EPAM-Final-project.git

2. Create virtual environment in project
> cd EPAM-Final-project

> python3.9 -m venv venv

> source venv/bin/activate

3. Install project requirements
> pip install -r requirements.txt

4. Prepare the database for usage. Postgresql must already be installed in the system. 
Setup environment variables for the database SQLalchemy configuration or change the config file.

Example configuration: 
> 'postgresql://postgres:1234@localhost:5432/restwebapp'

5. Run the migration scripts to create database schema:
> flask db init - further use is optional, only in case of intentional reinstallation
> flask db migrate
> flask db update

6. Run flask populate-db command to create test data (make sure you set up environment variables for flask app):
> flask populate-db

7. Admin user will be created automatically after you run "flask populate-db" command. You can use following credentials 
to login and to use API:
> username: admin

> password: admin
---

After these steps you should see the home page of the application

![alt text](https://github.com/stefanyuk/EPAM-Final-project/blob/main/documentation/mockups/welcome.png "Logo Title Text 1")


## API Operations

Current API version - __1__. Each API url should start with __/api/v1__


* /users
  * GET - get all users in json format
  * POST - create a new user

* /users/user_id
  * GET - get user with a given id in json format
  * PATCH - update user with a given id
  * DELETE - delete user with a given id
---
* /employees
  * GET - get all employees in json format
  * POST - create a new employee

* /employees/employee_id
  * GET - get employee with a given id in json format
  * PATCH - update employee with a given id
  * DELETE - delete employee with a given id
---
* /departments
  * GET - get all departments in json format
  * POST - create a new department

* /departments/department_id
  * GET - get department with a given id in json format
  * PATCH - update department with a given id
  * DELETE - delete department with a given id
---
* /orders
  * GET - get all orders in json format
  * POST - create a new order

* /orders/order_id
  * GET - get order with a given id in json format
  * PATCH - update order with a given id
  * DELETE - delete order with a given id
