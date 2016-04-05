Feature: load, parse & display HTML content from a file
    As a developer, tester or end-user
    I want to work with the HTML pages offline
    So that I am not dependent on an Internet connection
    And do not have to wait for HTTP requests to complete

    Scenario: display HTML file
        Given a HTML page file "data\broken_page.html"
        When the page is parsed
        Then the output should match the file "output\parsed_broken_page.html"

    Scenario: gracefully handle non-existant HTML file
        Given a HTML page file "oops.html"
        When the file can not be found
        Then display an informative file not found message
