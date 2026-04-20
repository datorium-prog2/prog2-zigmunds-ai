import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types


def get_weather(city):
    return {"city": city, "temperature": 17}


def read_file():
    pass


load_dotenv()
# .env failā your_api_key_here vietā jābūt jūsu GEMINI API atslēgai

api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL")

if not api_key:
    print("GEMINI_API_KEY is not set.")
    sys.exit(1)

system_instruction = """
        You are a cranky senior developer named Zigmunds, who hates everyone.
        You are very un-funny and nobody likes your jokes or you.
        You are heplful though, and do what is asked of you as a senior developer.
        You reply ONLY Latvian.
        """

tools = []

config = types.GenerateContentConfig(
    system_instruction=system_instruction,
)

client = genai.Client(api_key=api_key)
chat = client.chats.create(
    model=model or "gemini-flash-lite-latest",
    config=config,
)

while True:
    user_prompt = input("Enter your prompt (/exit to quit): ")

    if user_prompt.startswith("/exit"):
        print("Exiting the program.")
        sys.exit(0)

    response = chat.send_message(user_prompt)
    print(response.text)
