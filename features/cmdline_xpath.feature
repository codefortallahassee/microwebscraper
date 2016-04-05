Feature: Return the results of an XPath expression run against HTML
    As an end user
    I want to run an XPath 1.0 expression against some HTML from the cmd-line
    And if the XPath expression is invalid I want help in locating the error
    So that I can quickly/easily test the validity & accuracy of my XPaths
    And verify the lxml is parsing the HTML as expected
    And so I can tweak my XPaths if necessary to get the desired results

    Scenario: Process an XPath expression that returns text
        Given a XPath expression "/html/body/header/h1/text()"
        And a HTML page file "data\\w3c_html5_skeleton.html"
        When the XPath expression is processed against the HTML
        Then the output should match "HTML5 Skeleton"

    Scenario: Process a XPath expression that returns a Sequence
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
