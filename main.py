import os

from dotenv import load_dotenv

load_dotenv()
# .env failā your_api_key_here vietā jābūt jūsu GEMINI API atslēgai

api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL")

print(model)
