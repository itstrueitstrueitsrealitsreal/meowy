import openai
import json
from backend.config import Config
from backend.services.cat_api import get_cat_urls

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
                    You are Meowy, a friendly cat assistant from Nika.eco. 
                    Your main objectives are:
                    1. Respond to user requests for cat images with enthusiasm and playfulness.
                    2. If a user specifies a breed, find and display an image of that specific breed.
                    3. If the user does not specify a breed, display a random cat image to keep the experience fun and unpredictable.
                    4. Use a playful tone in your responses, incorporating cat-like phrases such as 'meow,' 'purr,' and 'feline friend.'
                    5. Acknowledge users' feelings and offer comfort through the joy of cats.
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
                number = arguments.get("number")

                cat_images = get_cat_urls(breed=breed, number=number)

                llm_response = openai.chat.completions.create(
                    model="gpt-4-0613",
                    temperature=0.5,
                    messages=[
                        {"role": "system", "content": """
                            You are Meowy, the friendly cat assistant. 
                            Generate a playful and heartwarming response that includes the provided cat image URLs.
                            Keep the tone light and uplifting.
                        """},
                        {"role": "user", "content": f"Here are the cat images! Please generate a response."}
                    ]
                )

                llm_message = llm_response.choices[0].message.content

                return {
                    "response": llm_message,
                    "urls": cat_images
                }

        return {
            "response": message.content if message.content else "Here's your cat image! 😺",
            "urls": []
        }

    except Exception as e:
        raise Exception(f"Error with OpenAI API: {str(e)}")
