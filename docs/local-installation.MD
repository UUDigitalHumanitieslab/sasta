# Before you start

You need to install the following software:
- Docker. Make sure Docker has at least 4GB memory allocated, the default 2GB is insufficient.

## SASTADEV
SASTA requires SASTADEV to run. Clone it (from root directory):

#### SSH:
```console
git clone git@github.com:UUDigitalHumanitieslab/sastadev.git backend/sastadev
```
#### HTTPS:
```console
git clone https://github.com/UUDigitalHumanitieslab/sastadev.git backend/sastadev
```

## SASTADEV config
Create a `config.py` file in `backend/sastadev`, values from `default_config.py` work out-of-the-box:
```console
cp backend/sastadev/default_config.py backend/sastadev/config.py
```

# Running locally
To download, build, install, and run all containers:
```console
docker-compose up
```
If everything is executed correctly, the application is hosted at [localhost:80](localhost:80), or simply [localhost](localhost).

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
Visit the [django admin interface](localhost:80/admin)
Since the admin account does not follow the normal procedure of confirming email, do this manually:
- Email addresses
- Add
- User -> click magnifying glass and select your account
- E-mail address -> the address you entered in the previous step
- Verified & primary -> both checked
- Save

Your account is now ready for use. Regular user accounts can be made through the web-interface. Verification email is mocked in the backend console, copy verification link there.

## Add SASTADEV method definitions
- Analysis -> Assessment methods -> Add new
- Category: `TARSP`
- File: `backend/sastadev/methods/TARSP Index Current.xlsx`
- Save
- Repeat for STAP and ASTA




