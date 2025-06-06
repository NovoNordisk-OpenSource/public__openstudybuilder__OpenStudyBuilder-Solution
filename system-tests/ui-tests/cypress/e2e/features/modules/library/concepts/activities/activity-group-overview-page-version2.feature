@REQ_ID:1070683
Feature: Library - Concepts - Activities - Activity Group Overview Page (Version 2)
    As a user, I want to verify that the Activity Group Overview Page version 2 in the Concepts Library, can display correctly.

    Background: 
        Given The user is logged in
        When [API] Activity Instance in status Final with Final group, subgroup and activity linked exists
        And Group name created through API is found
        And Subgroup name created through API is found

@pending_development
    Scenario: Verify that the activity group overview page version 2 displays correctly
        Given The '/library/activities/activity-groups' page is opened
        When I click on the test activity group name in the activity group page
        Then The test group overview page should be opened
        And The Activity subgroups table will be displayed with correct column
        And The linked subgroup should be displayed in the Activity subgroups table
        And The free text search field should be displayed in the Activity subgroups table
        # And The free text search field in the Activity subgroups table should work (this scenario will be implemented in the future)
        
@pending_development
    Scenario: Verify that the activities group overview page version 2 can link to the correct subgroup
        Given The '/library/activities/activity-groups' page is opened
        When I click on the test activity group name in the activity group page
        Then The test group overview page should be opened
        When I select the version '0.1' from the Version dropdown list
        Then The correct End date should be displayed
        And The status should be displayed as 'Draft'
        And The Activity subgroups table should be empty
        When I select the version '1.0' from the Version dropdown list
        Then The linked subgroup should be displayed in the Activity subgroups table

@pending_development
    Scenario: Verify that the pagination works in the Activity subgroups table
        Given The '/library/activities/activity-groups' page is opened
        When I search for the test activity group through the filter field
        When I click on the test activity group name in the activity group page
        Then The test group overview page should be opened
        When I select 5 rows per page from dropdown list in the Acitivity subgroups table
        Then The Acitivity subgroups table should be displayed with 5 rows per page
        When I click on the next page button in the Acitivity subgroups table
        Then The Acitivity subgroups table should display the next page within 5 rows per page
         When I select 10 rows per page from dropdown list in the Acitivity subgroups table
        Then The Acitivity subgroups table should be displayed with 10 rows per page
        When I click on the next page button in the Acitivity subgroups table
        Then The Acitivity subgroups table should display the next page within 10 rows per page