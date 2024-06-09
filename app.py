from dotenv import load_dotenv
import streamlit as st
import os
import fitz  # PyMuPDF

load_dotenv()  # take environment variables from .env.
# os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load OpenAI model and get responses
# No OpenAI model used in this code

def input_pdf_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()
        return bytes_data
    else:
        raise FileNotFoundError("No file uploaded")

def extract_chapters_from_pdf(uploaded_file):
    chapters = []
    if uploaded_file is not None:
        pdf_document = fitz.open(stream=uploaded_file)
        chapter_start = 0
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text = page.get_text()
            # Identify chapter divisions based on some criteria, for example, if the text contains "Chapter"
            if "Chapter" in text:
                chapter_end = page_num
                chapter_pdf = pdf_document.extract_subdocument(chapter_start, chapter_end)
                chapters.append(chapter_pdf)
                chapter_start = chapter_end
        # Append the last chapter
        if chapter_start < len(pdf_document):
            last_chapter_pdf = pdf_document.extract_subdocument(chapter_start, len(pdf_document))
            chapters.append(last_chapter_pdf)
        return chapters
    else:
        raise FileNotFoundError("No PDF file uploaded")

##initialize our streamlit app

st.set_page_config(page_title="PDF Chapter Splitter")

st.header("PDF Chapter Splitter")
uploaded_file = st.file_uploader("Choose a PDF file...", type=["pdf"])

if uploaded_file is not None:
    pdf_bytes = input_pdf_setup(uploaded_file)
    pdf_chapters = extract_chapters_from_pdf(pdf_bytes)

    st.write(f"Number of chapters detected: {len(pdf_chapters)}")

    for i, chapter_pdf in enumerate(pdf_chapters):
        st.write(f"Chapter {i+1}:")
        st.download_button(
            label="Download Chapter",
            data=chapter_pdf,
            file_name=f"chapter_{i+1}.pdf",
            mime="application/pdf"
        )
