## API examples

### I want to list all the available `movies`

For checking the available movies perform a `GET` request 
at `/api/movies/v1/`

Response:
```json
[
  {
    "title": "Home Alone",
    "desc": "Movie description",
    "genre": "Comedy",
    "year": "1990",
    "likes": [],
    "dislikes": [],
    "id": 53
  }
]
```
**Note**: All users (authenticated/non-authenticated) can 
access this endpoint.

### I want to create a new `movie`
For creating a new movie perform a `POST` request at:
`api/movies/v1/new` 

```curl
curl -X 'POST' \
  'http://127.0.0.1:8000/api/movies/v1/new' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-CSRFToken: VBjul0SKyKZeNmrlESi7bYFQnjqHG2GeIYzU2DJFPdIQ79P1IrdQTyBlQsBP19HP' \
  -d '{
  "title": "New movie",
  "desc": "my description",
  "genre": "Action",
  "year": "2022"
}'

```
Response: 
```json
{
  "title": "New movie",
  "desc": "my description",
  "genre": "Action",
  "year": "2022",
  "likes": [],
  "dislikes": [],
  "id": 65
}
```
with status-code= `201`
**Note**: Only authenticated can access this endpoint.

### I want to update my existing `movie`
For updating an existing movie perform `PUT/PATCH` request at: `/api/movies/v1/{int}`

```curl
curl -X 'PATCH' \
  'http://127.0.0.1:8000/api/movies/v1/67' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-CSRFToken: xsUjESjy77oj0GuCJc5LnvyUHVyJw9J0kPaJlvatoA7VktSiNL0u55upa4JRRgKB' \
  -d '{
  "title": "New title",
  "desc": "New desc",
  "genre": "Action",
  "year": "2023"
}'
```

Response:
```json
{
  "title": "New title",
  "desc": "New desc",
  "genre": "Action",
  "year": "2023",
  "likes": [],
  "dislikes": [],
  "id": 66
}
```

Trying to update a movie from different user:
```curl
curl -X 'PUT' \
  'http://127.0.0.1:8000/api/movies/v1/53' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-CSRFToken: YzEirAJU5mkM8vZYAY7KYy3N6sVqSbhFLWUI8dAPmP3osinEEx2tG8ZizB6ydiig' \
  -d '{
  "title": "string",
  "desc": "string",
  "genre": "string",
  "year": "stri"
}'
```

Response:
```json
{
  "detail": "You do not have permission to perform this action."
}
```
and a `status-code=Forbidden`

**Note**: Only authenticated and author users can access this endpoint.


### I want to delete one `movie`
For deleting an existing movie perform `DELETE` request at `/api/movies/v1/{int}`

```curl
curl -X 'DELETE' \
  'http://127.0.0.1:8000/api/movies/v1/66' \
  -H 'accept: application/json' \
  -H 'X-CSRFToken: YzEirAJU5mkM8vZYAY7KYy3N6sVqSbhFLWUI8dAPmP3osinEEx2tG8ZizB6ydiig
  ```
Response:  `status-code=204`

Trying to delete a movie from different user  will give a response:
```json
{
  "detail": "You do not have permission to perform this action."
}
```
status-code:`Forbidden`

**Note**: Only authenticated and author users can access this endpoint.
