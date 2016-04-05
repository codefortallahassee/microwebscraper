Feature: scrape data from an HTML file using a JSON configuration file
    As an analyst, developer or end-user
    I want to scrape data from web pages using just JSON & XPath 1.0
    And I want the scraped values to be returned in JSON in names that I define
    So that I can quickly build reliable web scrapers without touching code
    And without learning specialized syntax
    So I can focus my time on real world usage of the data, not on scraping it
    And when web pages change I can quickly reconfigure the scraper to match.

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
