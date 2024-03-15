import re
import json

def load_file(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        return file.read()
    
def save_json(file_path, data):
    with open(file_path, 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def save_file(file_path, data):
    with open(file_path, 'w', encoding="utf-8") as file:
        file.write(data)

def extract_and_load_json(json_str):
    # Regular expression to find the JSON
    # This pattern assumes the JSON object starts with '{' and ends with '}'
    # or it starts with '[' and ends with ']', without checking the validity of the content in between.
    # This is a simplistic approach and might need adjustments based on actual content.
    pattern = r'{.*}|[.*]'
    match = re.search(pattern, json_str, re.DOTALL)
    
    if match:
        try:
            # Extract the matched JSON string
            valid_json_str = match.group(0)
            # Parse the JSON string
            return json.loads(valid_json_str)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
    else:
        print("No valid JSON found in the string.")
        return None