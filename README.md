## Sleepwalker - Backend

Part of [sleepwalker](https://github.com/zNitche/sleepwalker) project. 
Django powered backend for sleep monitoring and sleepwalking detection + prevention system.

---

### Technologies
- Django 4.2
- django rest framework 3.14
- gunicorn
- celery
- swagger (drf-spectacular)

### Features
- Token and ApiKey based authentication.
- Heart beat monitoring and sleepwalking detection.
- Configurable detection parameters (user settings).

### Setup
#### Dev
1. Create `.env` file
```
cp .env.template .env
```
2. Run dev docker services.
```
sudo docker compose -f docker-compose-dev.yml up
```
3. Run celery workers
```
sh scripts/celery_entrypoint.sh
```
#### Prod
1. Create `.env` file
```
cp .env.template .env
```
2. Change config values
   - `DEBUG` - set to 0
   - `DB_PATH` - database path
   - `LOGS_PATH` - logs path
   - `ALLOWED_HOSTS` - comma separated host names 
   - `POSTGRES_USER` - database user
   - `POSTGRES_PASSWORD` - password for database
3. Run docker services.
```
sudo docker compose up -d
```

#### Accounts Management
1. Bash into web app container.
```
sudo docker container exec -it sleepwalker_backend bash
```
2. Run accounts manager cli `python3 manage.py create_user`.

#### API Documentation
swagger documentation can be found (only `DEBUG` mode)
```
/api/docs
```

#### Tests
```
python3 manage.py test
```