Feature: load, format & display HTML content from a file
    As a developer, I want to explore the data offline
    And as a tester, I want to be able to run tests offline
    So that I am not dependent on an Internet connection
    And so that I don't have to wait for a HTTP request to complete
    And so I can view & navigate the data using a variety of tools


    Scenario: format & display HTML from a file
        Given a HTML file named "data\\webpage.html"
        Then format/tidy the HTML and output it to the console
        And the output format should match "output\\tidy_webpage.html"

    Scenario: gracefully handle non-existant HTML file
        Given a HTML file named "oops.html"
        When the file can not be found
        Then display a friendly, informative file not found message
