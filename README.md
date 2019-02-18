# flask_rest_api
This code creates a small REST API python application that listens on port 8080
The application has only 2 endpoints.

The first endpoint accepts only POST requests which have a json payload.
 
The JSON payload will be:
 
    [
    {
        "name": "Abraham Lincoln",
        "user_id": "1",
        "date": "1989-02-12T13:12:00.451765",
        "hw": "Apple I",
        "md5checksum": "8670d7dd125266374cb14660ff587413"
    },
    {
        "name": "John Kennedy",
        "user_id": "2",
        "date": "1961-01-26T14:12:00.451765",
        "hw": "Atari ST",
        "md5checksum": "2cdaec775db46ccbf10403bf1bcb2e16"
    }
    ]

The endpoint stores the data in a sqlite3 database.

Before storing the data it makes sure that the checksum for each
JSON object (just fields: user_id, name, date and hw) is correct and matches the original checksum in the JSON payload.
If checksum matches the original checksum, JSON object will be written into database. If not, it will be ignored.

In the example above you can see 2 JSON objects with CORRECT md5 checksum (I written these checksums instead of those generated in task,
because they are incorrect).
  
The second endpoint accepts only GET requests with an user_id parameter. The endpoint returns  all records for given user_id.

All requirements are in requirements.txt. To install all libraries run in command line:

```pip install -r requirements.txt```

You can run code in terminal:

```python app.py```
