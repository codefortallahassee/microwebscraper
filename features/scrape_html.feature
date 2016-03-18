Feature: scrape data from an HTML web page

    Scenario: get the H1 header from HTML file
        Given a xpaths file named "config\\skeleton_header.json"
        And a HTML file named "data\\w3c_html5_skeleton.html"
        Then scraped data should match "output\skeleton_header.json"

    Scenario: get a list of article titles and contents from HTML file
        Given a xpaths file named "config\\skeleton_articles.json"
        And a HTML file named "data\\w3c_html5_skeleton.html"
        Then scraped data should match "output\skeleton_articles.json"
