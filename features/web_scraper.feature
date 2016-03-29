Feature: scrape data from an HTML file
    As an analyst or developer
    I want to scrape data from web pages using just JSON & XPath 1.0
    So that I can quickly build applications that use the data in new ways
    And if a web page changes I want to be able to fix it by only modify a simple JSON file, not the underlying code.


    Scenario: get the H1 header from HTML file
        Given a config file named "config\\skeleton_header.json"
        And a HTML file named "data\\w3c_html5_skeleton.html"
        When page is scraped
        Then the data should match "output\skeleton_header.json"

    Scenario: get a list of article titles and contents from HTML file
        Given a config file named "config\\skeleton_articles.json"
        And a HTML file named "data\\w3c_html5_skeleton.html"
        When page is scraped
        Then the data should match "output\skeleton_articles.json"
