# FULL STACK TRIVIA

Welcome to the Capstone Casting Agency API. This is a backend api designed to facilitate casting assistants, casting directors and executive directors as they create, read, update and delete movies and actors. 

## Getting Started
**Note:** This app requires python3, pip, virualenv and psql. Please download these dependencies before proceeding.

<!-- 1. Download the zip files provided with this submission and cd into the starter folder.
2. Create a virutal environement
    ```bash
    python3 -m venv env
    ```
    ```bash
    source env/bin/activate
    ```
3. Install all dependecies with:

    ```bash
    pip install -r requirements.txt
    ```
4. Create a new trivia database with the following commands.

    ```
    psql create database trivia
    ```
    ```
    psql trivia < trivia.psql
    ```

5. Install Node package manager for the front-end.

    ```bash
    npm install
    ```

6. Start the backend.

    ```bash
    export FLASK_APP=flaskr
    flask run
    ```

7. Start the front end.
    ```bash
    npm start
    ```  -->
## Testing

This api is equipped with a fully-functional Postman testing suite for all API endpoints. Just run the `Casting Agency Tests.postman_collection.json` file in Postman. 

**Note:** You will need to set up the JSON Web Tokens (JWT's) for each role. Please see Auth0 login information provided with submission to obtain the JWTs. 


## Error Handling

Errors are returned as JSON objects with the following format:

```
{
    "success": False, 
    "error": 404,
    "message": "Not Found"
}
```

The API will return 3 error types when requests fail:
- 404: Not Found
- 422: Unprocessable
- 500: Server Error

If authentication fails or the request in malformed, then the server will return an AuthError with a description of the problem in the `"message"` key.

# API Reference

## Authentication
- Visit [Login Page] and follow login flow to authenticate.
**Note:** If the reviewer needs to create new users, they will need to use the Auth0 credentials provided with the submission to assign roles to the new users.

[Login Page]:
(https://testytesteryson.us.auth0.com/authorize?audience=CastingAgency&response_type=token&client_id=6shGIWYciWgdeSLi9aC4K1XfH0KuSzKb&redirect_uri=http://localhost:5000/login)

## Actors

### GET/actors
- General
    - Returns a list of actors in database and success value.
    - Must be authenticated with `get:actors` permission. 
- Example `curl http://127.0.0.1:5000/actors`
```
{
    "actors": [
        {
            "age": 54,
            "gender": "Male",
            "id": 3,
            "name": "Tom Cruise"
        },
        {
            "age": 62,
            "gender": "Male",
            "id": 4,
            "name": "Tom Hanks"
        }
    ],
    "success": true
}
```

### POST/actors
- General
    - Adds a new actor to the database.
    - Include a name, age, and gender. 
    - Returns a success value and the formatted actor json
    - Must be authenticated with `post:actors` permission. 
- Example: 
```
curl -X POST -H "Content-Type: application/json" -d '{"name" : "Olivia Munn", "age" : 33, "gender" : "Female"}' http://127.0.0.1:5000/actors
```

```
{
    "actors": {
        "age": 33,
        "gender": "Female",
        "id": 5,
        "name": "Olivia Munn"
    },
    "success": true
}
```

### PATCH/actors/<id>
- General
    - Updates an actor in the database.
    - Include an actor id in the uri. 
    - Returns a success value and the formatted actor json
    - Must be authenticated with `patch:actors` permission. 
- Example: 
```
curl -X PATCH -H "Content-Type: application/json" -d '{"name" : "Olivia Munn", "age" : 39, "gender" : "Female"}' http://127.0.0.1:5000/actors/5
```

```
{
    "actors": {
        "age": 39,
        "gender": "Female",
        "id": 5,
        "name": "Olivia Munn"
    },
    "success": true
}
```

### DELETE/actors/<id>
- General
    - Deletes an actor in the database.
    - Include an actor id in the uri. 
    - Returns a success value and the deleted actor id.
    - Must be authenticated with `delete:actors` permission. 
- Example `curl-X DELETE http://127.0.0.1:5000/actors/5`
```
{
    "success": true,
    "actors": 5
}
```

## Movies

### GET/movies
- General
    - Returns a list of movies in database and success value.
    - Must be authenticated with `get:movies` permission. 
- Example `curl http://127.0.0.1:5000/movies`
```
{
    "movies": [
        {
            "id": 1,
            "release_date": "Tue, 08 May 2007 12:35:29 GMT",
            "title": "Ocean's Eleven"
        },
        {
            "id": 2,
            "release_date": "Tue, 08 May 2007 12:35:29 GMT",
            "title": "Titanic"
        }
    ],
    "success": true
}
```

### POST/movies
- General
    - Adds a new movie to the database.
    - Include a title and release date.
    **Note:** release_date must be an string appropriately formated for SQL Datetime type.
    - Returns a success value and the formatted movies json
    - Must be authenticated with `post:movies` permission. 
- Example: 
```
curl -X POST -H "Content-Type: application/json" -d '{"title" : "Bourne Identity", "release_date" : "2007-05-08 12:35:29.123"}' http://127.0.0.1:5000/movies
```

```
{
    "movie": {
        "id": 3,
        "release_date": "Tue, 08 May 2007 12:35:29 GMT",
        "title": "Bourne Identity"
    },
    "success": true
}
```

### PATCH/movies/<id>
- General
    - Updates a movie in the database.
    - Include a movie id in the uri. 
    - Returns a success value and the formatted movies json
    - Must be authenticated with `patch:movies` permission. 
- Example: 
```
curl -X PATCH -H "Content-Type: application/json" -d '{"title" : "Bourne Identity", "release_date" : "2007-06-08 12:35:29.123"}' http://127.0.0.1:5000/movies/5
```

```
{
    "movie": {
        "id": 3,
        "release_date": "Fri, 08 Jun 2007 12:35:29 GMT",
        "title": "Bourne Identity"
    },
    "success": true
}
```

### DELETE/movies/<id>
- General
    - Deletes a movie in the database.
    - Include a movie id in the uri. 
    - Returns a success value and the deleted movies id.
    - Must be authenticated with `delete:movies` permission. 
- Example `curl-X DELETE http://127.0.0.1:5000/movies/5`
```
{
    "success": true,
    "movies": 5
}
```
