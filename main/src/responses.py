from revChatGPT.Official import AsyncChatbot
from dotenv import load_dotenv
import os
import requests

load_dotenv()
openAI_key = os.getenv("OPENAI_KEY")
openAI_model = os.getenv("ENGINE")
weather_key = os.getenv("WEATHER_KEY")
youtube_key = os.getenv("YOUTUBE_KEY")
chatbot = AsyncChatbot(api_key=openAI_key, engine=openAI_model)

async def handle_response(message) -> str:
    response = await chatbot.ask(message)
    responseMessage = response["choices"][0]["text"]
    return responseMessage

def get_weather(message):
  response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={message}&units=metric&appid={weather_key}")
  response = response.json()
  return response

def get_music(message):
  response = requests.get(f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&q={message}&type=video&maxResults=1&key={youtube_key}") 
  response = response.json()
  return response

# def get_todo_list(message):
def get_todo_list():
  # response = requests.get(f"url{message.user.id}")
  response = requests.get(f"https://643a539490cd4ba563f71100.mockapi.io/todo")
  response = response.json()
  return response