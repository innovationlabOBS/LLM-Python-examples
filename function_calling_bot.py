import os
import json
import math
from datetime import datetime
import PySimpleGUI as sg
from gpt_api_call import gpt_api_call
from prompt_constructor import construct_prompt
from file_helper import extract_and_load_json

meta_prompts_path = "Function Calling Meta Prompts"
python_helper_fn_path = "Python Helper Functions"
logging_path = "Logs"

class FunctionCallingBot:
    def __init__(self):
        self.layout = [
            [sg.Text("Enter something: "), sg.InputText(key='-INPUT-')],  # Input field
            [sg.Button('Submit'), sg.Button('Exit')],  # Buttons
            [sg.Multiline(size=(40, 10), key='-MULTILINE-', autoscroll=True, disabled=True)]  # Multiline text box
        ]

        # Create the window
        self.window = sg.Window("Function Calling Bot", self.layout)

        self.log_filename = None
        self.create_log_file()

    def create_log_file(self):
        self.log_filename = f"function_calling_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        with open(f"{logging_path}/{self.log_filename}", "w", encoding="utf-8") as file:
            file.write("")

    def log(self,header, message):
        with open(f"{logging_path}/{self.log_filename}", "a", encoding="utf-8") as file:
            file.write(f"==============={header}================:\n\n {message}\n\n")

    def load_json_file(self, filename):
        with open(filename, "r") as file:
            return json.loads(file.read())
    
    def save_json_file(self, filename, data):
        with open(filename, "w") as file:
            file.write(json.dumps(data, indent=4))

    def load_python_fn_descriptions(self):
        json_list = os.listdir(python_helper_fn_path)
        desc_str = ""
        counter = 1
        for json_file in json_list:
            d = self.load_json_file(f"{python_helper_fn_path}/{json_file}")
            function_text = "FUNCTION NAME: " +  d["function_name"] + "   FUNCTION DESCRIPTION: " + d["function_description"]
            desc_str += str(counter) + ": " + function_text + "\n\n"
            counter += 1
        return desc_str

    def load_meta_prompt(self, filename):
        with open(f"{meta_prompts_path}/{filename}", "r") as file:
            return file.read()
        
    def gpt_call_check_fn_exists(self, user_query):
        desc_list_str = self.load_python_fn_descriptions()
        prompt = construct_prompt(meta_prompt=self.load_meta_prompt("find_existing_python_fn.txt"), replacement_array=[["<<USER_QUERY>>", user_query], ["<<DESCRIPTIONS_OF_FNS>>", desc_list_str]])
        self.log("GPT_CALL_CHECK_FN_EXISTS Prompt", prompt)
        response = gpt_api_call(prompt)
        self.log("GPT_CALL_CHECK_FN_EXISTS Response", response)

        return extract_and_load_json(response)
    
    def gpt_call_get_fn_params_from_user_input(self, user_query, fn_name):
        function_definition = self.load_json_file(f"{python_helper_fn_path}/{fn_name}.json")
        prompt = construct_prompt(meta_prompt=self.load_meta_prompt("get_user_params.txt"), replacement_array=[["<USER_QUERY>", user_query], ["<<FUNCTION_DEFINITION>>", json.dumps(function_definition)]])
        self.log("GPT_CALL_GET_FN_PARAMS_FROM_USER_INPUT Prompt", prompt)
        response = gpt_api_call(prompt)
        self.log("GPT_CALL_GET_FN_PARAMS_FROM_USER_INPUT Response", response)

        return extract_and_load_json(response)
    
    def gpt_call_convert_to_python(self, user_query):
        prompt = construct_prompt(meta_prompt=self.load_meta_prompt("create_python_fn.txt"), replacement_array=[["<<USER_QUERY>>", user_query]])
        self.log("GPT_CALL_CONVERT_TO_PYTHON Prompt", prompt)
        response = gpt_api_call(prompt)
        self.log("GPT_CALL_CONVERT_TO_PYTHON Response", response)

        return extract_and_load_json(response)
    
    def gpt_call_answer_user_query(self, user_query, correct_answer, fn_dict):
        prompt = construct_prompt(meta_prompt=self.load_meta_prompt("answer_user_query.txt"), replacement_array=[["<<USER_QUERY>>", user_query], ["<<FUNCTION_DEFINITION>>", json.dumps(fn_dict)], ["<<CORRECT_ANSWER>>", correct_answer]])
        self.log("GPT_CALL_ANSWER_USER_QUERY Prompt", prompt)
        response = gpt_api_call(prompt)
        self.log("GPT_CALL_ANSWER_USER_QUERY Response", response)

        return response
    
    def call_python_function(self, response_json):
        fn_desc = response_json["function_description"]
        input_params = response_json["input_param_names"]
        user_values = response_json["actual_input_values"]
        output_param = response_json["output_param_name"]
        code_body = response_json["code"]
        fn_name = response_json["function_name"]

        # Instantiate function
        exec(code_body)

        # Create function call string
        fn_call_str = f"{fn_name}({', '.join([str(i) for i in user_values])})"

        # Call the function
        result = eval(fn_call_str)
        return result
    
    def handle_gpt_call_sequence(self, user_query):
        response = self.gpt_call_check_fn_exists(user_query)

        fn_dict = None
        save_fn = False
        if response["function_exists"] == "YES":
            fn_dict = self.load_json_file(f"{python_helper_fn_path}/{response['function_name']}.json")
            user_input_params = self.gpt_call_get_fn_params_from_user_input(user_query, response["function_name"])
            fn_dict["actual_input_values"] = user_input_params["values_for_input_params"]
        else:
            save_fn = True
            fn_dict = self.gpt_call_convert_to_python(user_query)
            
        python_answer = self.call_python_function(fn_dict)
        final_answer = self.gpt_call_answer_user_query(user_query, python_answer, fn_dict)

        if save_fn:
            del fn_dict['actual_input_values']
            self.save_json_file(f"{python_helper_fn_path}/{fn_dict['function_name']}.json", fn_dict)

        return final_answer
        

    def run(self):
        while True:
            event, values = self.window.read()
            
            # If user closes window or clicks 'Exit'
            if event == sg.WINDOW_CLOSED or event == 'Exit':
                break
            # If user clicks 'Submit'
            elif event == 'Submit':
                # Get the input text
                input_text = values['-INPUT-']
                # Append the input text to the multiline text box using the append parameter
                self.window['-MULTILINE-'].update("USER:" + input_text + '\n', append=True)
                # Optionally, clear the input field after appending
                self.window['-INPUT-'].update('')
                self.log("User Input", input_text)

                response = self.handle_gpt_call_sequence(input_text)

                self.window['-MULTILINE-'].update("ASSISTANT:" + response + '\n', append=True)
        # Close the window
        self.window.close()

if __name__ == "__main__":
    bot = FunctionCallingBot()
    bot.run()