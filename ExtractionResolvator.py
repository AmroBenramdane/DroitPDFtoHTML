from bs4 import BeautifulSoup
import re
import EurlexAPI

def get_body_html_list(file_path):
    """
    Cette fonction prend en paramètre le chemin d'un fichier HTML,
    lit le contenu du fichier et renvoie une liste contenant le HTML brut
    de chaque élément enfant dans les balises <body> du document.
    """
    # Lire le contenu du fichier HTML
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse le contenu HTML avec BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Trouver toutes les balises <body>
    bodies = soup.find_all('body')

    # Initialiser une liste pour accumuler le texte brut
    tab_body = []

    # Itérer sur chaque <body>
    for body in bodies:
        # Itérer sur chaque élément enfant du body
        for element in body.find_all(recursive=False):
            # Ajouter le HTML brut de chaque élément à la liste
            tab_body.append(str(element))

    return tab_body


def split_html_text(html_content):
    """
    Cette fonction prend un texte HTML et le divise en une liste
    contenant les segments de texte brut et les balises HTML,
    en excluant les balises de type <block> spécifiées.
    """
    # Expression régulière pour trouver les balises HTML
    html_tag_regex = re.compile(r'(<[^>]+>)')

    # Utiliser re.split pour diviser le texte par les balises HTML
    split_content = re.split(html_tag_regex, html_content)

    # Filtrer les segments pour supprimer les chaînes vides et les balises <block> spécifiées
    split_content = [
        segment for segment in split_content
        if segment.strip() and not re.match(r'<\/?block\b', segment.strip(), re.IGNORECASE)
    ]

    return split_content

def split_text_segments(segments):
    """
    Cette fonction prend une liste de segments de texte HTML et renvoie une nouvelle liste
    où les segments de texte brut sont divisés en mots individuels, tandis que les balises HTML
    restent intactes.
    """
    result = []

    # Expression régulière pour identifier les balises HTML
    html_tag_regex = re.compile(r'<[^>]+>')

    for segment in segments:
        if html_tag_regex.match(segment):
            # Si le segment est une balise HTML, l'ajouter directement à la liste des résultats
            result.append(segment)
        else:
            # Si le segment est du texte brut, le diviser en mots et les ajouter à la liste des résultats
            words = segment.split()
            result.extend(words)

    return result


def reposition_resolvator_tags(segments):
    """
    Cette fonction prend une liste de segments de texte HTML et modifie l'emplacement des balises
    Resolvator. Les balises de début sont déplacées en arrière jusqu'à trouver les mots 'article',
    'décision', 'directive', et les balises de fermeture sont déplacées en avant jusqu'à trouver
    'et', '.', ou ','.
    """
    mots_cles_gauche = ['article', 'articles', 'règlement', 'décision', 'directive']
    mots_cles_droite = ['et', '.', ',']

    mots_cles_gauche_regex = re.compile(r'\b(' + '|'.join(mots_cles_gauche) + r')\b', re.IGNORECASE)
    mots_cles_droite_regex = re.compile(r'\b(' + '|'.join(mots_cles_droite) + r')\b', re.IGNORECASE)

    # Liste de flags pour les index des balises déjà déplacées
    moved_indices = set()

    i = 0
    while i < len(segments):
        if 'data-exotic="resolvator"' in segments[i] and i not in moved_indices:
            # Déplacer la balise d'ouverture
            j = i - 1
            found_article = False
            while j >= 0:
                if isinstance(segments[j], str) and 'article' in segments[j].lower():
                    segments.insert(j, segments.pop(i))
                    moved_indices.add(j)  # Ajouter l'index déplacé aux flags
                    i = j  # Ajuster l'indice après déplacement
                    found_article = True
                    break
                elif isinstance(segments[j], str) and mots_cles_gauche_regex.search(segments[j]):
                    # Si on ne trouve pas "article", déplacer jusqu'à trouver un autre mot clé
                    segments.insert(j, segments.pop(i))
                    moved_indices.add(j)  # Ajouter l'index déplacé aux flags
                    i = j  # Ajuster l'indice après déplacement
                    break
                elif '</a>' in segments[j]:
                    break
                j -= 1

            if not found_article:
                # Si "article" n'a pas été trouvé, chercher les autres mots
                j = i - 1
                while j >= 0:
                    if isinstance(segments[j], str) and mots_cles_gauche_regex.search(segments[j]):
                        segments.insert(j, segments.pop(i))
                        moved_indices.add(j)  # Ajouter l'index déplacé aux flags
                        i = j  # Ajuster l'indice après déplacement
                        break
                    elif '</a>' in segments[j]:
                        break
                    j -= 1

        i += 1

    return segments

def generateurHTML(file_path):
    html = f""""""
    tab_body = get_body_html_list(file_path)
    for body in tab_body:
        split_result = split_text_segments(split_html_text(body))
        if split_result[0] != '<script>':
            split_result = reposition_resolvator_tags(split_result)
            temp = ' '.join(split_result)
            bodyy = f"""
                 <body>
                    {Ajout_ancrage(temp)}
                </body>
                """
            html += bodyy

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
                    }}
                    .container {{
                        width: 80%;
                        margin: 0 auto;
                        padding: 20px;
                        background-color: #fff;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
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
            {html}
            </html>
            """

    with open(f"pdfWithResolvator_interactif.html", "w", encoding="utf-8") as file:
        file.write(html_content)
    print("Le document HTML avec resolvator a été créé avec succès.")


def Ajout_ancrage(html):
    """
    Modifie les liens <a> dans le contenu HTML si le texte contient le mot "article" suivi d'un nombre.
    Remplace l'attribut href par le nouveau URL suivi de #art_{numéro de l'article}.

    Args:
        html (str): Le contenu HTML à traiter.

    Returns:
        str: Le contenu HTML modifié.
    """
    soup = BeautifulSoup(html, 'html.parser')

    # Rechercher toutes les balises <a> avec les attributs spécifiques
    for a_tag in soup.find_all('a', {'data-corpus': 'resolvator-direg', 'data-exotic': 'resolvator'}):
        if a_tag.has_attr('data-role') and a_tag.has_attr('href'):
            # Vérifier si le texte contient "article" suivi d'un nombre
            match = re.search(r'article\s*(\d+)', a_tag.get_text(), re.IGNORECASE)
            if match:
                numero_article = match.group(1)
                data_role = a_tag['data-role']
                new_url = EurlexAPI.eurlexAPI(data_role)
                if new_url is not None:
                    # Modifier l'attribut href
                    new_href = f"{new_url}#art_{numero_article}"
                    a_tag['href'] = new_href

    return str(soup)



