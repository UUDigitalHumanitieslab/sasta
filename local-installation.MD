## Before you start

You need to install the following software:
- Docker. Make sure Docker has at least 4GB memory allocated, the default 2GB is insufficient.

SASTA requires SASTADEV to run. Clone it (from root directory).
SSH:
```console
$ git clone git@github.com:UUDigitalHumanitieslab/sastadev.git backend/sastadev
```
HTTPS:
```console
$  git clone https://github.com/UUDigitalHumanitieslab/sastadev.git backend/sastadev
```

Create a `config.py` file in `backend/sastadev`:


## Running locally
To download, build, install, and run all containers:
```console
$ docker-compose up
```
If everything is executed correctly, the application is hosted at `localhost:80` (or simply `localhost`)

## First-use setup
### Create an admin account
Connect to the backend container:
```console
$ docker-compose run backend bash
```
Create a superuser using Django command.
Choose a username, email and password. Email does not have to be real (but cannot be blank):
```console
$ python manage.py createsuperuser
```
Visit localhost:80/admin

### Add SASTADEV method definitions
Under analysis -> Assessment methods -> Add new

Category -> Tarsp -> choose file
backend -> sastadev -> methods -> Tarsp index current -> Save
Repeat for STAP and ASTA




