==============
Auth connector
==============

The goal of this project is to have a reusable component that allow us to authenticate against a
microservice for user management. This will take the JWT token that was send in the request
Authorization header and it will use it to retrieve the user information and store it in the
local user database.


Quick start
-----------

1. Install the project by doing ``pip install authconnector``
2. Install the usual django migrations.
3. Add the app to the django INSTALLED_APPS:
    'remoteauth'

3. Add the next configuration on the django settings:

INMOBILIO_AUTHENTICATION_SERVICE = {
'JWT_VALIDATION_URL': 'http://localhost:9000/auth/user'
}

4. Done :D

You can now retrieve the user within the request to your API endpoints.
