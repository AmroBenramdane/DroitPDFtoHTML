import sys

import pdfplumber

from Traitement.Extraction import *
from tqdm import tqdm
from Traitement import ExtractionResolvator, Texte_TO_html
from Resolvator import ResolvatorAuto
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
        if i not in [5,6,7,8]:
            page = createIndexDict(pdf, i, dict)
            print(dict)
            html_body += Texte_TO_html.Page_to_html(pdf_path, i, dict)
        else:
            html_body += Texte_TO_html.PageSommmaireToHTML(pdf_path, i)

    html_content = Texte_TO_html.finalHtml(html_body)

    # Save the HTML content to a file
    html_output_path = pdf_path.replace('.pdf', '.html')
    with open(html_output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    ResolvatorAuto.modify_html_with_extension(html_output_path)
    ExtractionResolvator.generateurHTML(html_output_path)

    print(f"HTML content saved to {html_output_path}")







