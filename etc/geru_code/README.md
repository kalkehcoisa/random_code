# geru


```
https://gist.github.com/flaviogeru/53a739e35e1523a39bf3e7a95d177918
https://1c22eh3aj8.execute-api.us-east-1.amazonaws.com/challenge/quotes
http://localhost:6543/
```


## 1) Create a lib that will act as a wrapper around the API described above

Create a python package within you project to make queries to the API containing the following methods:

    get_quotes() -> queries the API and returns a python dictionary containing all quotes available
    get_quote(quote_number) -> queries the API and returns a python dictionary containing the corresponding quote


## 2) Create a Pyramid [1] application that will use the API

The application must have 4 routes:

    / - Presents a simple HTML page containing a title that reads "Web Challenge 1.0".
    /quotes - Presents a page containing all quotes returned by the API (each contained in its own bullet point).
    /quotes/<quote_number> - Presents a page containing the <quote_number> quote returned by the API.
    /quotes/random - Present a page containing a random quote. Both the <quote_number> and the quote selected randomly ought to be displayed.


## 3) Create and register the session

Using the framework's session mechanism, create a unique identifier for all application requests that came from the same browser.


## 4) Store requests in a database

Using SQLAlchemy + sqlite create a model (or models) to store:

    The session identifier
    The date, time and page requested within a given session for every request made.


## 5) Create RESTful endpoints to query the sessions/requests stored in the database

