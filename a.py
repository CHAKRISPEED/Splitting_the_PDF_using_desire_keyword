import streamlit as st
import PyPDF2

def split_pdf_by_chapters(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        num_pages = pdf_reader.numPages
        chapters = []
        chapter_start = 0
        for page_num in range(num_pages):
            page = pdf_reader.getPage(page_num)
            text = page.extractText()
            if 'Chapter' in text:
                if chapter_start < page_num:
                    chapters.append((chapter_start, page_num))
                chapter_start = page_num

        # Add the last chapter
        chapters.append((chapter_start, num_pages))

        return chapters

def save_chapter_as_pdf(pdf_path, output_path, chapter_range):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        pdf_writer = PyPDF2.PdfFileWriter()
        for page_num in range(chapter_range[0], chapter_range[1]):
            pdf_writer.addPage(pdf_reader.getPage(page_num))

        with open(output_path, 'wb') as output_file:
            pdf_writer.write(output_file)

def main():
    st.title("PDF Chapter Splitter")

    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

    if uploaded_file is not None:
        st.write("PDF Uploaded!")

        chapters = split_pdf_by_chapters(uploaded_file)

        st.write(f"Detected {len(chapters)} chapters")

        for i, chapter_range in enumerate(chapters):
            chapter_start, chapter_end = chapter_range
            st.write(f"Chapter {i+1}: Pages {chapter_start+1}-{chapter_end}")

            if st.button(f"Save Chapter {i+1}"):
                output_path = f"chapter_{i+1}.pdf"
                save_chapter_as_pdf(uploaded_file.name, output_path, chapter_range)
                st.write(f"Chapter {i+1} saved as {output_path}")

if __name__ == "__main__":
    main()
