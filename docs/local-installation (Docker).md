# Before you start

Using to run the containerized version of SASTA bypasses the need to install system dependencies.

You need to install the following software:

-   [Docker](https://docs.docker.com/get-docker/). Make sure Docker has at least 4GB memory allocated.

# Running locally

To download, build, install, and run all containers:

```console
docker-compose up
```

If everything is executed correctly, the application can be opened at [localhost:80](localhost:80).

# First-use setup

## Create an admin account

Connect to the backend container:

```console
docker-compose run backend bash
```

Create a superuser using Django command.
Choose a username, email and password. Email does not have to be real (but cannot be blank):

```console
python manage.py createsuperuser
```

## Add SASTADEV method definitions

1. Go to localhost:80/admin
2. Log in with your admin account
3. `analysis` -> `Assessment methods` -> `Add new`
4. Choose the following settings:
    - Category: `TARSP`
    - File: `<project directory>/backend/sastadev/methods/Tarsp index current.xlsx` (xlsx spreadsheet)
5. Repeat step 3 & 4 for STAP and ASTA
