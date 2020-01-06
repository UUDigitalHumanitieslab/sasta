import os
from docx import Document


def docx_to_txt(filepath):
    '''converts .docx file to .txt file'''
    try:
        document = Document(filepath)
        txt_path = filepath.replace('.docx', '.txt')
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            for para in document.paragraphs:
                print(para.text, file=txt_file)
        os.remove(filepath)
    except Exception as error:
        print(error)
