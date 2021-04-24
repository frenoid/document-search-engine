## DocumentDB to ES Loader

Script to load documents from MongoDB to Elasticsearch.

#### Setup

```
$ mkvirtualenv -p python3 document-search-engine
$ pip3 install -r requirements-dev.txt -r requirements.txt
```
#### Configuration

Create a `config.json` file with the following contents. A `config_sample.json` file is provided as an example. 

```
{
  "MONGO": {
      "HOST": "localhost",
      "USERNAME": "username",
      "PASSWORD": "password",
      "DB": "db",
      "COLLECTION": "collection"
  },
  "ES": {
    "HOST": "localhost",
    "USERNAME": "username",
    "PASSWORD": "password",
    "INDEX": "index"
  }
}
```

#### Tests

```
$ pytest
```

#### Code Formatting

```
$ black .
```