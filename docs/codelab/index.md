# Mesop DuoChat Codelab

This tutorial walks you through building DuoChat, an interactive web application for chatting with multiple AI models simultaneously. You'll learn how to leverage Mesop's powerful features to create a responsive UI and integrate with AI APIs like Google Gemini and Anthropic Claude.

### What is Mesop?

Mesop is a Python-based UI framework designed to simplify web UI development for engineers without frontend experience. It leverages the power of the Angular web framework and Angular Material components, allowing rapid construction of web demos and internal tools.

### Project Overview

DuoChat will allow users to:
- Chat with multiple AI models (Gemini and Claude) in parallel
- Compare responses from different models side-by-side
- Provide their own API keys
- Use a responsive and intuitive user interface

### Setting Up the Development Environment

Let's start by setting up our development environment:

1. Create a new directory for your project:

```bash
mkdir duochat
cd duochat
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Create a `requirements.txt` file with the following content:

```
mesop
gunicorn
anthropic
google-generativeai
```

4. Install the dependencies:

```bash
pip install -r requirements.txt
```

### Project Structure

Create the following files in your project directory:

```
duochat/
├── main.py
├── data_model.py
├── dialog.py
├── claude.py
├── gemini.py
├── requirements.txt
```

We'll populate these files as we progress through the codelab.

### Setting Up the Main Application

Let's start by creating a basic Mesop application. Open `main.py` and add the following code:

```python
import mesop as me

@me.page(path="/")
def page():
    me.text("Welcome to DuoChat!")

if __name__ == "__main__":
    me.run()
```

This creates a simple Mesop application with a single page that displays a welcome message.

### Running the Application

To run your Mesop application:

```bash
mesop main.py
```

Navigate to `http://localhost:32123` in your web browser. You should see the welcome message.

### Next Steps

In the next section, we'll start building the user interface for DuoChat, including the header, chat input area, and basic styling. We'll explore Mesop's components and styling system to create an attractive and functional layout.
