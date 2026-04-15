# test

from google import genai

client = genai.Client(api_key="AIzaSyBp5XGXWTFJ4JFXQLUpasLYcoVhP8w5SyU")

response = client.models.generate_content(
    model="gemini-3-flash-preview", contents="Prompt here"
)
print(response.text)
