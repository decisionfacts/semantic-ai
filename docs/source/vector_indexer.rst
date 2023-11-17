Indexer
=======

.. code-block:: python

    from semantic_ai.indexer import ElasticsearchIndexer
    from semantic_ai.embeddings.huggingface import HFEmbeddings

    embeddings = await HFEmbeddings().embed()
    elastic_search = await ElasticsearchIndexer(
            url="http://localhost:9200",
            index_name="test_index",
            embedding=embeddings
    ).create()


**Index:**

Before index, we need to extract the content from the documents and constructed as json format. Here we can use the :ref:`df-extraction`. Once we extracted the data using df-extraction and converted as json format we can start to index.

.. code-block:: python

    await elastic_search.index("/home/test/sample.json")


If we lots of files, stored into directory and we can use directory path in `index`

.. code-block:: python

    await elastic_search.index("/home/test/")

You can check your elasticsearch vector database its indexing or not.