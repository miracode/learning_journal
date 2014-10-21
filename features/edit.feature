Feature: Enable editing for Learning Journal

    Scenario: Anonymous user cannot see edit button
        Given an anonymous user
        And en entry exists
        When I view the home page
        Then I do not see the edit button for an entry

    Scenario: Logged in user can see edit button
        Given an authenticated user
        And an entry exists
        When I view the home page
        Then I see the edit button for an entry

    Scenario: Anonymous user cannot submit edited form
        Given an anonymous user
        And the title "Edited Post"
        And the text "This is edited text"
        When I submit the edited form
        Then I am redirected to the home page
        And I do not see an edited entry

    Scenario: Logged in user can submit edited form
        Given an authenticated user
        And the title "Edited Post"
        And the text "This is an edited post"
        When I submit the edited form
        Then I am redirected to the home page
        And I see the edited entry