import pandas as pd
from sqlalchemy import create_engine
from extract_text import extract_texts_and_timecodes_from_folder

def create_database(data, db_name='my_database.db'):
    engine = create_engine(f'sqlite:///{db_name}')
    df = pd.DataFrame(data)
    df.to_sql('documents', engine, if_exists='replace', index=False)

if __name__ == "__main__":
    folder_path = 'data/pdf_extraction'  # Assurez-vous que ce chemin est correct
    data = extract_texts_and_timecodes_from_folder(folder_path)
    create_database(data)