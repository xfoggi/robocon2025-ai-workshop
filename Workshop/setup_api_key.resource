*** Settings ***
Library    RFOpenAILibrary.py

*** Keywords ***
Setup API Key And Model
    ${api_key_result}=    Set OpenAI API Key    OPENAI_API_KEY_SECRET
    Log    ${api_key_result}

    ${model_result}=    Set Model    gpt-4o-mini
    Log    ${model_result}