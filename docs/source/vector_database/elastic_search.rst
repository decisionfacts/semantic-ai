.. _elastic-search:

Elastic Search
==============

.. image:: https://github.com/decisionfacts/semantic-ai/blob/master/docs/source/_static/images/logo/elastic-logo-920x920-sue-v02.png?raw=true
    :alt: Logo
   :align: left
   :width: 110px
   :target: https://www.elastic.co/elasticsearch


Elasticsearch is the distributed search and analytics engine. Elasticsearch provides real-time search and analytics for all types of data. Whether structured or unstructured text, numerical data.

**Setup Elasticsearch:**

Running a elasticsearch using docker.

.. code-block:: shell

        docker run -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" -e "xpack.security.http.ssl.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:8.9.0


Once the elasticsearch instance is running, you can connect to it using the Elasticsearch URL and index name along with the embedding object to the constructor.

To Elasticsearch object creation

.. code-block:: python

    from semantic_ai.indexer import ElasticsearchIndexer
    from semantic_ai.embeddings.huggingface import HFEmbeddings

    embeddings = await HFEmbeddings().embed()
    elastic_search = await ElasticsearchIndexer(
            url="http://localhost:9200",
            index_name="test_index",
            embedding=embeddings
    ).create()

**Authentication:**

For production, we recommend to enable the security. To connect with login credentials. We can us the parameters `api_key` or `es_user` and `password`

.. code-block:: python

    elastic_search = await ElasticsearchIndexer(
            url="http://localhost:9200",
            index_name="test_index",
            embedding=embeddings,
            es_user="elastic",
            es_password="password"
    ).create()

**Index:**

Before index, we need to extract the content from the documents and constructed as json format. Here we can use the :ref:`df-extraction`. Once we extracted the data using df-extraction and converted as json format we can start to index.

.. code-block:: python

    await elastic_search.index("/home/test/sample.json")


If we lots of files, stored into directory and we can use directory path in `index`

.. code-block:: python

    await elastic_search.index("/home/test/")


You can check your elasticsearch vector database its indexing or not.

**Search Query:**

.. code-block:: python

    query = "<your query>"
    result = await elastic_search.asimilarity_search(query)