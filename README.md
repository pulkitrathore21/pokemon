# CRUD operation for pokemon.

This project implements a simple CRUD operation for managing POKEMON data which I am taking from an json file and trying to upload the database.
it provides APIS for creating,reading,updating or deleting pokemon records.

Url for accessing the endpoints(http://127.0.0.1.5000/pokemon/<api_name>)

## GUIDENCE:

- Run the fate.py file to launch the application. 
- App/config.py contains the fundamental configuration.
- In app/models.py, there is a table and the Marshallow schema.
- In app/views.py are APIs.

## Installation Procedures
--"python3 -m venv venv" run the command to create a new venv "source venv/bin/activate" to activate virtual environment "export FLASK_APP=start.py" "flask run" use the command above to launch the application; it will run in debug: mode OFF
## Features
--Run the fate.py file to launch the application.
--App/config.py contains the fundamental configuration.
--In app/models.py, there is a table and the Marshallow schema.
--In app/views.py are APIs.
--build a model, then add the data from the link.
--Peruse the Pokemon records
--Revisit previous Pokemon records

## API Endpoints for deletion

- GET:/ a list of all Pokemon records by typing GET /pokemon. search by  Name ,legendary,generation.
- order by properties also added .
=POST: /pokemon/new: post the information into database by passing in body.
-PATCH: /pokemn/up-date/<pokemon_name> we can partial update by providing this apis.
DELETE: /pokemon/<string:name> we can delete by providing the name of pokemon .







