import streamlit as st
import PyPDF2
import os
import pandas as pd
from sqlalchemy import create_engine

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        text = ''
        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            text += page.extractText()
    return text

def extract_texts_from_folder(folder_path):
    data = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            text = extract_text_from_pdf(pdf_path)
            data.append({'filename': filename, 'content': text})
    return data

def create_database(data, db_name='my_database.db'):
    engine = create_engine(f'sqlite:///{db_name}')
    df = pd.DataFrame(data)
    df.to_sql('documents', engine, if_exists='replace', index=False)

def query_database(query):
    engine = create_engine('sqlite:///my_database.db')
    df = pd.read_sql('documents', engine)
    results = df[df['content'].str.contains(query, na=False)]
    return results

st.title("PDF Text Extractor and Database Query")

if st.sidebar.button("Extract Text from PDFs"):
    folder_path = 'pdfs'
    data = extract_texts_from_folder(folder_path)
    st.write("Text extracted from PDFs:")
    for entry in data:
        st.write(f"Extracted from {entry['filename']}: {entry['content'][:100]}...")

    create_database(data)
    st.sidebar.success("Database created successfully")

query = st.text_input("Enter query to search the database:")
if st.button("Search"):
    results = query_database(query)
    st.write("Search results:")
    st.write(results)

st.sidebar.info("Use the sidebar buttons to perform actions")