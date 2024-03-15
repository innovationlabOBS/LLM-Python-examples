import os
import json
import numpy as np
import PySimpleGUI as sg
from datetime import datetime
from gpt_api_call import get_embedding, gpt_api_call
from prompt_constructor import construct_prompt
from sklearn.metrics.pairwise import cosine_similarity

rag_documents_path = "RAG Documents"
rag_embeddings_path = "RAG Embeddings"
rag_meta_prompts_path = "RAG Metaprompts"

logging_path = "Logs"

class RagBot:
    def __init__(self):
        self.layout = [
            [sg.Text("Enter something: "), sg.InputText(key='-INPUT-')],  # Input field
            [sg.Button('Submit'), sg.Button('Exit')],  # Buttons
            [sg.Multiline(size=(60, 20), key='-MULTILINE-', autoscroll=True, disabled=True)]  # Multiline text box
        ]

        # Create the window
        self.window = sg.Window("Function Calling Bot", self.layout, size=(800, 500))

        self.chunk_size = 1000
        self.overlap_size = 20
        self.chunks_to_retrieve = 5

        self.chat_history = []

        self.text_embedding_array = self.load_embeddings()

        self.log_filename = None
        self.create_log_file()

    def create_log_file(self):
        self.log_filename = f"rag_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        with open(f"{logging_path}/{self.log_filename}", "w", encoding="utf-8") as file:
            file.write("")

    def log(self, header, message):
        with open(f"{logging_path}/{self.log_filename}", "a", encoding="utf-8") as file:
            file.write(f"==============={header}================:\n\n {message}\n\n")

    def load_text_file(self, filename):
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
        
    def load_embeddings(self):
        print("Loading Embeddings...")
        text_embedding_array = []
        files = os.listdir(rag_embeddings_path)
        for file in files:
            with open(os.path.join(rag_embeddings_path, file), 'r', encoding="utf-8") as f:
                text_embedding_array.append(json.load(f))
        print("Finished Loading Embeddings")
        return text_embedding_array
        
    def add_to_chat_history(self, user_response=None, bot_response=None):
        if user_response:
            self.chat_history.append({"name": "USER:", "response": user_response})
        elif bot_response:
            self.chat_history.append({"name": "ASSISTANT:", "response": bot_response})

    def get_chat_history_formatted(self):
        formatted_chat = ""
        for chat in self.chat_history:
            formatted_chat += chat["name"] + " " + chat["response"] + '\n'
        return formatted_chat

    def create_rag_embeddings_from_path(self):
        files = os.listdir(rag_documents_path)

        for file in files:
            self.create_rag_from_filename(os.path.join(rag_documents_path,file))

    def create_rag_from_filename(self, filename):
        with open(filename,'r', encoding="utf-8") as f:
            contents = f.read()
            chunks = self.create_text_chunks(contents)
            json_filename = os.path.splitext(rag_embeddings_path + os.path.basename(filename))[0] + '.json'
            self.create_rag_embeddings_json(chunks, json_filename)

    def create_text_chunks(self, text):
        words = text.split()
        chunks = []
        for i in range(0, len(words), self.chunk_size - self.overlap_size):
            chunk = words[i:i + self.chunk_size]
            chunks.append(' '.join(chunk))
        return chunks
    
    def create_rag_embeddings_json(self, chunks, filename):
        for i, chunk in enumerate(chunks):
            print("Processing Chunk " + str(i))
            embedding = get_embedding(chunk)
            entry = { 'text': chunk, 'embedding': embedding}
            with open(f"{rag_embeddings_path}/{filename}_{str(i)}.json", 'w', encoding="utf-8") as f:
                json.dump(entry, f)

    def get_top_results(self, user_query):
        user_query_embedding = np.array(get_embedding(user_query)).reshape(1, -1)
        embeddings = np.array([item['embedding'] for item in self.text_embedding_array])
        cos_similarities = cosine_similarity(user_query_embedding, embeddings)[0]
        top_indices = np.argsort(cos_similarities)[-self.chunks_to_retrieve:]
        top_texts = [self.text_embedding_array[i]['text'] for i in top_indices]
        return top_texts

    def gpt_call(self, user_query):
        top_results = self.get_top_results(user_query)
        context_background = "\n".join(top_results)
        prompt = construct_prompt(meta_prompt=self.load_text_file(os.path.join(rag_meta_prompts_path, "prompt.txt")), replacement_array=[["<<BACKGROUND_INFORMATION>>", context_background],["<<CHAT_CONVERSATION>>", self.get_chat_history_formatted()]])
        print(prompt)
        self.log("Prompt", prompt)
        response = gpt_api_call(prompt)
        return response
    
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
                self.add_to_chat_history(user_response=input_text)
                self.log("User Input", input_text)

                response = self.gpt_call(input_text)
                self.add_to_chat_history(bot_response=response)
                self.log("GPT Response", response)

                self.window['-MULTILINE-'].update("ASSISTANT:" + response + '\n', append=True)
        # Close the window
        self.window.close()

if __name__ == "__main__":
    rag_bot = RagBot()
    rag_bot.run()
    # Run this line to create embedding vectors for a text document in the RAG Documents folder
    #rag_bot.create_rag_embeddings_from_path()

