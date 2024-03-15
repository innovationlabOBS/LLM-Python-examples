import json
from file_helper import extract_and_load_json
from gpt_api_call import gpt_api_call

script_filename = "self_modifying_code.py"
meta_prompts_path = "SMC Meta Prompts"

class SelfModifyingCode:
    def __init__(self):
        pass

    def load_text_file(self, filename):
        with open(filename, "r") as file:
            return file.read()
        
    def save_text_file(self, filename, data):
        with open(filename, "w") as file:
            file.write(data)
    
    def modify_self(self):
        code = self.load_text_file(script_filename)
        prompt = self.load_text_file(f"{meta_prompts_path}/find_improvements.txt")
        prompt = prompt.replace("<<PYTHON_CODE>>", code)
        response = gpt_api_call(prompt)
        self.save_text_file(script_filename, extract_and_load_json(response)["complete_rewritten_code"])

    def run(self):
        prompt = "how are you doing today?"
        response = gpt_api_call(prompt)
        print(response)

        self.modify_self()
        

if __name__ == "__main__":
    smc = SelfModifyingCode()
    smc.run()