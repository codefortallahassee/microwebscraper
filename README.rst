Micro Web Scraper
=================
A lightweight recursive HTML web scraper that takes a very simple
JSON file containing keys & xpaths and packages the response in JSON.

.. code-block::

    Usage: scraper [OPTIONS]

    Options:
      -c, --config FILENAME       name of JSON config file containing request &
                                  xpath info
      -i, --indent INTEGER RANGE  indent size for output
      -t, --tidy                  tidy HTML (normalizes space & indent)
      -u, --url TEXT              URL of HTML page
      -v, --verbose               display the results for each scraper step
      -x, --xpath TEXT            XPATH expression
      -p, --page FILENAME         name of file containing HTML content
      --raw                       bypass parser, output raw HTML
      --help                      Show this message and exit.

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

