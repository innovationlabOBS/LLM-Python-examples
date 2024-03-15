import json
import datetime
import wikipedia
from file_helper import load_file
from gpt_api_call import gpt_api_call
from prompt_constructor import construct_prompt

wiki_meta_prompt_filename = "Meta Prompts/extract_info_to_lookup.txt"

LIST_OF_SEARCHES = "list_of_searches"

class Bots:
    def __init__(self):
        self.wiki_meta_prompt = load_file(wiki_meta_prompt_filename)
        self.current_year = datetime.datetime.now().year

    def gpt_wiki_search(self, query):
        prompt = construct_prompt(meta_prompt=self.wiki_meta_prompt, replacement_array=[["<USER_QUERY>", query,], ["<CURRENT_YEAR>", str(self.current_year)]])
        response = gpt_api_call(prompt)
        list_of_wiki_searches = json.loads(response)[LIST_OF_SEARCHES]
        context = ""
        for search in list_of_wiki_searches:
            context += wikipedia.summary(search) + "\n\n"

        return context
    
    