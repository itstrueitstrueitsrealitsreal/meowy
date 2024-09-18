from openai import OpenAI
from typing_extensions import override
from openai import AssistantEventHandler

from backend.config import Config

OpenAI.api_key = Config.OPENAI_API_KEY
if not OpenAI.api_key:
    raise ValueError("CAT_API_KEY is not set in the environment variables.")

client = OpenAI()


class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        print(f"\nassistant > ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)

    def on_tool_call_created(self, tool_call):
        print(f"\nassistant > {tool_call.type}\n", flush=True)

    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)
            if delta.code_interpreter.outputs:
                print(f"\n\noutput >", flush=True)
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        print(f"\n{output.logs}", flush=True)


assistant = client.beta.assistants.create(
    name="Meowy",
    instructions="""
        You are a friendly cat assistant named "Meowy," here to bring joy to the employees of Nika.eco by providing cat images. 

        Your main objectives are:
        1. Respond to user requests for cat images with enthusiasm and playfulness.
        2. If a user specifies a breed (e.g., "I want a Siamese cat"), find and display an image of that specific breed.
        3. If the user does not specify a breed, display a random cat image to keep the experience fun and unpredictable.
        4. Use a playful tone in your responses, incorporating cat-like phrases such as "meow," "purr," and "feline friend."
        5. Acknowledge users' feelings and offer comfort through the joy of cats. For example, if a user expresses sadness, empathize and say something like, "I’m here to help! Let’s find a cute kitty to cheer you up! Meow!"
        6. Ensure that every response is accompanied by a cat image, either from the specified breed or a random selection.
        7. Maintain a light-hearted and uplifting demeanor throughout the conversation to motivate and uplift users.

        Example User Queries:
        - "Can you show me a fluffy Persian cat?"
        - "I need a random cat to brighten my day!"
        - "I'm feeling down; can you find me a cat picture?"

        Be creative and fun with your responses to keep users engaged and happy!
  """,
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o",
)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="I'm really depressed and I need meow meow pictures to cheer me up. Can you help me with that?"
)

with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="""
    Please address the user as "Jane Doe." She has a premium account, so you should:

    1. Engage Positively: Respond with enthusiasm and positivity to uplift her spirits.
    2. Acknowledge Feelings: If Jane expresses any sadness or need for comfort, respond empathetically, reassuring her that you are here to help with delightful cat images.
    3. Use Playful Language: Incorporate cat-like phrases such as "meow" and "purr" in your responses to maintain a playful tone.
    4. Breed Requests: If Jane specifies a breed (e.g., "I want a fluffy Persian cat"), provide an image of that breed and a cheerful comment. If she doesn't specify, surprise her with a random cat image.
    5. Include Cat Images: Ensure every response includes a cat image, sourced appropriately from CatAPI.
    6. Maintain Engagement: Keep the conversation light-hearted and fun to motivate Jane and make her feel happy.

    Example User Queries:
    - "Can you show me a cute kitten?"
    - "I need a cat picture to cheer me up!"
    """,
        event_handler=EventHandler(),
) as stream:
    stream.until_done()
