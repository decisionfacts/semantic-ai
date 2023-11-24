LLAMA 2
=======

.. image:: https://github.com/decisionfacts/semantic-ai/blob/DFPS-172-Semantic-ai-LLM-IBM/docs/source/_static/images/logo/Untitled_design_(1).png?raw=true
    :alt: Logo
   :align: left
   :width: 180px
   :height: 80px
   :target: https://ai.meta.com/llama/


Llama 2 is a open-access large language models released by Meta. The Llama 2 ranging in scale from 7B to 70B parameters (7B, 13B, 70B). We can check the model details in `Llama 2 <https://ai.meta.com/llama/>`_

**Download the model:**

- Llama 2 model download `here <https://ai.meta.com/resources/models-and-libraries/llama-downloads/>`_

**Import Semantic AI:**

.. code-block:: python

    from semantic_ai.llm import Llama

    llama_llm = await Llama(model_name_or_path="model_name_or_path").llm_model()

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
                model=llama_llm,
                load_vector_db=elastic_search
    )
    query = "What is an AI"
    search = await search_obj.generate(query)

We can change the top_k value and prompt using `top_k` and 'prompt' params respectively

.. code-block:: python

    search_obj = Search(
                model=llama_llm,
                load_vector_db=elastic_search,
                top_k=5,
                prompt=prompt
    )
    query = "What is an AI"
    search = await search_obj.generate(query)