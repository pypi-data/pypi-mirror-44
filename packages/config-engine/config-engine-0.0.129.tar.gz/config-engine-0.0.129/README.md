## Config Engine App
Config Engine is the backend system to Config Manager. 

### Tech Stack

- Django 2
- Postgresql 
- Python3
- RabbitMQ
- Celery


### Download

- Postgresql App
- brew install python3
- brew install rabbitmq

### Config Settings

    export DJANGO_SETTINGS_MODULE='config_engine.settings'


### Set up your environment

    tox -r

### Local Settings

- Create your local.yaml file. Copy the database settings from default.
- To allow for default client for swagger docs add below to local.yaml
- Create Queues and Exchange and Bind queue to exchange for read/write queues
        
            DEFAULT_TENANT': 'Internal' 

## To run: Start the Server

    python manage.py runserver
    
 
## To run rabbit consumer

    python manage.py message_listener
    
