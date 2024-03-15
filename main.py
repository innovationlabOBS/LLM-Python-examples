from processing import create_fns_from_names, create_fn_embeddings
from bots import Bots
from googlesearch import search
import requests
from bs4 import BeautifulSoup
from file_helper import save_file
    
def main():
    bots = Bots()
    bots.gpt_wiki_search("What is the mass of jupiter? Also, how far away is the nearest star, and who is the current president of the US?")
    
if __name__ == "__main__":
    main()