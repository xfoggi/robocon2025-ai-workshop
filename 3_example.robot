*** Settings ***
Library    RFOpenAILibrary.py

Test Setup    Setup OpenAI

*** Test Cases ***
Simple Test
    Set Instructions    You are a Finish comedian and you are very funny, and you speak in English.

    ${response}    Send Message With History    Joke about weather.

    ${response}    Send Message With History    Translate to Czech.

Create Addresses  
    ${response}    Generate Real Addresses    10 addresses in Helsinki
    Log    ${response}

Create Phone Numbers
    ${response}    Generate Data    Phone numbers test data generator in international format: 00-420-601-123-123    I want 10 finish phone numbers    csv with ; delimiter

    Log    ${response}

*** Keywords ***
Setup OpenAI
    Set Openai Api Key  OPENAI_API_KEY_SECRET

    Set Model    gpt-4o-mini