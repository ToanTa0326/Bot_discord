from revChatGPT.Official import AsyncChatbot
from dotenv import load_dotenv
import os
import requests

load_dotenv()
openAI_key = os.getenv("OPENAI_KEY")
openAI_model = os.getenv("ENGINE")
weather_key = os.getenv("WEATHER_KEY")
youtube_key = os.getenv("YOUTUBE_KEY")
todo_url = os.getenv("TEST_TODO_URL")
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

def get_todo_list(params):
  response = requests.get(todo_url, params)
  response = response.json()
  return response

def create_todo(data):
  response = requests.post(todo_url, data)
  response = response.json()
  return response

def edit_todo(data):
  response = requests.put(todo_url, data)
  response = response.json()
  return response

def delete_todo(params):
  response = requests.delete(todo_url, params)
  response = response.json()
  return response
