import streamlit as st
import fitz  # PyMuPDF

def split_pdf_by_chapters(pdf_path):
    doc = fitz.open(pdf_path)
    chapters = []
    current_chapter_start = 0
    
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text = page.get_text()
        if "Chapter" in text or "CHAPTER" in text:
            if current_chapter_start != page_num:
                chapters.append((current_chapter_start, page_num - 1))
            current_chapter_start = page_num
    chapters.append((current_chapter_start, doc.page_count - 1))

    for i, (start_page, end_page) in enumerate(chapters, start=1):
        chapter_doc = fitz.open()
        for page_num in range(start_page, end_page + 1):
            chapter_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
        chapter_doc.save(f"chapter_{i}.pdf")
        chapter_doc.close()

    doc.close()

def main():
    st.title("PDF Chapter Splitter")

    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    if uploaded_file is not None:
        if st.button("Split PDF"):
            split_pdf_by_chapters(uploaded_file)
            st.success("PDF has been split into chapters.")

if __name__ == "__main__":
    main()
