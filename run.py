from io import StringIO
from os import listdir
from os.path import isfile, join

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

def get_text_from_pdf(file):
    output_string = StringIO()
    with open(file, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
    return output_string.getvalue()

def get_list_of_files(mypath, extension):
    extension_norm = '.'+extension.lower().replace('.','')
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f.lower().endswith(extension_norm)]
    onlyfiles.sort()
    return onlyfiles

mypath = './data'
files = get_list_of_files(mypath, 'pdf')#[7:8]
#files = get_list_of_files(mypath, 'pdf')

f= open("output.txt","w+")

for file in files:
    file_full_path = join(mypath, file)
    pdf_text = get_text_from_pdf(file_full_path).split('\n')
    ref_index = pdf_text.index('NÚMERO DE CRÉDITO')
    pdf_text_filtered = [pdf_text[i] for i in range(len(pdf_text)) if pdf_text[i] != '' and (i>=ref_index or pdf_text[i].startswith('Nro.  '))]
    
    index_to_take = [0, 4, 3, 5, 28, 22, 15,37,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,74,75,77,80,81,83]
    extracted_data = [pdf_text_filtered[i] for i in index_to_take]
    print('|'.join(extracted_data))
    f.write('|'.join(extracted_data)+'\n')

f.close()
    
"""     lines = len(pdf_text_filtered)
    for i in range(lines):
        if len(pdf_text_filtered[i])<80:
            print(f'{i}: {pdf_text_filtered[i]}') """
    

