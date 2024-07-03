import EurlexAPI
import APIgoogle
import requests
from bs4 import BeautifulSoup
import re

mots_clés = ['Règlement', 'Décision', 'Directive']

def extraire_debut_a_fin(texteSplit):
    return ' '.join(texteSplit[1:6])

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
        tmp = Dic_indice[key].split(' ')
        if tmp[0] in mots_clés:
            tmpp = EurlexAPI.eurlexAPI(Dic_indice[key])
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