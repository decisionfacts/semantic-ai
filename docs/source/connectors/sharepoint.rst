Microsoft Sharepoint
==========

This documents covers how to download the documents from Sharepoint.

Pre-requisites
-------------

Register an application with the `Microsoft identity platform <https://learn.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app>`_ and create the client_id, client_secret and tenant_id.

To create a sharepoint connection with credentials
--------------------------------------------------

.. code-block:: python

    CLIENT_ID = '<client_id>'
    CLIENT_SECRET = '<client_secret>'
    TENANT_ID = '<tenant_id>'
    SCOPE = 'https://graph.microsoft.com/.default'
    HOST_NAME = "<tenant_name>.sharepoint.com"

.. code-block:: python

    from semantic_ai.connectors import Sharepoint
    connection = Sharepoint(
            client_id = CLIENT_ID,
            client_secret = CLIENT_SECRET,
            tenant_id = TENANT_ID,
            scope = SCOPE,
            host_name = HOST_NAME
    )