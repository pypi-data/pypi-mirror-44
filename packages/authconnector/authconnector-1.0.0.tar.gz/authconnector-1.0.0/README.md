# Authconnector
## What is this about
The goal of this project is to have a reusable component that allow us to authenticate against a microservice for user management. This will take the JWT token that was send in the request Authorization header and it will use it to retrieve the user information and store it in the local user database.


## How to use it
* Do `pip install authconnector` to install the project on your django microservice.
* Install the usual django migrations.
* Done :D

You can now retrieve the user within the request to your API endpoints. 
