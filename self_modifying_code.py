import json
import logging
from file_helper import extract_and_load_json
from gpt_api_call import gpt_api_call

script_filename = "self_modifying_code.py"
meta_prompts_path = "SMC Meta Prompts"

logging.basicConfig(filename='conversation_log.txt', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

class SelfModifyingCode:
    def __init__(self):
        self.conversation_history = []

    def load_text_file(self, filename):
        try:
            with open(filename, "r") as file:
                return file.read()
        except Exception as e:
            logging.error(f"Error reading {filename}: {e}")
            return None
    
    def save_text_file(self, filename, data):
        try:
            with open(filename, "w") as file:
                file.write(data)
        except Exception as e:
            logging.error(f"Error writing to {filename}: {e}")
    
    def modify_self(self):
        code = self.load_text_file(script_filename)
        if code is None: return
        prompt = self.load_text_file(f"{meta_prompts_path}/find_improvements.txt")
        if prompt is None: return
        prompt = prompt.replace("<<PYTHON_CODE>>", code)
        response = gpt_api_call(prompt)
        self.save_text_file(script_filename, extract_and_load_json(response)["complete_rewritten_code"])

    def run(self):
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'quit':
                break
            self.conversation_history.append(f"You: {user_input}")
            try:
                response = gpt_api_call(user_input)
                print(f"AI: {response}")
                self.conversation_history.append(f"AI: {response}")
                logging.info(f"Conversation: {self.conversation_history[-2]}, {self.conversation_history[-1]}")
            except Exception as e:
                logging.error(f"Error during API call: {e}")
                print("Sorry, I couldn't process that. Let's try something else.")

        self.modify_self()
        

if __name__ == "__main__":
    smc = SelfModifyingCode()
    smc.run()
