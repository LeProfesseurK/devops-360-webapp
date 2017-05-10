# DevOps-360-Webapp
Webapp used in devops-360 project

## Running the application in prod

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

# Enjoy!
![Image of BeerBattle](app/static/img/bartender.png)

Made with ♥ for teaching people
