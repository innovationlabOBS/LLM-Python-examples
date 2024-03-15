import os
import sys
import json
from gpt_api_call import gpt_api_call, get_embedding, cosine_similarity
from file_helper import load_file, save_json
from prompt_constructor import construct_prompt

def create_fns_from_names():
    physics_functions_path = "Physics Functions"

    physics_fn_names = json.loads(load_file("physics_fn_names.json"))["physics_fn_names"]

    for fn_name in physics_fn_names:
        prompt = construct_prompt(meta_prompt=load_file("Meta Prompts/create_fn_from_name.txt"), replacement_array=[["<FN_NAME>", fn_name]])
        response = gpt_api_call(prompt)

        with open(f"{physics_functions_path}/{fn_name}.json", "w") as file:
            file.write(response)

def create_fn_embeddings():
    physics_functions_path = "Physics Functions"

    physics_fn_filenames = os.listdir(physics_functions_path)

    for fn_filename in physics_fn_filenames:
        fn_json = json.loads(load_file(f"{physics_functions_path}/{fn_filename}"))
        description = fn_json["description"]
        embedding_vec = get_embedding(description)
        fn_json["embedding"] = embedding_vec
        save_json(f"{physics_functions_path}/{fn_filename}", fn_json)
        print(f"Saved embedding for {fn_filename}")