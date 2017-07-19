Feature: Basic run-through of core site navigation
    

    Scenario Outline: Check nav links
        Given I go to the url http://0.0.0.0:7000
        Then I see "Home Page Heading"

        When I click "About"
        Then I see "The About Page"
        And I see "About Page Content"

        When I click "FAQ"
        Then I see "Obvious Questions"

        When I click "Contact"
        Then I see "THIS IS THE CONTACT PAGE"

        Given I go to the url http://0.0.0.0:7000

        When I click "Study at other University"
        Then I see "THIS IS THE WHAT LANGUAGE CAN I STUDY AT A UNIVERSITY OTHER THAN MY OWN PAGE"

        Given I go to the url http://0.0.0.0:7000

        When I click "Where can I study Indigenous Languages"
        Then I see "THIS IS THE WHERE CAN I STUDY INDIGENOUS LANGUAGES PAGE"

        Given I go to the url http://0.0.0.0:7000

        When I click "What languages can I study?"
        Then I see "THIS IS THE WHAT LANGUAGES CAN I STUDY PAGE"

        When I fill in "Language" with "English"
        And I press "Search"
        Then I should see ""

        Given I go to the url http://0.0.0.0:7000

        When I click "Why study languages?"
        Then I see "THIS IS THE WHY STUDY LANGUAGES PAGE"

        Given I go to the url http://0.0.0.0:7000

        When I click "Home"
        Then I see "I AM THE HOME PAGE"
