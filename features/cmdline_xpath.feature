Feature: Return the results of an XPath expression run against HTML

    Scenario: Process an XPath expression that returns text
        Given a XPath expression "/html/body/header/h1/text()"
        And a HTML page file "data\\w3c_html5_skeleton.html"
        When the XPath expression is processed against the HTML
        Then the output should match "HTML5 Skeleton"

    Scenario: Process an XPath expression that returns a Sequence
        Given a XPath expression "//article"
        And a HTML page file "data/w3c_html5_skeleton.html"
        When the XPath expression is processed against the HTML
        Then the output should match the file "output/articles.txt"

    Scenario: When the XPath is invalid show me where it failed
        Given a XPath expression "/html/body/[oops!!!]/h1"
        And a HTML page file "data/tiny_page.html"
        When the XPath expression is processed against the HTML
        Then display the XPath with a pointer below at the 12th character

    Scenario: Gracefully handle when XPath text doesn't return anything
        Given a XPath expression "/html/body/this_does_not_match/text()"
        And a HTML page file "data/w3c_html5_skeleton.html"
        When the XPath expression is processed against the HTML
        Then there should be no output

    Scenario: Gracefully handle when XPath sequence doesn't return anything
        Given a XPath expression "/html/body//no_match"
        And a HTML page file "data/w3c_html5_skeleton.html"
        When the XPath expression is processed against the HTML
        Then there should be no output
