# DevOps-360-Webapp
Webapp used in devops-360 project

## 1. Mysql Database
##### 1.1. Running the database in production

* Install a Mysql-Server
* Database schemas and the intial mysql dump are located in the [database](./database) folder.
* Developers will make sure to provide database schema upgrades in  `database/schemas/vX/beerbattle.sql` where `X` is the major realease number of the version. 

> For example [v1.0.0](https://github.com/Lowess/devops-360-webapp/releases/tag/v1.0.0) requires `database/schemas/v1/beerbattle.sql`.

> If you install [v2.0.0](https://github.com/Lowess/devops-360-webapp/releases/tag/v2.0.0) right away, you need to make sure to import the following schemas `database/schemas/v1/beerbattle.sql` and `database/schemas/v2/beerbattle.sql`.

> It is safe to rerun multiple times the schemas/vX/beerbattle.sql imports as they include `IF NOT EXISTS` statements.

* When you setup the database for the first time, you need to make sure to populate the `beer` table with the initial data dump file named [beerbattle.sql](./database/data/beerbattle.sql) (Also available as a CSV file if needed [beerbattle.csv](./database/data/beerbattle.csv)). 
 
> :warning: Do not run the data import twice otherwise you will end up with duplicated data!

## 2. Web application
##### 2.1. Running the application in production

* Install the project dependencies in a [virtualenv](https://virtualenv.pypa.io/en/stable/) with
```
cd <application-root>/
# Once the virtualenv is activated
pip install requirements.txt
```

* In order to override the developement configuration for production, configure the following template and place it under `<application-root>/app/config/prod.py`:

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from app.config.config import Config

class ProductionConfig(Config): 
   ### Mysql config
   MYSQL_SERVER = '127.0.0.1'
   MYSQL_DB = 'beerbattle'
   MYSQL_USER = 'root'
   MYSQL_PWD = 'password'

   ### Webapp custom settings
   # Restrict battles to a specific ID interval [min_id, max_id]
   # BEER_BATTLE_ID_INTERVAL = (1,10)
```

* Once the configuration is in place, make sure the following environment variable is set: `export FLASK_ENV=prod`.

* Now run `python run.py` and that's it :)

>Please note that in production you should not run `python run.py`. You should instead run the application with a tool like (UWSGI)[https://uwsgi-docs.readthedocs.io/en/latest/]

##### 2.2. Application endpoints

###### /heartbeat
-----------------

Returns 200 and a the following message if the application is healthy:

```
The Flask WebApp is healthy
```

###### /info
------------

Returns information about the Webapp:

* `db_conn` (`string`): Database connection string
* `db_conn_state` (`boolean`): Is the webapp connected to the database
* `git_revision` (`string`): First 7 digit of the SHA commit
* `git_tag` (`string`): Tag applied to the current commit (This is the application version)
* `server_name` (`string`): Ip address of the server

```
{
  "db_conn": "mysql://root:***@127.0.0.1/beerbattle",
  "db_conn_state": false,
  "git_revision": "18281ca",
  "git_tag": "v1.0.0",
  "server_name": "127.0.0.1"
}
```

###### /home
------------

Home page of the webapp (HTML content).

![Image of /home](./docs/webapp-home.png)

###### /catalog
---------------

List all beers present in the `beer` table from the database.

![Image of /catalog](./docs/webapp-catalog.png)

###### /top-beers
-----------------

List beers present in the `battle` table from the database, and display them ordered by people votes.

![Image of /top-beers](./docs/webapp-top-beers.png)

###### /battle
--------------

Run a battle versus two beers picked up randomly from the database. The user can vote for his favorite one. Once the use vote, an other battle starts!

![Image of /home](./docs/webapp-battle.png)

# Enjoy!
![Image of BeerBattle](app/static/img/bartender.png)

Made with ♥ for teaching people
