import re
import fitz  # PyMuPDF
from html import escape

import pdfplumber

"""def ajout_liens_html(texte, Dic, chiffre):
    # Expression régulière pour trouver les mots qui se terminent par le chiffre donné
    pattern = rf'\b\w*[A-Za-z]+{chiffre}\b'

    # Liste pour stocker les mots modifiés
    mots_modifies = []

    # Fonction de remplacement qui utilise le chiffre
    def remplacement(match):
        mot_complet = match.group(0)
        mots_modifies.append(mot_complet)
        return f'<span class="tooltip"><a href="{Dic[str(chiffre)][1]}" target="_blank">{mot_complet[:-1]}<sup>{mot_complet[-1]}</sup></a><span class="tooltiptext"><iframe src="{Dic[str(chiffre)][1]}"></iframe></span></span>'

    # Utilisation de re.sub avec une fonction de remplacement
    texte_modifie = re.sub(pattern, remplacement, texte)

    return texte_modifie"""
def replace_superscripts_with_html(file_path,page_number,dict):
    doc = fitz.open(file_path)
    full_text = ""
    modifications = []  # Stocker les modifications à apporte

    page = doc.load_page(page_number)  # charger la page
    text_instances = page.get_text("dict")["blocks"]
    for block in text_instances:
        if 'lines' in block:
            for line in block['lines']:
                baseline_y = max([span['bbox'][3] for span in line['spans']])  # y de la base de la ligne
                for span in line['spans']:
                    text = span['text']
                    full_text += text + " "
                    if span['bbox'][3] < baseline_y and (text.isdigit() or text in ['+','++']) and (text in dict.keys()):  # Vérifier si le texte est en superscript et numérique
                        # Planifier le remplacement par HTML
                        lien = dict[text][1]
                        if "eli" in lien:
                            replacement_html = f'<span class="tooltip"> <a href="{lien}" target="_blank"> <sup> {text} </sup> </a> </span>'
                        else:
                            replacement_html = f'<span class="tooltip"> <a href="{lien}" target="_blank"> <sup> {text} </sup> </a> <span class="tooltiptext"> <iframe src="{lien}"> </iframe> </span></span>'
                        modifications.append((len(full_text) - len(text) - 1, len(full_text) - 1, replacement_html))
                full_text += "\n"  # Ajouter une nouvelle ligne après chaque ligne de texte

    # Appliquer les remplacements du dernier au premier pour ne pas perturber les indices de caractères
    for start, end, html in reversed(modifications):
        full_text = full_text[:start] + html + full_text[end:]

    doc.close()
    return full_text

def Page_to_html(fpath,page_number,Dic):
    texte = replace_superscripts_with_html(fpath,page_number,Dic)

    texte = texte.replace('\n', ' <br> ')

    html_page = f"""
     <body>
        <div class="container">
            <p id="{page_number}"> {texte} </p>
        </div>
    </body>
    """
    print(html_page)
    return html_page

def finalHtml(texte):
    html_content = f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f4f4f4;
                    color: #333;
                    text-align: justify;
                }}
                .container {{
                    width: 80%;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #fff;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    text-align: justify;
                }}
                h1 {{
                    text-align: center;
                    color: #4CAF50;
                }}
                p {{
                    line-height: 1.6;
                }}
                a {{
                    color: #4CAF50;
                    text-decoration: none;
                }}
                a:hover {{
                    text-decoration: underline;
                }}
                .tooltip {{
                position: relative;
                display: inline-block;
                cursor: pointer;
                }}
                .tooltip .tooltiptext {{
                visibility: hidden;
                width: 700px;
                height: 600px;
                background-color: #555;
                color: #fff;
                text-align: center;
                border-radius: 6px;
                padding: 10px;
                position: absolute;
                z-index: 1;
                top: 125%; /* Position the tooltip above the text */
                left: 50%;
                margin-left: -200px;
                opacity: 0;
                transition: opacity 0.3s;
                }}
                .tooltip .tooltiptext::after {{
                content: "";
                position: absolute;
                bottom: 100%; /* Arrow at the bottom of the tooltip */
                left: 50%;
                margin-left: -5px;
                border-width: 5px;
                border-style: solid;
                border-color: #555 transparent transparent transparent;
                }}
                .tooltip:hover .tooltiptext {{
                visibility: visible;
                opacity: 1;
                }}
                iframe {{
                width: 100%;
                height: 100%;
                border: none;
                }}
            </style>
        </head>
        {texte}
        </html>
        """

    return html_content


def extract_toc_entries(toc_text):
    # Trouver les entrées de la table des matières avec des regex
    lines = toc_text.split('\n')
    toc_entries = []
    for line in lines:
        match = re.search(r'(.+?)\s+(\d+)$', line)
        if match:
            title = match.group(1).strip()
            page_num = match.group(2).strip()
            toc_entries.append((title, page_num))
    return toc_entries


def PageSommmaireToHTML(pdf_path, toc_page_number):
    # Ouvrir le fichier PDF
    with pdfplumber.open(pdf_path) as pdf:
        # Charger la page de la table des matières
        toc_page = pdf.pages[toc_page_number - 1]

        # Extraire le texte de la page
        toc_text = toc_page.extract_text()

        # Extraire les entrées de la table des matières
        toc_entries = extract_toc_entries(toc_text)

        # Créer la structure HTML pour la table des matières
        html_content = '<body> <div class="container"> <h1>Table des Matières</h1><ul>'

        for title, page_num in toc_entries:
            title = escape(title)
            page_num = int(page_num)
            html_content += f'<li><a href="#{page_num +3}">{title}</a></li>'

        html_content += '</ul>'

        html_content += ' </div> </body>'

    return html_content