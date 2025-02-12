*** Settings ***
Library    RFOpenAILibrary.py

*** Test Cases ***
Send A Message to OpenAI
    [Documentation]    Demonstrates setting the API key, configuring the model, and sending a message.
    ${api_key_result}=    Set OpenAI API Key    OPENAI_API_KEY_SECRET
    Log    ${api_key_result}
    
    ${model_result}=    Set Model    gpt-4o-mini
    Log    ${model_result}
    
    ${response}=    Send Message    Hello, how do I integrate AI?
    Log    ${response}