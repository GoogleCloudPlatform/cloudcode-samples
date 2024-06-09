import PyPDF2
import os

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        text = ''
        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            text += page.extractText()
    return text

def extract_texts_and_timecodes_from_folder(folder_path):
    data = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            text = extract_text_from_pdf(pdf_path)
            timecodes = extract_timecodes_from_pdf(pdf_path)  # Implement this function based on your PDF structure
            data.append({'filename': filename, 'content': text, 'timecodes': timecodes})
    return data

def extract_timecodes_from_pdf(pdf_path):
    # Placeholder for timecode extraction logic
    return []

if __name__ == "__main__":
    import sys
    folder_path = sys.argv[1]
    data = extract_texts_and_timecodes_from_folder(folder_path)
    for entry in data:
        print(f"Extracted from {entry['filename']}: {entry['content'][:100]}... Timecodes: {entry['timecodes']}")