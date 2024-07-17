.. _opensearch:

OpenSearch
===========

.. image:: https://github.com/decisionfacts/semantic-ai/blob/master/docs/source/_static/images/logo/opensearch_logo_img.png?raw=true
    :alt: Logo
   :align: left
   :width: 110px
   :target: https://opensearch.org/


OpenSearch offers a flexible and scalable open-source approach for developing solutions tailored to data-intensive applications. Utilize its built-in performance, developer-friendly tools, and robust integrations for machine learning, data processing, and beyond to explore, enhance, and visualize your data effectively.

**Setup Opensearch:**



.. code-block:: shell

        docker run -d -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" -e "OPENSEARCH_INITIAL_ADMIN_PASSWORD=<custom-admin-password>" opensearchproject/opensearch:latest


Once the opensearch instance is running, you can connect to it using the Opensearch URL and index name along with the embedding object to the constructor.

To Opensearch object creation

.. code-block:: python

    from semantic_ai.indexer import OpenSearchIndexer
      from semantic_ai.embeddings.huggingface import HFEmbeddings

    embeddings = await HFEmbeddings().embed()
    open_search = await OpensearchIndexer(
            url="http://localhost:9200",
            index_name="test_index",
            embedding=embeddings
    ).create()


**Authentication:**

For production, we recommend to enable the security. To connect with login credentials. We can us the parameters `user` and `password`

.. code-block:: python

     open_search = await OpensearchIndexer(
            url="http://localhost:9200",
            index_name="test_index",
            embedding=embeddings,
            user="elastic",
            password="password"
     ).create()


**Index:**

Before index, we need to extract the content from the documents and constructed as json format. Here we can use the :ref:`df-extraction`. Once we extracted the data using df-extraction and converted as json format we can start to index.

.. code-block:: python

    await open_search.index("/home/test/sample.json")


If we lots of files, stored into directory and we can use directory path in `index`

.. code-block:: python

    await open_search.index("/home/test/")


You can check your opensearch vector database its indexing or not.

**Search Query:**

.. code-block:: python

    query = "<your query>"
    result = await open_search.asimilarity_search(query)