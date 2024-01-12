Natural Language Processing
======

.. figure:: https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSuqJW1cosMDRjkXvBnJ8eWZp0q0xT2nG5tpA&usqp=CAU
   :alt: Logo
   :align: left
   :width: 100px
   :target: https://www.office.com/

Natural language processing (NLP) is a machine learning technology that gives computers the ability to interpret,
manipulate, and comprehend human language.

**Prompt:**

    An artificial intelligence (AI) prompt is a mode of interaction between a human and a large language model that lets
the model generate the intended output. This interaction can be in the form of a question, text, code snippets or examples.

**Normal text to SQL:**

.. code-block:: python

    async def nlp_to_sql(
        self,
        data_base: SQLDatabase,
        normal_text: str,
        prompt: str = None
   ):


The `nlp_to_sql()` function is used for generate the sql query from the normal text. It's return the sql response
object. The function have three params first one is for get Database object next one is for get user query text and
the last one for get prompt

.. code-block:: python

    get_llm_chain()

i the prompt value is `None` then the default prompt will be apply.
