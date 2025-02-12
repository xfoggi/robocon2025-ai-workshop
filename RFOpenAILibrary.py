from openai import OpenAI
import json

class RFOpenAILibrary:
    def __init__(self):
        self.client = None
        self.model = None
        self.instructions = None
        self.history = []

    def set_openai_api_key(self, api_key):
        self.client = OpenAI(api_key=api_key)
        return

    def set_model(self, model_name):
        self.model = model_name
        return
    
    def set_instructions(self, instructions):
        self.instructions = instructions
        return

    def send_message(self, message):
        messages = [
            {"role": "system", "content": self.instructions},
            {"role": "user", "content": message}
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )

        return response.choices[0].message.content
    
    def send_message_with_history(self, message):         
        self.history.append({"role": "user", "content": message})
       
        messages = [
            {"role": "system", "content": self.instructions}            
        ]
        messages.extend(self.history)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )

        print(response)

        assistant_response = response.choices[0].message.content
        self.history.append({"role": "assistant", "content": assistant_response})

        print(json.dumps(self.history))
        return assistant_response
    
    def generate_real_addresses(self, message):
        instructions = "You are generating real addresses with real people, output is provided in JSON format like: {'persons name', 'address', 'postal code', 'city'}. Dont include any other text or MD markings."

        messages = [
            {"role": "system", "content": instructions},
            {"role": "user", "content": message}
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )

        print(response)
        return response.choices[0].message.content
    
    def generate_data(self, instructions, message, format):
        messages = [
            {"role": "system", "content": f"{instructions} and keep the exact format: '{format}'. Dont include any other text or MD markings."},
            {"role": "user", "content": message}
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )

        print(response)
        return response.choices[0].message.content