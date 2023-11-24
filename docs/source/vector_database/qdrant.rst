Qdrant
======

.. image:: https://github.com/decisionfacts/semantic-ai/blob/DFPS-172-Semantic-ai-LLM-IBM/docs/source/_static/images/logo/logo_with_text.png?raw=true
    :alt: Logo
   :align: center
   :width: 110px
   :target: https://qdrant.tech/


Qdrant is a vector similarity search engine that provides a production-ready service with a convenient API to store, search, and manage points (i.e. vectors) with an additional payload.

**Setup Qdrant:**

First we download the latest Qdrant image from docker hub

.. code-block:: shell

    docker pull qdrant/qdrant

Then, run the service

.. code-block:: shell

    docker run -p 6333:6333 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant

Under the default configuration all data will be stored in the ./qdrant_storage directory. This will also be the only directory that both the Container and the host machine can both see.

Qdrant API : `localhost:6333 <http://localhost:6333>`_
Qdrant Web Dashboard: `Dashboard <http://localhost:6333/dashboard>`_

Once the Qdrant instance is running, you can connect to it using the Qdrant URL and index name along with the embedding object to the constructor.

To Qdrant object creation

.. code-block:: python

    from semantic_ai.indexer import QdrantIndexer
    from semantic_ai.embeddings.huggingface import HFEmbeddings

    embeddings = await HFEmbeddings().embed()
    qdrant = await QdrantIndexer(
            url="http://localhost:6333",
            index_name="test_index",
            embedding=embeddings
    ).create()

**Authentication:**

For production, we recommend to enable the security. To connect with login credentials. We can us the parameters `api_key`.

.. code-block:: python

    qdrant = await QdrantIndexer(
            url="http://localhost:9200",
            index_name="test_index",
            embedding=embeddings,
            api_key="<api_key>"
    ).create()

**Index:**

Before index, we need to extract the content from the documents and constructed as json format. Here we can use the :ref:`df-extraction`. Once we extracted the data using df-extraction and converted as json format we can start to index.

.. code-block:: python

    await qdrant.index("/home/test/sample.json")


If we lots of files, stored into directory and we can use directory path in `index`

.. code-block:: python

    await qdrant.index("/home/test/")


You can check your elasticsearch vector database its indexing or not.

**Search Query:**

.. code-block:: python

    query = ""
    result = await qdrant.asimilarity_search(query)