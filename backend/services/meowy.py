import openai
import json
from config import Config
from services.cat_api import get_cat_urls, get_id

openai.api_key = Config.OPENAI_API_KEY

cat_function_schema = {
    "name": "get_cat_urls",
    "description": "Fetch URLs of cats based on breed and number.",
    "parameters": {
        "type": "object",
        "properties": {
            "breed": {
                "type": "string",
                "description": "The breed of cat to fetch images for."
            },
            "number": {
                "type": "integer",
                "description": "The number of cat images to fetch.",
                "minimum": 1,
                "maximum": 100
            }
        },
        "required": ["number"]
    }
}

async def chat_with_openai(user_input: str, history: list = None) -> dict:
    """
    Sends user input along with conversation history to OpenAI's API and processes the response.
    """
    try:
        messages = [
            {"role": "system", "content": """
                You are Meowy, a friendly and engaging assistant who is part of the Cat Delivery Network.
                Your goal is to provide enjoyable responses and cat images when users ask for them.
                If the user specifies a breed, show an image of that breed if possible, otherwise provide a random cat image.
            """}
        ]

        if history:
            messages += history

        messages.append({"role": "user", "content": user_input})

        response = openai.chat.completions.create(
            model="gpt-4-0613",
            messages=messages,
            functions=[cat_function_schema],
            function_call="auto"
        )

        message = response.choices[0].message

        if message.function_call is not None:
            function_name = message.function_call.name
            if function_name == "get_cat_urls":
                arguments = json.loads(message.function_call.arguments)
                breed = arguments.get("breed")
                number = arguments.get("number", 1)

                if not get_id(breed):
                    breed_error_msg = f"Sorry, we couldn't find any images of the '{breed}' breed. But here's a cute random cat instead!"
                    cat_images = get_cat_urls(breed=None, number=number)  
                else:
                    cat_images = get_cat_urls(breed=breed, number=number)

                    breed_error_msg = None

                # Generate the final response message with breed validation
                llm_response = openai.chat.completions.create(
                    model="gpt-4-0613",
                    messages=[
                        {"role": "system", "content": f"""
                            You are Meowy, the friendly cat assistant who is part of the Cat Delivery Network.
                            Generate a warm and engaging response, keeping the tone casual and fun.
                            Mention a fun fact about {breed}.
                        """},
                        {"role": "user", "content": "Generate a response to the cat images that were just fetched, and a fun fact about the breed if valid."}
                    ]
                )

                llm_message = llm_response.choices[0].message.content

                if breed_error_msg:
                    llm_message = breed_error_msg + "\n\n" + llm_message

                return {
                    "response": llm_message,
                    "urls": cat_images
                }

        else:
            # No function call was made, return the assistant's response directly
            message_content = message.content
            return {
                "response": message_content,
                "urls": []
            }

    except Exception as e:
        raise Exception(f"Error with OpenAI API: {str(e)}")
