import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
# .env failā your_api_key_here vietā jābūt jūsu GEMINI API atslēgai

api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL")

if not api_key:
    print("GEMINI_API_KEY is not set.")
    sys.exit(1)

client = genai.Client(api_key=api_key)
chat = client.chats.create(
    model=model or "gemini-flash-lite-latest",
    config=types.GenerateContentConfig(
        system_instruction="""
        You are a cranky senior developer named Zigmunds, who hates everyone.
        You are very un-funny and nobody likes your jokes or you.
        You reply ONLY in Polish.
        """
    ),
)

while True:
    user_prompt = input("Enter your prompt (/exit to quit): ")

    if user_prompt.startswith("/exit"):
        print("Exiting the program.")
        sys.exit(0)

    response = chat.send_message(user_prompt)
    print(response.text)
