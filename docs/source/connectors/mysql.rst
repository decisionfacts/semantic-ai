MYSQL
======

.. figure:: https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRmvZum7UQzH7A7I6M-f4Rjdth_UEf4i6_0SA&usqp=CAU
   :alt: Logo
   :align: left
   :width: 100px
   :target: https://www.office.com/



This documents covers how to interact with Mysql database using our library.

**Pre-requisites:**

    Please make sure the credentials of Mysql DB.

**Setup:**


**To create a mysql connection using credentials**

    Please setup the value to the following environment object

.. code-block:: python

    MYSQL_HOST='<host>'
    MYSQL_USER='<user>'
    MYSQL_PASSWORD='<password>'
    MYSQL_DATABASE='<database>'
    MYSQL_PORT='<port>'


.. code-block:: python

    from semantic_ai.connectors import Mysql

        conn = Mysql(
                    host='',
                    user='',
                    password='',
                    database='',
                    port=""
                    )
        cursor = await conn.connect_db()

**To create natural language processing for normal text**

.. code-block:: python

    from semantic_ai.nlp.prompt import Prompt

    prompt = Prompt()
    prompt_res = await prompt.nlp_to_sql(data_base=cursor, normal_text="query")

**To get answer from NLP**

.. code-block:: python

    data = json.loads(prompt_res)
    result = sql.execution(data)



