## I have learned

- fast api -> auto documentation
- postgresql
- using raw sql in your api or use orm (sqlalchemy)
- database migration tool - alembic
- automatic integration testing
- deployment -> on ubuntu (Ec2 machine), nginx , firewall , ssl / use heroku , or use docker

# python virtual environment

- project1 - need fastapi : (v1.2.3) -> installed in my local computer
- project2 - need fastapi : (v1.2.4) -> now my above on ewill crash

so create a virtual env for each project (they are seperate out and ony my project us using it)

- project1 - need fastapi -> venv-1 : (v1.2.3) -> installed in my project env
- project2 - need fastapi -> venv-2 : (v1.2.4) -> now no problem

```shell
 python3 -m venv venv
 source venv/bin/activate.  # activating our venv in terminal
```

to check module installed

```shell
   pip3 freeze
```

run unicorn server

```shell
uvicorn main:app --reload.    # similar to nodemon , uvicorn file_name:fast_api_instance --reload
```

## schema

- client can send me anything to my route
- we need to validate if the data that user send is correct
- we define a schema -> basically tell how our data looks , and we asked user to send data in that scehma otherwise we wills how error
- i want to get data like this, otherwie i will not do anything

- we use pydantic (already installed with fastapi) -> we use it to create schema for our api

## inbuilt docmentation

- just access - `url/docs` or use `url/redoc`

- whenever creating a new folder add `__init__.py` to make it a module so you can access it
- suppose , you have created an folder named app and put your main.py inside it
- run server using this `uvicorn app.main:app --reload`

## DBMS

- when we interact with , we do not do it directly
- we use a software called dbms , who do it in behalf of us

- we are going to use postgresql dbms

## installing postgres

- we install postgres server and run a instance in our local machine (could create multiple instances)
- an instance can have multiple database and you can one database for one and one for another
- as you install postgres server , it would have postgres server , it comes with one database inside it named `postgres`

- open server in terminal - `/Library/PostgreSQL/16/scripts/runpsql.sh; exit`

## basics terms postgres

- **primary_key** : only one , unique , you can make any column as primary_key
- **constraints**
  - **unique** : apply on column , no duplicate value
  - **not null** : can't pass null

## Some Commands (Basic not complete)

- create database

```sql
CREATE DATABASE <database_name>;
```

- check in which database you are currently in

```sql
SELECT current_database();
```

- check list of all database in my instance

```sql
\l
```

- change to a different database

```sql
\c <database_name>;
```

- print table with selected and with some condition

```sql
SELECT name, price FROM products WHERE price > 50 AND price < 60;

SELECT name, price FROM products WHERE price IN (20,30,34,50);

SELECT name, price FROM products WHERE name LIKE 'TV%';        /* eveything start with tv will print */

SELECT name, price FROM products ORDER BY price DESC LIMIT 5 OFFSET 5;              /* in DESC order on the basis of price , i got five row after leaving first 5 */
```

- raw sql complete notes (link)[https://github/abhi1992002]

## Psycopg2

- its a postgreql adapters or driver (something like mongoose)
- use to connect python with postgres and execute sql queries in python

- install psycopg2

```shell
pip3 install psycopg2
```

- for development

```shell
pip install psycopg2-binary
```

## sqlAlchemy

- sits between us and databse
- we write code in python , it covert it to sql , talk to database

## installtion ORM

```sql
pip install sqlalchemy
```

## Albemic

- our sql can't directly do migration (means not able alter the database schema)
