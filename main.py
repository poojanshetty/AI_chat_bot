import subprocess
import os
import openai
from config import apikey
openai.api_key = apikey

def run_text_chat():
    """Run the AI Text Chat bot."""
    script_path = os.path.join(os.getcwd(), 'AI_text_chat_bot.py')
    subprocess.run(['python3', script_path])

def run_voice_chat():
    """Run the AI Voice Chat bot."""
    script_path = os.path.join(os.getcwd(), 'Ai_Voice_chat_bot.py')
    subprocess.run(['python3', script_path])

def chat_with_gpt3(prompt):
    """Chat with GPT-3 using OpenAI API."""
    try:
        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            prompt=prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response['choices'][0]['text']
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    """Main function to prompt user for selection."""
    print("Welcome to the AI Bot Hub!")
    print("Please select the bot you would like to run:")
    print("1. AI Text Chat Bot")
    print("2. AI Voice Chat Bot")

    choice = input("Enter the number (1 or 2) of your selection: ")

    if choice == '1':
        print("Launching AI Text Chat Bot...")
        run_text_chat()
    elif choice == '2':
        print("Launching AI Voice Chat Bot...")
        run_voice_chat()
    else:
        print("Invalid selection. Please enter 1 or 2.")

if __name__ == '__main__':
    main()