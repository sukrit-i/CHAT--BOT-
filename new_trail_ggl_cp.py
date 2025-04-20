import os
import streamlit as st
import google.generativeai as genai

from dotenv import load_dotenv
from PyPDF2 import PdfReader

load_dotenv()

# Configure generative AI model
GOOGLE_API_KEY='AIzaSyCT0JytzkhZrVa0g6tkZyt_MxJfzqDTqTM'
genai.configure(api_key=GOOGLE_API_KEY)
txt_model = genai.GenerativeModel('gemini-pro')

# Function to extract text from PDF
def read_pdf(file):
    if file.type == "application/pdf":  # Validate file type
        pdf_reader = PdfReader(file)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        return text
    else:
        st.error("Please upload a PDF file.")
        return None

# Function to add to history
def add_to_history(query, response):
    st.session_state.history.append({"query": query, "response": response})

# Streamlit UI with memory and dynamic conversation flow
def main():
    st.set_page_config(page_title="PDF Chatbot", page_icon=":book:")  # Set title and icon
    
    logo = 'logo.png'  # Replace with the path to your logo file
    st.sidebar.image(logo, width=70)

    logo = 'chatbot.png'  # Replace with the path to your logo file
    st.image(logo, width=70) 

    st.title("PDF Chatbot")

    # Initialize session state
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'pdf_text' not in st.session_state:
        st.session_state.pdf_text = ""

    # Sidebar for PDF upload
    with st.sidebar:
        st.subheader("PROV")
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    # Main conversation area
    with st.container():
        if uploaded_file is not None:
            st.write("Uploaded successfully!")
            # Read PDF content
            pdf_text = read_pdf(uploaded_file)
            st.session_state.pdf_text = pdf_text  # Store PDF text in session state

            # Display conversation history
            if st.session_state.history:
                st.subheader("Conversation:")
                for entry in st.session_state.history:
                    st.write(f"**User:** {entry['query']}")
                    st.write(f"**Chatbot:** {entry['response']}")
                    st.write("")

            # Query input area and button
            # **Key Change:** The prompt will now appear after the chatbot's response.
            if 'query' in st.session_state:
                if st.session_state.query:
                    with st.spinner("Thinking..."):  # Show loading indicator
                        try:
                            # **Key Change:** Improved conversational prompt
                            response = txt_model.generate_content(
                                f"""I have read the following document:

{st.session_state.pdf_text}

Now, please answer this question:

{st.session_state.query}
                                """
                            )

                            # Display response
                            st.write(f"**Chatbot:** {response.text}")

                            # Add to history
                            add_to_history(st.session_state.query, response.text)

                            # Reset query input field
                            st.session_state.query = "" 

                        except Exception as e:
                            st.error(f"An error occurred: {e}")  # Handle errors

            # Clear the previous question
            st.session_state.query = ''  

            st.subheader("Ask me anything about the document:")
            st.session_state.query = st.text_input("")

if __name__ == '__main__':
    main()