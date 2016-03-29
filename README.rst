Micro Web Scraper
=================
A lightweight recursive HTML web scraper that takes a very simple
JSON file containing keys & xpaths and packages the response in JSON.

.. code-block::

    Usage: scraper [OPTIONS]

    Options:
      -f, --file FILENAME  name of JSON file containing xpaths
      -x, --xpath TEXT     XPATH expression
      -u, --url TEXT       URL of HTML page
      -P, --page FILENAME  name of file containing HTML content
      -t, --tidy           tidy HTML
      -v, --verbose        display the results for each scraper step
      --help               Show this message and exit.

keys that startwith '_' are arguments/parameters for the Python requests
module.  "_url" is a required key.

In it's simpliest form:

.. code-block:: json

    {
        "key1": "xpath expression"
    }

would return

.. code-block:: json

        {
            "key1": value
        }

If the XPath expression returns a list we can run additional xpath
expressions on each item in the returned list.

.. code-block:: json

    {
        "key-a": ["xpath expression that returns multiple items", {
            "nested-key-1": "another xpath expression",
            "nested-key-2": "another xpath expression",
        }],
        "key-b": "xpath expression"
    }

would return

.. code-block:: json

    {
        "key-a": [
            {
                "nested-key-1": value-1-1,
                "nested-key-2": value-1-2,
            },
            {
                "nested-key-1": value-2-1,
                "nested-key-2": value-2-2,
            }
        ]
    }

It's recursive so you can continue nesting as deep as needed. Check out
the working demos in the "examples" folder.

