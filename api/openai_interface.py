import openai
import logging

# Define a class to interface with OpenAI's API
class GPTInterface:
    # Initialize the class with API credentials
    def __init__(self, api_token, org_id):
        self.api_key = api_token  # Set the API token
        self.org_id = org_id  # Set the organization ID
        self.set_api_credentials()  # Apply the credentials to the OpenAI API

    # Method to set OpenAI API credentials
    def set_api_credentials(self):
        try:
            openai.api_key = self.api_key  # Apply the API token
            openai.organization = self.org_id  # Apply the organization ID
        except Exception as e:
            # Log any errors that occur during credential setup
            logging.error(f"Failed to set API credentials: {e}")

    # Method to update the API token
    def set_api_token(self, api_token):
        try:
            self.api_key = api_token  # Update the API token
            self.set_api_credentials()  # Reapply credentials
        except Exception as e:
            # Log any errors that occur during token update
            logging.error(f"Failed to set API token: {e}")

    # Method to update the organization ID
    def set_api_org(self, org_id):
        try:
            self.org_id = org_id  # Update the organization ID
            self.set_api_credentials()  # Reapply credentials
        except Exception as e:
            # Log any errors that occur during organization ID update
            logging.error(f"Failed to set API organization: {e}")

    # Method to send text prompts to the API and receive text responses
    def create_prompt_response(self, model_engine, prompt, max_tokens=1024, temperature=0.5):
        try:
            # Use OpenAI API to generate a response to the prompt
            completion = openai.Completion.create(
                engine=model_engine,
                prompt=prompt,
                max_tokens=max_tokens,
                n=1,
                stop=None,
                temperature=temperature
            )
            return completion.choices[0].text  # Return the generated text
        except openai.error.OpenAIError as e:
            # Log any OpenAI API specific errors and re-raise them
            logging.error(f"OpenAI API Error in create_prompt_response: {e}")
            raise
        except Exception as e:
            # Log any unexpected errors and re-raise them
            logging.error(f"Unexpected error in create_prompt_response: {e}")
            raise

    # Method to send prompts to the API and receive image responses
    def create_image_response(self, prompt):
        try:
            # Use OpenAI API to generate an image based on the prompt
            response = openai.Image.create(
                prompt=prompt,
                size="1024x1024"
            )
            return response['data'][0]['url']  # Return the URL of the generated image
        except openai.error.OpenAIError as e:
            # Log any OpenAI API specific errors and re-raise them
            logging.error(f"OpenAI API Error in create_image_response: {e}")
            raise
        except Exception as e:
            # Log any unexpected errors and re-raise them
            logging.error(f"Unexpected error in create_image_response: {e}")
            raise

    # General method to get a response from the API, defaulting to text
    def get_response(self, prompt, model_engine="text-davinci-003"):
        try:
            # Use the create_prompt_response method to get a text response
            return self.create_prompt_response(model_engine, prompt)
        except Exception as e:
            # Log any errors that occur during the get_response process and re-raise them
            logging.error(f"Error in get_response: {e}")
            raise
