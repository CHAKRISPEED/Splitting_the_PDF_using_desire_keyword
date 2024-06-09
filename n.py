import streamlit as st
import PyPDF2
import io

def extract_chapters_from_pdf(uploaded_file):
    chapters = []
    if uploaded_file is not None:
        pdf_reader = PyPDF2.PdfFileReader(uploaded_file)
        num_pages = pdf_reader.numPages

        chapter_start = 0
        for page_num in range(num_pages):
            page = pdf_reader.getPage(page_num)
            text = page.extractText()

            # Identify chapter divisions based on some criteria
            if "Chapter" in text:
                chapter_end = page_num
                chapter_pdf = PyPDF2.PdfFileWriter()
                for i in range(chapter_start, chapter_end):
                    chapter_pdf.addPage(pdf_reader.getPage(i))
                chapters.append(chapter_pdf)
                chapter_start = chapter_end
        
        # Append the last chapter
        if chapter_start < num_pages:
            last_chapter_pdf = PyPDF2.PdfFileWriter()
            for i in range(chapter_start, num_pages):
                last_chapter_pdf.addPage(pdf_reader.getPage(i))
            chapters.append(last_chapter_pdf)
        
        return chapters
    else:
        raise FileNotFoundError("No PDF file uploaded")

st.set_page_config(page_title="PDF Chapter Splitter")

st.header("PDF Chapter Splitter")
uploaded_file = st.file_uploader("Choose a PDF file...", type=["pdf"])

if uploaded_file is not None:
    pdf_bytes = io.BytesIO(uploaded_file.read())
    pdf_chapters = extract_chapters_from_pdf(pdf_bytes)

    st.write(f"Number of chapters detected: {len(pdf_chapters)}")

    for i, chapter_pdf in enumerate(pdf_chapters):
        st.write(f"Chapter {i+1}:")
        st.download_button(
            label="Download Chapter",
            data=io.BytesIO(),
            file_name=f"chapter_{i+1}.pdf",
            mime="application/pdf",
            key=i
        ).write(chapter_pdf)
