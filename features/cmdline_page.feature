Feature: load, format & display HTML content from a file
    As a developer, I want to view the HTML offline
    And as a tester, I want to be able to test offline
    So that I am not dependent on an Internet connection
    And so that I don't have to wait for a HTTP request to complete
    And so I can output highly readable HTML text from the command-line


    Scenario: format & display HTML from a file
        Given a HTML page file "data\\tiny_page.html"
        When the tidy option is selected
        Then the output should match the file "output\tidy_tiny_page.html"

    Scenario: gracefully handle non-existant HTML file
        Given a HTML page file "oops.html"
        When the file can not be found
        Then display an informative file not found message
