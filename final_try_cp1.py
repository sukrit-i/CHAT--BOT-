import os
import streamlit as st
import google.generativeai as genai

from dotenv import load_dotenv
from PyPDF2 import PdfReader

# Load environment variables
load_dotenv()

# Configure generative AI model

GOOGLE_API_KEY='AIzaSyCT0JytzkhZrVa0g6tkZyt_MxJfzqDTqTM'
genai.configure(api_key=GOOGLE_API_KEY)

txt_model = genai.GenerativeModel('gemini-pro')

# Function to extract text from PDF
def read_pdf(file):
    pdf_reader = PdfReader(file)
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

def save_file(uploaded_file):
    """helper function to save documents to disk"""
    FILES_DIR = "C:\\Users\\Sukriti Sonam\\OneDrive\\Desktop\\sample pdf"
    file_path = os.path.join(FILES_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# Streamlit UI
def main():

    st.markdown(
        """
        <style>
        .stApp {
            background: url("https://img.freepik.com/free-vector/abstract-blurred-blue-background_1102-33.jpg?w=740&t=st=1721060792~exp=1721061392~hmac=d5782bcfefcce163b7239776f6303195856feea1b5c9236f73f93867626a6f26");
             background-size: cover;
            color: white;
        }
        .css-1d391kg, .css-1d391kg * {
            background-color: steelblue !important;
            color: white !important;
        }
        .css-18e3th9 {
            background-color: #FFFFFF !important;
        }
        
        </style>
        """,
        unsafe_allow_html=True
    )

    logo = 'logo.png'  # Replace with the path to your logo file
    st.sidebar.image(logo, width=150)

    logo = 'chatbot.png'  # Replace with the path to your logo file
    st.image(logo, width=150) 


    st.title("CHATBOT")


    with st.sidebar:
        new_title = '<p style="font-family:sans-serif; color:#FFFFFF; font-size: 51px;">PROV</p>'
        st.markdown(new_title, unsafe_allow_html=True)

        ##
        uploaded_files = st.file_uploader(
        "Upload PDFs for context", type=["PDF", "pdf"], accept_multiple_files=True
    )
    file_paths = []
    for uploaded_file in uploaded_files:
        file_paths.append(save_file(uploaded_file))

    if uploaded_files != []:
        st.write("Uploaded successfully!")
        st.subheader("Enter your query:")
        # query = st.text_input("")

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])    

        # Accept user input
        if prompt := st.chat_input("Ask me anything!"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                # Read PDF content
                pdf_text = read_pdf(uploaded_file)

                # Combine query and PDF text
                input_text = f"{prompt} {pdf_text}"
                response = txt_model.generate_content(input_text)
                extracted_text = response.candidates[0].content.parts[0].text

                print(extracted_text)
                response = st.write(extracted_text)  # Access content directly
            # st.session_state.messages.append({"role": "assistant", "content": answer.result[0]['content']})            


if __name__ == '__main__':
    main()