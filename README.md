# pokemonapi

Project created with django and djangorestframework.

This project contains a command which, by executing it, inserts the pokemon's that are part of the evolution chain into the api.
This project exposes a web service that allows to search by name for a pokemon, this return the information of the pokemon, the base stats and the evolutions, in the evolutions it returns both the pre-evolutions and the evolutions.

![pokemonapi](../master/screenshot.PNG)

## Pre requirements
1. Python 3.X
2. Django==2.2.7
3. djangorestframework==3.10.3
 
## Installation
1. Clone the repository
2. Execute manage.py migrate

## Execute command
1. Execute manage.py getevolutionchain {evolution_chain_id}

## Run web service
1. Execute manage.py runserver
2. Enter from the browser to http://127.0.0.1:8000/api/v1/pokemons/{name}/
