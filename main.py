import sys

import pdfplumber

import Texte_TO_html
from Extraction import *
from tqdm import tqdm
import warnings
import ExtractionResolvator

"""
warnings.filterwarnings("ignore")

if choix == 1:
    path = "ToC-AI-Act-French.pdf"
    pdf = pdfplumber.open(path)
    taille = len(pdf.pages)

    html_body = ""
    dict = {}

    for i in tqdm(range(14, 15), desc="Processing pages"):

        page = createIndexDict(pdf,i,dict)
        print(dict)
        html_body += Texte_TO_html.Page_to_html(path,i,dict)


    Texte_TO_html.finalHtml(html_body)

#l'ulisateur ouvre le document html sur son navigateur (chrome de pref) puis applique l'extension Resolvator
#Ensuite, il doit réappeler le script avec script -Resolvator <fichier.html>
else:
    ExtractionResolvator.generateurHTML('pdfTOhtml_interactif.html')

"""

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python process_pdf.py <pdf_path>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    print("jiji")
    pdf = pdfplumber.open(pdf_path)
    taille = len(pdf.pages)

    html_body = ""
    dict = {}

    for i in tqdm(range(0, taille), desc="Processing pages"):
        page = createIndexDict(pdf, i, dict)
        print(dict)
        html_body += Texte_TO_html.Page_to_html(pdf_path, i, dict)

    html_content = Texte_TO_html.finalHtml(html_body)

    # Save the HTML content to a file
    html_output_path = pdf_path.replace('.pdf', '.html')
    with open(html_output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"HTML content saved to {html_output_path}")







