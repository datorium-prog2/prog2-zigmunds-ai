import os
import sys

from dotenv import load_dotenv
from google import genai

load_dotenv()
# .env failā your_api_key_here vietā jābūt jūsu GEMINI API atslēgai

api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL")

if not api_key:
    print("GEMINI_API_KEY is not set.")
    sys.exit(1)

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model=model or "gemini-flash-lite-latest", contents="Čau! Kā tev iet?"
)
print(response.text)
