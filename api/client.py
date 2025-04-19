import requests
import streamlit as st

def get_openai_response(input_text):
    response = requests.post(
        "http://localhost:8000/essay/invoke",
        json={'input': {'topic': input_text}}
    )
    # First try the expected structure, if it fails, try alternative structures
    try:
        return response.json()['output']['content']
    except (KeyError, TypeError):
        # If the above fails, try accessing the content directly
        return response.json().get('content', str(response.json()))

def get_ollama_response(input_text):
    try:
        response = requests.post(
            "http://localhost:8000/poem/invoke",
            json={'input': {'topic': input_text}}
        )
        response.raise_for_status()
        
        data = response.json()
        
        # Extract just the poem content
        if 'output' in data:
            # Split by newlines and remove the first line if it's a description
            poem_lines = data['output'].split('\n')
            if "Here is a" in poem_lines[0] or "poem about" in poem_lines[0]:
                return '\n'.join(poem_lines[1:])  # Skip the first line
            return data['output']  # Return full output if no description line
        return str(data)  # Fallback if no output found
        
    except requests.exceptions.RequestException as e:
        return f"API request failed: {str(e)}"
    except ValueError as e:
        return f"Invalid JSON response: {response.text}"

## streamlit framework

st.title('Langchain Demo with LLAMA3 API')
input_text = st.text_input("Write an essay on")
input_text1 = st.text_input("Write a poem on")

if input_text:
    st.write(get_openai_response(input_text))

if input_text1:
    st.write(get_ollama_response(input_text1))