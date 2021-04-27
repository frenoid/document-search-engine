from elasticsearch import Elasticsearch

config = {
    "ES": {
        "HOST": "localhost",
        "USERNAME": "username",
        "PASSWORD": "password",
        "PRODUCTION_ALIAS": "production-alias",
    }
}


def get_es_client(config: dict) -> Elasticsearch:
    host = config["ES"]["HOST"]
    username = config["ES"]["USERNAME"]
    password = config["ES"]["PASSWORD"]
    elastic_client = Elasticsearch(
        host,
        http_auth=(username, password),
        scheme="https",
        http_compress=True,
        timeout=60,
        max_retries=100,
        retry_on_timeout=True,
    )
    try:
        # test connection to elasticsearch client
        elastic_client.nodes.info()
        print("Success! Connected to Elasticsearch.")
        return elastic_client
    except ConnectionError:
        print("Error! Failed to connect to Elasticsearch.")


def search_documents(search_string: str) -> list:
    client = get_es_client(config)

    index = config["ES"]["PRODUCTION_ALIAS"]
    body = {
        "query": {
            "query_string": {
                "query": search_string,
                "fields": ["doc.content", "doc.topic"],
            }
        }
    }

    try:
        response = client.search(index=index, body=body, size=10)
        print("Success! Got search results.")
    except:
        print("Error!")

    topic_list = []
    hits = response["hits"]["hits"]
    
    for hit in hits:
        topic = hit["_source"]["doc"]["topic"]
        topic_list.append(topic)
    
    return topic_list


if __name__ == "__main__":
    search_string = "Hong Kong"
    results = search_documents(search_string)
    print(results)