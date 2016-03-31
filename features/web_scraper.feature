Feature: scrape data from an HTML file
    As an analyst or developer
    I want to scrape data from web pages using just JSON & XPath 1.0
    So that I can quickly build applications that use the data in new ways
    And if a web page changes I want to be able to fix it by only modify a simple JSON file, not the underlying code.


    Scenario: get the H1 header from HTML file
        Given a configuration file "config\\skeleton_header.json"
        And a HTML page file "data\\w3c_html5_skeleton.html"
        When the page is scraped
        Then the output should match the file "output\skeleton_header.json"

    Scenario: get a list of article titles and contents from HTML file
        Given a configuration file "config\\skeleton_articles.json"
        And a HTML page file "data\\w3c_html5_skeleton.html"
        When the page is scraped
        Then the output should match the file "output\skeleton_articles.json"
