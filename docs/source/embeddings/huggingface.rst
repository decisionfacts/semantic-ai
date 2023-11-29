Hugging Face 🤗
===============

HuggingFace sentence_transformers embedding models.

To use, you should have the ``sentence_transformers`` python package installed.

.. code-block:: python

    from semantic_ai.embeddings.huggingface import HFEmbeddings

    embedding = HFEmbeddings() # By default model name 'sentence-transformers/all-mpnet-base-v2'
    embeddings = await embedding.embed() # Huggingface embedding object creation

We can change the model name with ``model_name`` params

.. code-block:: python

    embedding = HFEmbeddings(model_name="<model_name>")

embed_documents
---------------

.. code-block:: python

    embedding_doc = await embeddings.aembed_documents(
                [
                    "Hi there!",
                    "Oh, hello!",
                    "What's your name?",
                    "My friends call me World",
                    "Hello World!"
                ]
            )
    len(embedding_doc), len(embedding_doc[0])

.. code-block:: python

    (5, 768)

embed_query
-----------

.. code-block:: python

    embedded_query = await embeddings.aembed_query("What is an AI")
    embedded_query[:5]

.. code-block:: python

    [-0.006212963722646236,
     0.02152606099843979,
     -0.028265055269002914,
     -0.02149374410510063,
     -0.03208868205547333]