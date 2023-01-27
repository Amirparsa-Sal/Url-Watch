# URL Watch

This repository contains a django app to monitor URLs. Different users can sign up and enter their URLs to be checked in predefined intervals. Users can set a threshold and if the failure count crosses that threshold the app will send a warning for user containing the reason of failure. Users also can reset their URLs to clear warnings and failure times.

## How to use

First you should create a `.env` file inside `url_watch` folder. The file contains the following env variables:

```
SECRET_KEY=YourDjangoSecretKey

MONITORING_INTERVAL=MonitoringIntervalSeconds

CELERY_BROKER_URL=redis://redis:6379
CELERY_RESULT_BACKEND=redis://redis:6379

POSTGRES_USER=YourPostgresUser
POSTGRES_PASSWORD=YourPostgresPassword
POSTGRES_DB=YourPostgresDB
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

You can change `redis` and `db` host in `docker-compose.yaml` file.

The monitoring interval is the time between each URL checks. You can enter it in seconds in `.env` file.

FInally, you can simply run:

```
docker-compose up -d --build
```

The app will be available on `localhost:8080`.

## Endpoints

### - Registration & Authentication

#### POST api/auth/register/

Registers the user.

Example request body:

```json
{
    "email": "amirparsa@gmail.com",
    "first_name": "amirparsa",
    "last_name": "sal",
    "password": "amirparsa"
}
```

It returns `201 CREATED` if the registration is successful else `400 BAD REQUEST`.

#### POST api/auth/login/

Users can log in using this endpoint. It gives the users their JWT access and refresh token. Clients must put the access token as the bearer token.

Example request body:

```json
{
    "email": "amirparsa@gmail.com",
    "password": "amirparsa"
}
```

Example response body:

```json
{
    "refresh": "ref_token",
    "access": "acc_token"
}
```

Returns `401 Unauthorized` if the credentials are incorrect.

#### POST api/auth/refresh/

Refreshes the user access token given the refresh token. The tokens timeout can be set using `.env` file which be discussed later.

Example request body:

```json
{
    "refresh": "ref_token"
}
```

Example response body:

```json
{
    "access": "acc_token"
}
```

Returns `401 Unauthorized` if the refresh token is incorrect.

### - URLs

#### GET api/url/

`Auth required` Gives a list of URLs which belong to the user.

No request body is required.

Example response body:

```json
[
    {
        "id": 1,
        "url": "https://www.google.com",
        "threshold": 20
    },
    {
        "id": 2,
        "url": "https://www.github.com",
        "threshold": 10
    }
]
```

Returns `401 Unauthorized` if user is not authorized.

#### PUT api/url/

`Auth required` Creates a URL for user.

Example request body:

```json
{
    "url": "https://www.google.com",
    "threshold": 20
}
```

It will return `201 CREATED` if the registration was successful otherwise `400 BAD REQUEST`.

Users can create at most 20 URLs.

#### GET api/url/{int:pk}

`Auth required` Returns the details of a url.

No request body is required.

Example response body:

```json
{
    "id": 1,
    "created_at": "2023-01-27T15:06:25.422836+03:30",
    "updated_at": "2023-01-27T15:06:25.422845+03:30",
    "failed_times": 0,
    "url": "https://www.google.com",
    "threshold": 20
}
```

Returns `404 NOT FOUND` if the URL does not exist.

Returns `401 Unauthorized` if user is not authorized.

#### DELETE api/url/{int:pk}

`Auth required` Deletes the URL.

No request body is required.

It will return `204 NO CONTENT` if the deletion was successful otherwise `404 NOT FOUND`. 

Returns `401 Unauthorized` if user is not authorized.

#### POST api/url/{int:pk}/reset

`Auth required` Resets the url failure times and warnings.

No request body is required.

It will return `200 OK` if the deletion was successful otherwise `404 NOT FOUND`.

Returns `401 Unauthorized` if user is not authorized.

### - Warnings

#### GET api/warning/

`Auth required` Returns the list of warnings for user.

No request body is required.

Example response body:

```json
[
    {
        "id": 1,
        "url_id": 7,
        "url": "https://www.sdbhjsds.com",
        "created_at": "2023-01-27T15:13:39.821905+03:30",
        "result_code": -1
    },
    {
        "id": 2,
        "url_id": 7,
        "url": "https://www.sdbhjsds.com",
        "created_at": "2023-01-27T15:13:49.808740+03:30",
        "result_code": -1
    }
]
```

Returns `401 Unauthorized` if user is not authorized.








