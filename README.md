# LLM-Python-Examples

This repository contains examples on how to use the OpenAI API with Python. It's designed to help you get started with integrating OpenAI's powerful language models into your Python projects.

## Setup

To get started with these examples, follow the steps below to set up your local environment.

### 1. Create a Python Virtual Environment

First, create a local Python virtual environment to manage your project's dependencies separately from your global Python installation. Open your terminal and run:

```bash
python -m venv venv
```

This command creates a new directory named `venv` where the virtual environment files will be stored.

### 2. Activate the Virtual Environment

Before installing the project dependencies, you need to activate the virtual environment. Depending on your operating system, run one of the following commands:

- **On Windows:**

```cmd
venv\Scripts\activate
```

- **On macOS and Linux:**

```bash
source venv/bin/activate
```

You should now see the name of your virtual environment (`venv`) at the beginning of the terminal prompt, indicating that the virtual environment is active.

### 3. Install Dependencies

With the virtual environment activated, install the project dependencies by running:

```bash
pip install -r requirements.txt
```

This command reads the `requirements.txt` file and installs all the listed packages along with their dependencies.

### 4. Set Up Your OpenAI API Key

To use the OpenAI API, you need an API key. Create a file named `.env` in the root directory of the project and add your OpenAI API key as follows:

```plaintext
OPENAI_API_KEY='put your openai api key here'
```

Replace `'put your openai api key here'` with your actual OpenAI API key.

# Function Calling Bot

The Function Calling Bot is a Python application designed to assist users in calling Python functions dynamically based on user input. It leverages GPT (Generative Pre-trained Transformer) models to interpret user queries, determine if a corresponding Python function exists, and either call the existing function or generate a new one. This document provides a comprehensive guide on how to set up and use the Function Calling Bot.

## Features

- **Dynamic Function Interpretation:** Interprets user queries to identify or generate the appropriate Python function.
- **Function Execution:** Executes Python functions dynamically based on user input.
- **Logging:** Maintains detailed logs of user queries and system responses for debugging and analysis.
- **GPT Integration:** Utilizes GPT models to interpret user queries and generate Python code when necessary.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher installed on your system.
- PySimpleGUI installed for the GUI interface. Install it using `pip install PySimpleGUI`.
- Access to GPT API for interpreting user queries and generating Python code. Ensure you have the necessary API keys and permissions set up.

## Installation

1. **Clone the Repository:**

   Clone this repository to your local machine using the following command:

   ```
   git clone https://github.com/your-username/function-calling-bot.git
   ```

2. **Install Dependencies:**

   Navigate to the cloned repository directory and install the required Python packages using:

   ```
   pip install -r requirements.txt
   ```

3. **Set Up GPT API Credentials:**

   Ensure you have your GPT API credentials ready. You will need to modify the `gpt_api_call` function in the script to include your API key and any necessary configuration.

## Usage

To use the Function Calling Bot, follow these steps:

1. **Start the Application:**

   Run the Python script to start the application:

   ```
   python function_calling_bot.py
   ```

2. **Enter a Query:**

   Once the application window opens, enter a query in the input field. Your query should describe the function you want to call or the task you want to accomplish. For example, "calculate the square root of 16".

3. **Submit the Query:**

   Click the 'Submit' button to process your query. The bot will interpret your query, determine the appropriate Python function to call, and display the result in the text box below.

4. **View Logs (Optional):**

   The application generates logs for each session, which are stored in the `Logs` directory. You can review these logs to understand how the bot processed your queries.

## Customizing the Bot

- **Adding New Python Functions:** To add new Python functions, create a JSON file in the `Python Helper Functions` directory with the function's metadata and code. The bot will automatically recognize these new functions.
- **Modifying GPT Prompts:** You can modify the GPT prompts used for interpreting user queries by editing the files in the `Function Calling Meta Prompts` directory.

## Contributing

Contributions to the Function Calling Bot are welcome. Please feel free to fork the repository, make changes, and submit pull requests.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

If you have any questions or feedback, please contact the project maintainer at your-email@example.com.

---

Enjoy using the Function Calling Bot to dynamically call Python functions based on user input!
