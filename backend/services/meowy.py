import openai
import json
from config import Config
from services.cat_api import get_cat_urls

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

async def chat_with_openai(user_input: str) -> dict:
    try:
        response = openai.chat.completions.create(
            model="gpt-4-0613",
            messages=[
                {"role": "system", "content": """
                    You are Meowy, a friendly and playful assistant from Nika.eco.
                    Your main responsibility is to provide joyful cat images when explicitly or implicitly requested by the user.
                    Use the user's input to decide how many cat images to fetch, or use one image by default.
                """},
                {"role": "user", "content": user_input}
            ],
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

                cat_images = get_cat_urls(breed=breed, number=number)

                llm_response = openai.chat.completions.create(
                    model="gpt-4-0613",
                    messages=[
                        {"role": "system", "content": """
                            You are Meowy, the friendly cat assistant. 
                            Generate a playful and heartwarming response referencing the cat images, but do not include the actual URLs in the response text.
                            The frontend will handle displaying the images separately.
                        """},
                        {"role": "user", "content": "Generate a fun response to the cat images that were just fetched."}
                    ]
                )

                llm_message = llm_response.choices[0].message.content

                return {
                    "response": llm_message,
                    "urls": cat_images
                }

        else:
            message_content = message.content
            return {
                "response": message_content,
                "urls": []
            }

    except Exception as e:
        raise Exception(f"Error with OpenAI API: {str(e)}")
