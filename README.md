# URL Shortener

## Getting started 

### Steps:
1. Clone/pull/download this repository
2. Build docker compose by run the following command: `docker-compose build`
3. Run docker container: `docker-compose up`
4. Create superuser (needed only first time): `docker-compose run web python manage.py createsuperuser`. In terminal prompt enter email, name and password for the admin user.