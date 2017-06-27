Feature: Basic run-through of core site navigation
    
    Background:

        Given languages languageCategory in the database:
        | name       | description         | cross_institutional_url    |
        | English    | This is english     | http://www.monash.edu      |
        | French     | This is french      | http://www.unimelb.edu.au  |
        | Spanish    | This is spanish     | http://www.deakin.edu.au   |

        Given I have languages in the database:
        | name       | description         | cross_institutional_url    |
        | English    | This is english     | http://www.monash.edu      |
        | French     | This is french      | http://www.unimelb.edu.au  |
        | Spanish    | This is spanish     | http://www.deakin.edu.au   |

    Scenario Outline: A user can visit an 'individual language' page of the site
        Given I go to the url http://127.0.0.1:7000
        Then I see "I AM THE HOME PAGE"

        When I click "What languages can I study?"
        Then I see "THIS IS THE WHAT LANGUAGES CAN I STUDY PAGE"
        And  I see "This is english"
        And  I see "This is french"
        And  I see "This is spanish"

        When I click "French"
        Then I see "I AM THE FRENCH PAGE"
