from googlesearch import search
import requests
from bs4 import BeautifulSoup
from file_helper import save_file

def fetch_page_paragraphs(url):
    try:
        # Fetch the content of the URL
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        p_text_concat = ""
        paragraphs = soup.find_all('p')
        for p in paragraphs:
            if p:
                p_text_concat += p.get_text() + "\n\n"

        return p_text_concat
    except Exception as e:
        return "Failed to fetch page content", str(e)

def fetch_page_html(url):
    try:
        # Fetch the content of the URL
        response = requests.get(url)
        html_content = response.text
        return html_content
    except Exception as e:
        return f"Failed to fetch page content: {str(e)}"
    
def get_content_from_key_words(file_path, keywords, n = 50):

    keywords = [keyword.lower() for keyword in keywords]
    # Read the content of the file
    with open(file_path, 'r', encoding = "utf-8") as file:
        text = file.read()
    
    # Split the text into words
    words = text.lower().split()
    
    # Prepare a set to keep track of indices of words already grabbed
    grabbed_indices = set()
    
    # Prepare a list to collect the words around keywords
    words_around_keywords = []
    
    # Iterate through each word in the text
    for i, word in enumerate(words):
        # Check if the word is a keyword and not already grabbed
        if word in keywords and i not in grabbed_indices:
            # Calculate the range of indices to grab
            start = max(0, i - n)
            end = min(len(words), i + n + 1)
            
            # Iterate through the range and collect words if not already grabbed
            for j in range(start, end):
                if j not in grabbed_indices:
                    words_around_keywords.append(words[j])
                    grabbed_indices.add(j)
    
    return words_around_keywords

if __name__ == "__main__":
    """
    post_fix = "wikipedia"

    query = "mass of jupiter" + post_fix

    for url in search(query, num_results=1):
        print(url)
        text = fetch_page_paragraphs(url)
        save_file("jupiter.txt", text)
        break

    key_words = ["mass"]

    words = get_content_from_key_words("jupiter.txt", key_words, n = 50)

    save_file("mass_of_jupiter.txt", " ".join(words))
    """
    key_words = ["mass"]

    words = get_content_from_key_words("jupiter.txt", key_words, n = 50)
    save_file("mass_of_jupiter.txt", " ".join(words))