def construct_prompt(meta_prompt, replacement_array):
    prompt = meta_prompt
    for r in replacement_array:
        prompt = prompt.replace(r[0], str(r[1]))

    return prompt