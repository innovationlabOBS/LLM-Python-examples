# LLM-Python-Examples

This repository contains examples on how to use the OpenAI API with Python. It's designed to help you get started with integrating OpenAI's powerful language models into your Python projects.

## Setup

To get started with these examples, follow the steps below to set up your local environment.

### 1. Clone the repo

   Clone this repository to your local machine using the following command:

   ```
   git clone https://github.com/innovationlabOBS/LLM-Python-examples.git
   ```

### 2. Create a Python Virtual Environment

First, create a local Python virtual environment to manage your project's dependencies separately from your global Python installation. Open your terminal and run:

```bash
python -m venv venv
```

This command creates a new directory named `venv` where the virtual environment files will be stored.

### 3. Activate the Virtual Environment

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

### 4. Install Dependencies

With the virtual environment activated, install the project dependencies by running:

```bash
pip install -r requirements.txt
```

This command reads the `requirements.txt` file and installs all the listed packages along with their dependencies.

### 5. Set Up Your OpenAI API Key

To use the OpenAI API, you need an API key. Create a file named `.env` in the root directory of the project and add your OpenAI API key as follows:

```plaintext
OPENAI_API_KEY='put your openai api key here'
```

Replace `'put your openai api key here'` with your actual OpenAI API key.
