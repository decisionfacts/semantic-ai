OpenAI
======

.. image:: https://github.com/decisionfacts/semantic-ai/blob/master/docs/source/_static/images/logo/openai-icon-2021x2048-4rpe5x7n.png?raw=true
    :alt: Logo
   :align: left
   :width: 120px
   :target: https://openai.com/

OpenAI offers a spectrum of models with different levels of power suitable for different tasks.



**Setup OpenAI api key:**

.. code-block:: python

    import os
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


.. code-block:: python

    from semantic_ai.llm import Openai
    openai_llm = await Openai().llm_model()

If you manually want to specify your OpenAI API key and/or organization ID, you can use the following:

.. code-block:: python

    openai_llm = await Openai(openai_api_key="api_key").llm_model()

**Vector Database:**

Now we are going to use :ref:`elastic-search` vector database.

.. code-block:: python

    from semantic_ai.indexer import ElasticsearchIndexer
    from semantic_ai.embeddings.huggingface import HFEmbeddings

    embeddings = await HFEmbeddings().embed()
    elastic_search = await ElasticsearchIndexer(
            url="http://localhost:9200",
            index_name="test_index",
            embedding=embeddings
    ).create()

**Search:**

.. code-block:: python

    from semantic_ai.search.semantic_search import Search
    search_obj = Search(
                model=openai_llm,
                load_vector_db=elastic_search
    )
    query = "What is an AI"
    search = await search_obj.generate(query)

We can change the top_k value and prompt using `top_k` and 'prompt' params respectively

.. code-block:: python

    search_obj = Search(
                model=openai_llm,
                load_vector_db=elastic_search,
                top_k=5,
                prompt=prompt
    )
    query = "What is an AI"
    search = await search_obj.generate(query)