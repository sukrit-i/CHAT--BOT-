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


# genai.configure(api_key='ggl_api_key')
# genai.configure(api_key=os.environ["ggl_api_key"])
txt_model = genai.GenerativeModel('gemini-pro')

# Function to extract text from PDF
def read_pdf(file):
    pdf_reader = PdfReader(file)
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

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
            background-color: babyblue !important;
        }
        
        </style>
        """,
        unsafe_allow_html=True
    )

    logo = 'logo.png'  # Replace with the path to your logo file
    st.sidebar.image(logo, width=70)

    logo = 'chatbot.png'  # Replace with the path to your logo file
    st.image(logo, width=70) 


    st.title("CHATBOT")

       # Two-column layout
    # col1, col2 = st.beta_columns([1, 3])  # Adjust the width ratio as needed
    # Create a two-column layout
    # left_column, right_column = st.columns([2, 1])

    # File uploader
    # st.header("Upload a PDF Document")
    # uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    with st.sidebar:
     st.subheader("PROV")
     uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    #  uploaded_file = st.file_uploader("Uploaded PDF Files",accept_multiple_files=True)

    if uploaded_file is not None:
        st.write("Uploaded successfully!")
        st.subheader("Enter your query:")
        query = st.text_input("")

        # Button to generate response
        if st.button("Generate Response"):
            # Read PDF content
            pdf_text = read_pdf(uploaded_file)

            # Combine query and PDF text
            input_text = f"{query} {pdf_text}"

            # Generate response from model
            response = txt_model.generate_content(input_text)

            # Display response
            st.subheader("Response:")
            st.write(response.text)
            st.write("Feel free to ask more questions or upload another document!")


if __name__ == '__main__':
    main()
