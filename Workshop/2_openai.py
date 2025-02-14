from openai import OpenAI
import json

client = OpenAI(api_key="OPENAI_API_KEY_SECRET")

messages = [
    {"role": "system", "content": "You are an test email generator, provide email adresses in json format. Only provide the json object, no other texts or '```'."},
    {"role": "user", "content": "Give me 10 gmail adresses, each should have different name."}
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages
)

assistant_reply = response.choices[0].message.content
print("Assistant: ", assistant_reply)

messages.append(
    {"role": "assistant", "content": assistant_reply}
)

messages.append({
    "role": "user", "content": "Give me only female email adresses from the list."
})

print(json.dumps(messages))

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages
)

print(response)

assistant_reply = response.choices[0].message.content
print("Assistant: ", assistant_reply)