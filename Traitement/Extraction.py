import fitz

from API.EurlexAPI import eurlexAPI
from API import APIgoogle
import re

mots_clés = ['Règlement', 'Décision', 'Directive']
IndiceFait = []

def extraire_debut_a_fin(texteSplit):
    return ' '.join(texteSplit[1:4])

def createIndexDict(pdf,ind,Dic_indice):

    #pdf = pdfplumber.open("ToC-AI-Act-French.pdf")
    page = pdf.pages[ind].extract_text()

    Tab_indice = []
    extrait = ""
    flag = False
    for line in page.split("\n"):
        test = line.split(' ')
        if ((test[0].isnumeric() or test[0] in ['+', '++']) and len(line) > 6) or flag:
            extrait += line + "\n"
            if line[-1] == "." or line == "FR FR":
                flag = False
                Tab_indice.append(extrait)
                extrait = ""
            else:
                flag = True

    for indice in Tab_indice:
        split = indice.split(' ')
        Dic_indice[split[0]] = extraire_debut_a_fin(split)


    for key in Dic_indice.keys():
        if key not in IndiceFait:
            IndiceFait.append(key)
            tmp = Dic_indice[key].split(' ')
            print(tmp)
            if tmp[0] in mots_clés:
                tmpp = eurlexAPI(Dic_indice[key])
                if tmpp is None:
                    tupl = (Dic_indice[key], APIgoogle.requetsGoogleSearch(Dic_indice[key]))
                else:
                    tupl = (Dic_indice[key], tmpp)

            else:
                tupl = (Dic_indice[key], APIgoogle.requetsGoogleSearch(Dic_indice[key]))
            Dic_indice[key] = tupl

    return page


def ancre(url, texte_donne):
    """
    Trouve le numéro d'article dans un texte donné et crée un lien d'ancrage vers cet article.

    Args:
        url (str): URL de la page web.
        texte_donne (str): Texte contenant le mot "article" suivi du numéro de l'article.

    Returns:
        str: Lien d'ancrage vers le numéro d'article trouvé ou un message indiquant que le numéro n'a pas été trouvé.
    """
    # Rechercher le motif "article" suivi d'un numéro
    match = re.search(r'article\s*(\d+)', texte_donne, re.IGNORECASE)
    if match:
        numero_article = match.group(1)
        lien_ancre = f"{url}#art_{numero_article}"
        return f"Lien d'ancrage: {lien_ancre}"
    else:
        return "Numéro d'article non trouvé dans le texte donné."


def is_sommaire(pdf_path, page_number):
    # Ouvrir le fichier PDF
    doc = fitz.open(pdf_path)

    # Charger la page spécifiée (les pages sont indexées à partir de 0)
    page = doc.load_page(page_number)

    # Extraire les mots avec leurs positions
    words = page.get_text("words")  # Extraction des mots avec leurs positions (x, y, w, h, text)

    num_count = 0
    for word in words:
        # Vérifier si le mot est un numéro (utilisation de regex pour matcher les chiffres)
        if re.match(r'\d+', word[4]):
            num_count += 1
            # Vérifier si le numéro est à droite de la page
            if word[0] > page.rect.width / 2:
                return True  # On considère que c'est une TDM si un numéro de page est trouvé à droite

    return False  # Sinon, on ne considère pas la page comme une TDM

