# URL Shortener (Cloudflare Exercise)

# Design and tradeoffs
The URL shortner uses SHA256 hashing to create a short URL, which it then
persists to a local MySQL database. It also uses an in-memory cache to ensure
latency for recently used items is low.

The shortener also stores statistics regarding accesses to short URLs. In order
to avoid high data use, the shortener stores aggregate per-hour and aggregate
all-time access statistics, and uses the per-hour statistics to compute
last-day and last-week statistics. This allows many accesses to the same URL
at the same time to not grow the DB in an unbounded fashion. The trade-off
is a drop in accuracy of statistics, since we have a one-hour granularity
in our underlying data.

In order to persist statistics while avoiding DB writes on the hot path,
we use a background thread that reads from a queue of recent accesses and
updates the database. If multiple instances of the shortener are run,
it's possible that the thread could run into locking issues. Solutions to this
could include moving statistics to a datastore with atomic increments, like
Redis.

# API

The API of the shortener is as follows:

## /create  (POST)
Create a URL shortname. Take as input the full URL as a form-encoded POST parameter named 'url'.
Returns JSON with one attribute, "url", containing the shortened URL.

### Usage Example

```
$ curl -d 'url=http://noam.horse/resume.html' http://localhost:5000/create
{"url":"http://localhost:5000/go/7e0ca0cb43"}
```

## /go/<shortname>  (GET)
Use a short URL. These URLs are returned from `/create` and can be used to
redirect a user to the full URL.

### Usage Example

```
$ curl -v http://localhost:5000/go/7e0ca0cb43
 ...

>
* HTTP 1.0, assume close after body
< HTTP/1.0 302 FOUND
< Content-Type: text/html; charset=utf-8
< Content-Length: 265
< Location: http://noam.horse/resume.html
< Server: Werkzeug/0.16.0 Python/3.7.4
< Date: Fri, 25 Oct 2019 22:05:08 GMT
<
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>Redirecting...</title>
<h1>Redirecting...</h1>
* Closing connection 0
<p>You should be redirected automatically to target URL: <a href="http://noam.horse/resume.html">http://noam.horse/resume.html</a>.
```

## /stat/<shortname>  (GET)
Statistics about a short URL. Will return JSON with three numeric attributes:
* `all_time`: Accesses for all time
* `last_day`: Accesses (approx) for last 24 hour
* `last_week`: Accesses (approx) for last 7 days

### Usage Example

```
$ curl http://localhost:5000/stat/7e0ca0cb43
{"all_time":20,"last_day":20,"last_week":20}
```


# Requirements
* Python 3
* Needed Python modules (can be installed with pip):
..* sqlalchemy
..* sqlalchemy-utils (necessary only for running bootstrap_db.py)
..* mysql
..* flask
..* cachetools
* An active local mysql instance with a passwordless root user

# Running

## Initial setup
Once you have started a local mysql server with a passwordless root user,
you can run `bootstrap_db.py` to drop and recreate the dev and test databases,
as well as create all tables.

## Running tests

To run the tests, run the `run_tests.py` script.

## Running the app

To run the app, run the `run_app.py` script.
