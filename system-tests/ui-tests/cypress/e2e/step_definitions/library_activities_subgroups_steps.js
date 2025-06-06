import { apiGroupName } from "./api_library_steps"
const { Given, When, Then } = require("@badeball/cypress-cucumber-preprocessor");

let activitysubgroup, apiActivitySubGroupName
let abbreviation = "ABB", definition = "DEF"

When('The Add activity subgroup button is clicked', () => cy.clickButton('add-activity'))

When('The subgroup can be find in table', () => cy.searchAndCheckPresence(apiActivitySubGroupName, true))

When('The test activity subgroup container is filled with data and saved', () => {
    fillSubGroupData(false)
    saveSubGroup()
})

When('Approved Group can be linked to subgroup', () => {
    fillSubGroupData(true, apiGroupName)
    saveSubGroup()
})

When('The test activity subgroup container is filled with data', () => fillSubGroupData())

Then('The newly added activity subgroup is visible in the the table', () => {  
    cy.searchAndCheckPresence(activitysubgroup, true)
    cy.checkRowByIndex(0, 'Activity subgroup', activitysubgroup)
    cy.checkRowByIndex(0,'Sentence case name', activitysubgroup.toLowerCase())
    cy.checkRowByIndex(0, 'Abbreviation', abbreviation)
    cy.checkRowByIndex(0, 'Definition', definition)
})

When('The Activity groups, Subgroup name, Sentence case name and Definition fields are not filled with data', () => {
    cy.fillInput('groupform-activity-group-field', 'test')
    cy.clearInput('sentence-case-name-field')
    cy.clearInput('groupform-activity-group-field')
    cy.clickButton('save-button')
})

Then('The user is not able to save the acitivity subgroup', () => {   
    cy.get('div[data-cy="form-body"]').should('be.visible');          
    cy.get('span.dialog-title').should('be.visible').should('have.text', 'Add activity subgroup'); 
})

Then('The message is displayed as {string} in each of the mandatory field', (message) => {  
    cy.get('[data-cy="groupform-subgroup-class"]').contains('.v-messages__message', message).should('be.visible'); 
    cy.get('[data-cy="groupform-activity-group-class"]').contains('.v-messages__message', message).should('be.visible'); 
    cy.get('[data-cy="sentence-case-name-class"]').contains('.v-messages__message', message).should('be.visible');
    cy.get('[data-cy="groupform-definition-class"]').contains('.v-messages__message', message).should('be.visible');
})

When('The user enters a value for Activity subgroup name', () => {
    cy.fillInput('groupform-activity-group-field', "TEST")
})

Then('The field for Sentence case name will be defaulted to the lower case value of the Activity subgroup name', () => {      
    cy.get('[data-cy="sentence-case-name-field"] input').should('have.value', 'test')
})

When('The user define a value for Sentence case name and it is not identical to the value of Activity subgroup name', () => {
    cy.fillInput('groupform-activity-group-field', "TEST")
    cy.fillInput('sentence-case-name-field', "TEST2")
    cy.clickButton('save-button')
})

When('The activity subgroup is edited', () => {
    editSubGroup()
    saveSubGroup('updated')
})

When('The activity subgroup edition form is filled with data', () => editSubGroup())

Then('The activity subgroup is no longer available', () => cy.searchAndCheckPresence(apiActivitySubGroupName, false))

Then('The activity subgroup is not created', () => cy.searchAndCheckPresence(activitysubgroup, false))

Then('The activity subgroup is not edited', () => cy.searchAndCheckPresence(activitysubgroup, false))

Then('One activity subgroup is found after performing full name search', () => cy.searchAndCheckPresence(apiActivitySubGroupName, true))

When('[API] Activity subgroup in status Draft exists', () => createSubGroupViaApi())

When('[API] Activity subgroup is approved', () => cy.approveSubGroup())

When('[API] Activity subgroup is inactivated', () => cy.inactivateSubGroup())

When('[API] Activity subgroup is reactivated', () => cy.reactivateSubGroup())

When('[API] Activity subgroup gets new version', () => cy.subGroupNewVersion())

Given('[API] First activity subgroup for search test is created', () => createSubGroupViaApi(`SearchTest${Date.now()}`))

Given('[API] Second activity subgroup for search test is created', () => cy.createSubGroup(`SearchTest${Date.now()}`))

Given('[API] Activity subgroup is created', () => cy.createSubGroup())

When('Activity subgroup is found', () => cy.searchAndCheckPresence(apiActivitySubGroupName, true))

When('Drafted or Retired group is not available during subgroup creation', () => selectCustomGroup(apiGroupName))

function selectCustomGroup(customGroup) {
    cy.get('[data-cy="groupform-activity-group-dropdown"] input').type(customGroup)
    cy.get('.v-overlay__content .v-list-item-title').should('have.text', 'No data available')
}

function fillSubGroupData(clickAddButton = true, customGroup = '') {
    activitysubgroup = `Subgroup${Date.now()}`
    if (clickAddButton) cy.clickButton('add-activity')
    cy.wait(1000)
    if (customGroup) cy.get('[data-cy="groupform-activity-group-dropdown"] input').type(customGroup)
    cy.selectFirstVSelect('groupform-activity-group-dropdown')
    cy.fillInput('groupform-activity-group-field', activitysubgroup)
    cy.fillInput('groupform-abbreviation-field', abbreviation)
    cy.fillInput('groupform-definition-field', definition) 
}

function editSubGroup() {
    activitysubgroup = `${activitysubgroup}Edited`
    cy.fillInput('groupform-activity-group-field', activitysubgroup)
    cy.fillInput('groupform-change-description-field', "e2e test")
}

function saveSubGroup(action = 'created') {
    cy.intercept('/api/concepts/activities/activity-sub-groups?page_number=1&*').as('getData')
    cy.clickButton('save-button')
    cy.get('.v-snackbar__content').contains(`Subgroup ${action}`).should('be.visible')
    cy.wait('@getData', {timeout: 20000}) 
    cy.searchAndCheckPresence(activitysubgroup, true)
}

function createSubGroupViaApi(customName = '') {
    cy.intercept('/api/concepts/activities/activity-sub-groups?page_number=1&*').as('getData')
    cy.getFinalGroupUid()
    cy.createSubGroup(customName)
    cy.getSubGroupNameByUid().then(name => apiActivitySubGroupName = name)
    cy.wait('@getData', {timeout: 20000})
}