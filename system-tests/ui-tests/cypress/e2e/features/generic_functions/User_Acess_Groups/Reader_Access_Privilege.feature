@REQ_ID:2332138
@pending_implementation

Feature: StudyBuilder: Reader access privilege
Pre-requisite note: User granted access with a Role as 'StudyBuilder: Reader ('Environment')' in novoAccess prior verification of the below functional requirement.

  As a user, I want to able to logged in with read access previlege for both 'Studies' and 'Library' Modules
  Background: User must be logged in
    Given The user is logged in

    Scenario: User must be able to view the data fields in the 'Library' Module
    Given The '/library' page is opened
    When The 'Library' menu is clicked in the Home page
    And 'Objective Templates' is clicked under 'Syntax Templates' menu item
    Then The sample data records for templates are visible on the main page.

   Scenario: User must not be able to have write access previlege in the data fields of the 'Library' Module
    Given The '/library' page is opened
    When The 'Library' module is clicked in the Home page
    And 'CT Catalogues' sub-menu is clicked under 'Code Lists' menu item 
    Then The 'All' tab window is not displayed with '+' (Cursor help text displayed as 'Add sponsor code list') option on the right side menu list
    And The 'Edit' option is not available in the three dot menu list for the available sample test Code list item.

  Scenario: User must be able to navigate to the 'Studies' Module
    Given The '/studies' page is opened
    When The 'Studies' menu is clicked in the Home page
    Then The left panel window displayed with mulitple Selection Menu options

   Scenario: User must be able to view the data fields in the 'Studies' Module
    Given The '/studies' page is opened
    When The 'Studies' menu is clicked in the Home page
    And 'Study Criteria' is clicked under 'Define Study' menu item
    Then The sample data records for criteria are visible on the main page.

   Scenario: User must not be able to have write access previlege in the data fields of the 'Studies' Module
    Given The '/studies' page is opened
    When The 'Studies' module is clicked in the Home page
    And 'Study Activities' sub-menu is clicked under 'Define Study' menu item 
    Then The 'List of Study Activities' tab window is not displayed with '+' (Cursor help text displayed as 'Add study activities') option on the right side menu list
    And The 'Edit' option is not available in the three dot menu list for the available sample test Study Activities.