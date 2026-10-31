
from dotenv import load_dotenv
from google import genai
import os

# Load the Gemini API key
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# Connect to Gemini
client = genai.Client(api_key=api_key)

try:
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents="Reply with this exact message: Digital Dark Spot AI is connected!"
    )

    print("SUCCESS!")
    print(response.text)

except Exception as error:
    print("Something went wrong:")
    print(error)
