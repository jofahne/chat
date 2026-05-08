from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr
import os

load_dotenv(override=True)
openai_api_key = os.getenv("OPENAI_API_KEY")

openai = OpenAI()
model = "gpt-4o-mini"


def echo(message, history):

    system_message = """
                    You are a helpful and precise assistant for a store that sells high performance sailing products.
                    """
    if "winch" in message.lower():
        system_message += " The store is having a sale on winches, with discounts up to 50% until the end of the month."
    
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]

    stream = openai.chat.completions.create(model=model, messages=messages, stream=True)

    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content or ""
        yield response


if __name__ == "__main__":
    gr.ChatInterface(fn=echo).launch()