==================
Eloqua Formhandler
==================

Validate and send Oracle Eloqua Forms.

`REST API for Oracle Eloqua Marketing Cloud Service <https://docs.oracle.com/cloud/latest/marketingcs_gs/OMCAC/index.html>`_

Quickstart
----------

.. code-block:: python

   import requests
   from eloquaformhandler.handler import HandlerFactory

   session = requests.Session()
   session.auth = (ELOQUA_USER, ELOQUA_PASSWORD)
   handler = HandlerFactory.get(session)(FORM_ID)
   # send form data
   # if everything went fine status_code is 201 and json_response is None
   json_response, status_code = handler(form_data)
