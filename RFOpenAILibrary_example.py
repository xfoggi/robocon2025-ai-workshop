import openai
from openai import OpenAI

class RFOpenAILibrary:
    def __init__(self):
        self.client = None
        self.model = None

    def set_openai_api_key(self, api_key):
        """
        Set the OpenAI API key and initialize the client.

        Arguments:
        - api_key: Your OpenAI API key.

        Returns:
        - A confirmation message.
        """
        self.client = OpenAI(api_key=api_key)
        return "OpenAI API key set."

    def set_model(self, model_name):
        """
        Set the model to be used for chat completions.

        Arguments:
        - model_name: The name of the model (e.g., 'gpt-4o-mini').

        Returns:
        - A confirmation message.
        """
        self.model = model_name
        return f"Model set to {model_name}"

    def send_message(self, message):
        """
        Send a message to the OpenAI API and return the assistant's response.

        Arguments:
        - message: The message string to send to the API.

        Returns:
        - The assistant's reply as a string, or an error message if the API call fails.
        """
        if self.client is None:
            return "Error: OpenAI API client is not initialized. Please set the API key first."
        if self.model is None:
            return "Error: Model is not set. Please set the model first."

        messages = [{"role": "user", "content": message}]
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            reply = response.choices[0].message.content
            return reply
        except Exception as e:
            return f"Error sending message: {e}"
    
    def generate_fake_phone_number(self):
        """
        Generate a fake phone number in international format using AI.

        Returns:
        - A string representing a fake phone number.
        """
        prompt = "Generate a fake phone number in international format."
        return self.send_message(prompt)

    def generate_fake_address(self):
        """
        Generate a realistic address including street, city, state, postal code, and country in JSON format using AI.

        Returns:
        - A JSON string representing a realistic address.
        """
        prompt = "Generate a realistic address including street, city, state, postal code, and country in JSON format."
        return self.send_message(prompt)

    def generate_fake_email(self):
        """
        Generate a realistic email address that looks like it could belong to a person using AI.

        Returns:
        - A string representing a realistic email address.
        """
        prompt = "Generate a realistic email address that looks like it could belong to a person."
        return self.send_message(prompt)