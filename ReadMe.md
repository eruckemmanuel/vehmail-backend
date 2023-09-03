# Dockerized Django application starter

Starter configurations for a django project, deployed with docker compose

## Services
This dockerized setup adds support for:
- Redis
- Celery


## Setup

Copy the contents of your django project folder into the app directory

```shell
cp -R vehamil-backend/* app/
```

### Environment variables
Copy from the sample.env file and update to match your app settings

```shell
cp sample.env .env
```
Add other environment variables used by your application to the `.env` file
