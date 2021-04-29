## DocumentDB to ES Loader

Script to load documents from MongoDB to Elasticsearch.

#### Setup

```
$ mkvirtualenv -p python3 es_loader
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
    "INDEX_PREFIX": "index-prefix-",
    "PRODUCTION_ALIAS": "production-alias"
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