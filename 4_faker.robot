*** Settings ***
Library    RFOpenAILibrary.py
Resource    setup_api_key.resource

Test Setup    Setup API Key And Model

*** Test Cases ***
Generate Fake Phone Number
    ${phone}=    Generate Fake Phone Number
    Log    Fake Phone Number: ${phone}

Generate Fake Address
    ${address}=    Generate Fake Address
    Log    Fake Address: ${address}

Generate Fake Email
    ${email}=    Generate Fake Email
    Log    Fake Email: ${email}


# TODO: update prompting to only return correct values